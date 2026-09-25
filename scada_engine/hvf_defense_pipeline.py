"""
HVF Autonomous SCADA Defense Pipeline Orchestrator — End-to-End Threat Integration
Integrates NOAA Threat Oracle, Dual-Key Kinetic Relay, Modbus RTU Fieldbus,
and Hardware Watchdog Supervisor into a unified sovereign execution pipeline.
DFARS 252.227-7018 Compliant Architecture.
"""

import os
import sys
import time
import logging
import sqlite3
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone

# Resilient imports across workspace roots
try:
    from scada_engine.hvf_noaa_oracle import HVFNoaaOracle, ThreatTier
    from scada_engine.hvf_kinetic_relay import HVFKineticRelay, BreakerChannel, BreakerState, DualKeyAuthorizationError
    from scada_engine.hvf_watchdog_timer import HVFWatchdogTimer, WatchdogStatus
    from scada_engine.hvf_modbus_driver import HVFModbusDriver
except ImportError:
    from hvf_noaa_oracle import HVFNoaaOracle, ThreatTier
    from hvf_kinetic_relay import HVFKineticRelay, BreakerChannel, BreakerState, DualKeyAuthorizationError
    from hvf_watchdog_timer import HVFWatchdogTimer, WatchdogStatus
    from hvf_modbus_driver import HVFModbusDriver

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class HVFDefensePipeline:
    def __init__(
        self,
        db_path: Optional[str] = None,
        station_id: str = "KOKC",
        modbus_port: str = "COM1",
        watchdog_timeout_ms: int = 1000
    ):
        self.station_id = station_id
        default_db = os.path.join(os.getenv("HVF_VAULT_PATH", "./cinematic_vault"), "database", "hvf_memory_vault.db")
        self.db_path = db_path or os.getenv("HVF_DATABASE_PATH", default_db)

        # 1. Initialize Subsystems
        self.oracle = HVFNoaaOracle(db_path=self.db_path, station_id=self.station_id)
        self.relay = HVFKineticRelay(db_path=self.db_path, simulated_hardware=True)
        self.modbus = HVFModbusDriver(port=modbus_port, db_path=self.db_path, virtual_bus=True)
        
        # 2. Breaker Channel to Modbus Coil Mapping
        self.channel_coil_map: Dict[str, int] = {
            BreakerChannel.CH1_GRID: 1,
            BreakerChannel.CH2_SOLAR: 2,
            BreakerChannel.CH3_BATTERY: 3,
            BreakerChannel.CH4_GENSET: 4
        }
        
        # 3. Watchdog Failsafe Hook (trips DER and alerts on thread lock)
        self.watchdog = HVFWatchdogTimer(
            timeout_ms=watchdog_timeout_ms,
            check_interval_ms=max(20, watchdog_timeout_ms // 10),
            db_path=self.db_path,
            failsafe_callback=self._emergency_watchdog_trip
        )
        
        # 4. Pipeline Execution Metrics
        self.last_pipeline_latency_us: float = 0.0

    def _emergency_watchdog_trip(self) -> Dict[str, Any]:
        """Emergency failsafe callback executed if SCADA watchdog starves."""
        logging.critical("🚨 [PIPELINE EMERGENCY] Watchdog starved! Actuating autonomous Modbus DER de-energization!")
        trip_res = self.relay.trip_breaker(BreakerChannel.CH2_SOLAR, reason="WATCHDOG_TIMEOUT_EMERGENCY")
        self.modbus.transmit_coil_actuation(coil_address=self.channel_coil_map[BreakerChannel.CH2_SOLAR], state=False)
        self.modbus.transmit_coil_actuation(coil_address=self.channel_coil_map[BreakerChannel.CH3_BATTERY], state=False)
        return trip_res

    def process_threat_alert(
        self,
        alert_payload: Dict[str, Any],
        key_primary: Optional[str] = None,
        key_secondary: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        End-to-End Pipeline Execution:
        1. Pet Watchdog
        2. Evaluate NOAA Threat Tier & Acoustic Beacons
        3. If Tier >= 3:
           a. Autonomously trip DER microgrid coils (CH2 Solar, CH3 Battery) via Modbus RTU
           b. If dual keys provided, trip Utility Grid (CH1) via Modbus RTU
        4. Return unified audit dispatch record
        """
        t_start = time.perf_counter_ns()
        self.watchdog.pet()

        # Step 1: NOAA Oracle Ingestion & Threat Classification
        oracle_record = self.oracle.evaluate_payload(alert_payload)
        threat_tier = oracle_record["threat_tier"]
        kinetic_trigger = oracle_record["kinetic_trigger"]

        pipeline_dispatch = {
            "event_id": oracle_record["event_id"],
            "threat_tier": threat_tier,
            "tier_label": oracle_record["tier_label"],
            "kinetic_trigger": kinetic_trigger,
            "tripped_channels": [],
            "modbus_frames": [],
            "dual_key_authorized": False,
            "grid_isolated": False
        }

        # Step 2: Actuator Logic
        if kinetic_trigger == 1:
            logging.warning(f"⚡ [PIPELINE ENGAGED] Kinetic trigger active for Tier {threat_tier} ({oracle_record['tier_label']})")
            
            # 2a. Autonomous DER Trip (Solar & Battery)
            for ch in [BreakerChannel.CH2_SOLAR, BreakerChannel.CH3_BATTERY]:
                trip_res = self.relay.trip_breaker(ch, reason=f"NOAA_TIER_{threat_tier}_{oracle_record['event_type']}")
                coil_addr = self.channel_coil_map[ch]
                modbus_res = self.modbus.transmit_coil_actuation(coil_address=coil_addr, state=False)
                pipeline_dispatch["tripped_channels"].append(ch)
                pipeline_dispatch["modbus_frames"].append(modbus_res)

            # 2b. Utility Grid Separation (Requires Dual-Key Verification)
            if key_primary and key_secondary:
                try:
                    grid_trip = self.relay.trip_breaker(
                        BreakerChannel.CH1_GRID,
                        reason=f"NOAA_TIER_{threat_tier}_DUAL_KEY_AUTHORIZED",
                        key_primary=key_primary,
                        key_secondary=key_secondary
                    )
                    grid_coil = self.channel_coil_map[BreakerChannel.CH1_GRID]
                    modbus_grid = self.modbus.transmit_coil_actuation(coil_address=grid_coil, state=False)
                    pipeline_dispatch["tripped_channels"].append(BreakerChannel.CH1_GRID)
                    pipeline_dispatch["modbus_frames"].append(modbus_grid)
                    pipeline_dispatch["dual_key_authorized"] = True
                    pipeline_dispatch["grid_isolated"] = True
                    logging.critical(f"🔒 [PIPELINE SUCCESS] Dual-Key Grid Isolation Completed via Modbus Coil {grid_coil}!")
                except DualKeyAuthorizationError as e:
                    logging.error(f"❌ Dual-Key Grid Isolation rejected by relay: {e}")
            else:
                logging.info("ℹ️ Utility Grid (CH1) maintained in CLOSED state — dual keys not supplied. DER isolated.")

        t_end = time.perf_counter_ns()
        self.last_pipeline_latency_us = round((t_end - t_start) / 1000.0, 3)
        pipeline_dispatch["pipeline_latency_us"] = self.last_pipeline_latency_us
        self.watchdog.pet()
        return pipeline_dispatch

    def run_self_test(self) -> bool:
        """Executes full end-to-end integration audit across all 4 defense subsystems."""
        logging.info("=== STARTING FULL END-TO-END SCADA PIPELINE AUDIT ===")
        self.watchdog.arm()

        # Test Case 1: Tier 1 Frost Advisory (No Kinetic Action)
        res1 = self.process_threat_alert({"event": "Frost Advisory", "severity": "Minor"})
        assert res1["kinetic_trigger"] == 0
        assert len(res1["tripped_channels"]) == 0
        logging.info(f"  [PASS] Tier 1 Handled Nominally: No Kinetic Actuation ({res1['pipeline_latency_us']}µs)")

        # Test Case 2: Tier 3 Tornado Warning without Dual Keys (Autonomous DER Isolation, Grid Holds)
        res2 = self.process_threat_alert({"event": "Tornado Warning", "severity": "Extreme"})
        assert res2["kinetic_trigger"] == 1
        assert BreakerChannel.CH2_SOLAR in res2["tripped_channels"]
        assert BreakerChannel.CH3_BATTERY in res2["tripped_channels"]
        assert BreakerChannel.CH1_GRID not in res2["tripped_channels"]
        assert res2["grid_isolated"] is False
        assert self.modbus._virtual_coils[2] is False
        assert self.modbus._virtual_coils[3] is False
        logging.info(f"  [PASS] Tier 3 Handled Nominally: DER Isolated Autonomously, Grid Protected ({res2['pipeline_latency_us']}µs)")

        # Test Case 3: Tier 4 Tornado Emergency with Dual-Key Custody (Full Grid & Array Separation)
        res3 = self.process_threat_alert(
            {"event": "Tornado Emergency", "severity": "Catastrophic"},
            key_primary="CEO_HUMPHREY_AUTH_1AHA8",
            key_secondary="DEFENSE_OFFICER_SIG_OKC01"
        )
        assert res3["kinetic_trigger"] == 1
        assert res3["dual_key_authorized"] is True
        assert res3["grid_isolated"] is True
        assert BreakerChannel.CH1_GRID in res3["tripped_channels"]
        assert self.modbus._virtual_coils[1] is False
        logging.info(f"  [PASS] Tier 4 Dual-Key End-to-End Pipeline Complete: Full Kinetic Grid Separation ({res3['pipeline_latency_us']}µs)")

        # Test Case 4: Pipeline Contactor Re-Arming Protocol
        self.relay.reset_breaker(BreakerChannel.ALL, operator_override_sig="CEO_HUMPHREY_AUTH_001")
        for ch, coil in self.channel_coil_map.items():
            self.modbus.transmit_coil_actuation(coil_address=coil, state=True)
            assert self.modbus._virtual_coils[coil] is True
        logging.info("  [PASS] Operator Override Contactor Re-Arming Verified Across All Coils")

        self.watchdog.disarm()
        logging.info("=== FULL END-TO-END SCADA PIPELINE AUDIT 100% NOMINAL ===")
        return True

if __name__ == "__main__":
    pipeline = HVFDefensePipeline(db_path=":memory:")
    pipeline.run_self_test()
