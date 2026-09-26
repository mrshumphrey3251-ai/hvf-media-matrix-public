"""
HVF Autonomous SCADA Defense Pipeline Orchestrator — Cryptographically Sealed Architecture
Integrates NOAA Threat Oracle, Dual-Key Kinetic Relay, Modbus RTU Fieldbus,
Hardware Watchdog Supervisor, and Ed25519 Cryptographic Audit Ledger.
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
    from scada_engine.hvf_crypto_ledger import HVFCryptoLedger
except ImportError:
    from hvf_noaa_oracle import HVFNoaaOracle, ThreatTier
    from hvf_kinetic_relay import HVFKineticRelay, BreakerChannel, BreakerState, DualKeyAuthorizationError
    from hvf_watchdog_timer import HVFWatchdogTimer, WatchdogStatus
    from hvf_modbus_driver import HVFModbusDriver
    from hvf_crypto_ledger import HVFCryptoLedger

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
        self.crypto_ledger = HVFCryptoLedger(db_path=self.db_path)
        
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
        
        # Cryptographically seal watchdog trip into audit ledger
        self.crypto_ledger.commit_event("WATCHDOG_EMERGENCY_FAILSAFE", {
            "action": "KINETIC_DER_DE-ENERGIZATION",
            "channels": [BreakerChannel.CH2_SOLAR, BreakerChannel.CH3_BATTERY],
            "reason": "THREAD_HEARTBEAT_STARVATION"
        })
        return trip_res

    def process_threat_alert(
        self,
        alert_payload: Dict[str, Any],
        key_primary: Optional[str] = None,
        key_secondary: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        End-to-End Pipeline Execution with Deep Cryptographic Sealing:
        1. Pet Watchdog
        2. Evaluate NOAA Threat Tier & Acoustic Beacons
        3. If Tier >= 3:
           a. Autonomously trip DER microgrid coils (CH2 Solar, CH3 Battery) via Modbus RTU
           b. Seal DER trip event in Ed25519 Cryptographic Ledger
           c. If dual keys provided, trip Utility Grid (CH1) via Modbus RTU and seal in Ledger
        4. Seal overall pipeline dispatch block into the tamper-proof Merkle chain
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
            "grid_isolated": False,
            "sealed_ledger_blocks": []
        }

        # Step 2: Actuator Logic & Cryptographic Sealing
        if kinetic_trigger == 1:
            logging.warning(f"⚡ [PIPELINE ENGAGED] Kinetic trigger active for Tier {threat_tier} ({oracle_record['tier_label']})")
            
            # 2a. Autonomous DER Trip (Solar & Battery)
            for ch in [BreakerChannel.CH2_SOLAR, BreakerChannel.CH3_BATTERY]:
                trip_res = self.relay.trip_breaker(ch, reason=f"NOAA_TIER_{threat_tier}_{oracle_record['event_type']}")
                coil_addr = self.channel_coil_map[ch]
                modbus_res = self.modbus.transmit_coil_actuation(coil_address=coil_addr, state=False)
                pipeline_dispatch["tripped_channels"].append(ch)
                pipeline_dispatch["modbus_frames"].append(modbus_res)

            # Seal autonomous DER trip event in Ed25519 Ledger
            der_block = self.crypto_ledger.commit_event("AUTONOMOUS_DER_ISOLATION", {
                "event_id": oracle_record["event_id"],
                "threat_tier": threat_tier,
                "event_type": oracle_record["event_type"],
                "channels_isolated": [BreakerChannel.CH2_SOLAR, BreakerChannel.CH3_BATTERY],
                "actuation_protocol": "MODBUS_RTU_FC05"
            })
            pipeline_dispatch["sealed_ledger_blocks"].append(der_block["block_index"])

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
                    
                    # Seal dual-key grid separation in Ed25519 Ledger
                    grid_block = self.crypto_ledger.commit_event("DUAL_KEY_GRID_ISOLATION", {
                        "event_id": oracle_record["event_id"],
                        "channel": BreakerChannel.CH1_GRID,
                        "modbus_coil": grid_coil,
                        "auth_mode": "DUAL_KEY_VERIFIED",
                        "key_primary_id": key_primary[:8] + "...",
                        "key_secondary_id": key_secondary[:8] + "..."
                    })
                    pipeline_dispatch["sealed_ledger_blocks"].append(grid_block["block_index"])
                except DualKeyAuthorizationError as e:
                    logging.error(f"❌ Dual-Key Grid Isolation rejected by relay: {e}")
            else:
                logging.info("ℹ️ Utility Grid (CH1) maintained in CLOSED state — dual keys not supplied. DER isolated.")

        t_end = time.perf_counter_ns()
        self.last_pipeline_latency_us = round((t_end - t_start) / 1000.0, 3)
        pipeline_dispatch["pipeline_latency_us"] = self.last_pipeline_latency_us
        
        # Commit Master Pipeline Dispatch Block to Ledger
        dispatch_block = self.crypto_ledger.commit_event("PIPELINE_DISPATCH_SUMMARY", {
            "event_id": oracle_record["event_id"],
            "threat_tier": threat_tier,
            "kinetic_trigger": kinetic_trigger,
            "grid_isolated": pipeline_dispatch["grid_isolated"],
            "tripped_channels": pipeline_dispatch["tripped_channels"],
            "pipeline_latency_us": self.last_pipeline_latency_us
        })
        pipeline_dispatch["sealed_ledger_blocks"].append(dispatch_block["block_index"])
        
        self.watchdog.pet()
        return pipeline_dispatch

    def run_self_test(self) -> bool:
        """Executes full end-to-end integration and cryptographic sealing audit."""
        logging.info("=== STARTING FULL END-TO-END SCADA PIPELINE AUDIT (BATCH 13) ===")
        self.watchdog.arm()

        # Test Case 1: Tier 1 Frost Advisory (No Kinetic Action)
        res1 = self.process_threat_alert({"event": "Frost Advisory", "severity": "Minor"})
        assert res1["kinetic_trigger"] == 0
        assert len(res1["tripped_channels"]) == 0
        logging.info(f"  [PASS] Tier 1 Handled Nominally: No Kinetic Actuation ({res1['pipeline_latency_us']}us)")

        # Test Case 2: Tier 3 Tornado Warning without Dual Keys (Autonomous DER Isolation, Grid Holds)
        res2 = self.process_threat_alert({"event": "Tornado Warning", "severity": "Extreme"})
        assert res2["kinetic_trigger"] == 1
        assert BreakerChannel.CH2_SOLAR in res2["tripped_channels"]
        assert BreakerChannel.CH3_BATTERY in res2["tripped_channels"]
        assert BreakerChannel.CH1_GRID not in res2["tripped_channels"]
        assert res2["grid_isolated"] is False
        assert self.modbus._virtual_coils[2] is False
        assert self.modbus._virtual_coils[3] is False
        logging.info(f"  [PASS] Tier 3 Handled Nominally: DER Isolated Autonomously, Grid Protected ({res2['pipeline_latency_us']}us)")

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
        logging.info(f"  [PASS] Tier 4 Dual-Key End-to-End Pipeline Complete: Full Kinetic Grid Separation ({res3['pipeline_latency_us']}us)")

        # Test Case 4: Pipeline Contactor Re-Arming Protocol
        self.relay.reset_breaker(BreakerChannel.ALL, operator_override_sig="CEO_HUMPHREY_AUTH_001")
        for ch, coil in self.channel_coil_map.items():
            self.modbus.transmit_coil_actuation(coil_address=coil, state=True)
            assert self.modbus._virtual_coils[coil] is True
            
        rearm_block = self.crypto_ledger.commit_event("OPERATOR_REARM_PROTOCOL", {
            "operator_sig": "CEO_HUMPHREY_AUTH_001",
            "channels_rearmed": list(self.channel_coil_map.keys())
        })
        logging.info(f"  [PASS] Operator Override Contactor Re-Arming Verified & Sealed (Block #{rearm_block['block_index']})")

        # Test Case 5: Full Cryptographic Chain-of-Custody Integrity Audit
        valid, block_count, errors = self.crypto_ledger.verify_chain_integrity()
        assert valid is True
        assert block_count >= 5, f"Expected >= 5 blocks, got {block_count}"
        assert len(errors) == 0
        logging.info(f"  [PASS] Cryptographic Chain-of-Custody 100% Intact ({block_count} Blocks Verified with Ed25519)")

        self.watchdog.disarm()
        logging.info("=== FULL END-TO-END SCADA PIPELINE AUDIT 100% NOMINAL (BATCH 13 SEALED) ===")
        return True

if __name__ == "__main__":
    pipeline = HVFDefensePipeline(db_path=":memory:")
    pipeline.run_self_test()
