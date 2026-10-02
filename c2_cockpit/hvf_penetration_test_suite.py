"""
HVF Sovereign Adversarial Cyber-Physical Penetration Test Suite
Automated security regression and stress verification engine attacking the SCADA defense matrix:
Dual-Key Forgery, Modbus CRC Fuzzing, Merkle Ledger Tampering, and Deadlock Starvation.
DFARS 252.227-7018 Compliant Architecture.
"""

import os
import sys
import time
import json
import logging
from typing import Dict, Any

try:
    from scada_engine.hvf_defense_pipeline import HVFDefensePipeline
    from scada_engine.hvf_kinetic_relay import BreakerChannel, DualKeyAuthorizationError
    from scada_engine.hvf_modbus_driver import HVFModbusDriver
    from scada_engine.hvf_crypto_ledger import HVFCryptoLedger
except ImportError:
    from hvf_defense_pipeline import HVFDefensePipeline
    from hvf_kinetic_relay import BreakerChannel, DualKeyAuthorizationError
    from hvf_modbus_driver import HVFModbusDriver
    from hvf_crypto_ledger import HVFCryptoLedger

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class HVFPenetrationTestSuite:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.pipeline = HVFDefensePipeline(db_path=self.db_path, watchdog_timeout_ms=300)

    def test_forged_dual_key_attack(self) -> bool:
        """Attack 1: Attempts single-key and forged key bypass against CH1 Utility Grid."""
        logging.info("  [TEST 1] Attacking Dual-Key Security Gate with forged & unauthorized keys...")
        
        # 1a. Missing secondary key
        caught_1a = False
        try:
            self.pipeline.relay.trip_breaker(BreakerChannel.CH1_GRID, reason="EXPLOIT_SINGLE_KEY", key_primary="ATTACKER_KEY_001")
        except Exception as e:
            if "Dual-key authorization" in str(e) or "DualKeyAuthorizationError" in type(e).__name__:
                caught_1a = True
        if not caught_1a:
            return False

        # 1b. Identical duplicate keys
        caught_1b = False
        try:
            self.pipeline.relay.trip_breaker(BreakerChannel.CH1_GRID, reason="EXPLOIT_DUPLICATE_KEY", key_primary="ATTACKER_KEY_001", key_secondary="ATTACKER_KEY_001")
        except Exception as e:
            if "Dual-key authorization" in str(e) or "DualKeyAuthorizationError" in type(e).__name__:
                caught_1b = True
        if not caught_1b:
            return False

        # 1c. Short entropy key
        caught_1c = False
        try:
            self.pipeline.relay.trip_breaker(BreakerChannel.CH1_GRID, reason="EXPLOIT_SHORT_KEY", key_primary="KEY1", key_secondary="KEY2")
        except Exception as e:
            if "Dual-key authorization" in str(e) or "DualKeyAuthorizationError" in type(e).__name__:
                caught_1c = True
        if not caught_1c:
            return False

        return True

    def test_modbus_frame_corruption_fuzzing(self) -> bool:
        """Attack 2: Injects corrupted CRC, malformed lengths, and bit-flipped payloads into RS-485 parser."""
        logging.info("  [TEST 2] Fuzzing Modbus RTU RS-485 transceiver with corrupted frames...")
        driver = self.pipeline.modbus

        # Valid frame
        valid_frame = driver.build_write_coil_frame(coil_address=1, state=True)

        # Corrupt CRC (bit flip)
        corrupted_crc = valid_frame[:-1] + bytes([valid_frame[-1] ^ 0xFF])
        try:
            driver.parse_response_frame(corrupted_crc)
            return False
        except ValueError:
            pass

        # Truncated frame
        try:
            driver.parse_response_frame(valid_frame[:3])
            return False
        except ValueError:
            pass

        return True

    def test_merkle_ledger_tamper_detection(self) -> bool:
        """Attack 3: Deliberately mutates historical SQLite event payload and asserts forensic alarm."""
        logging.info("  [TEST 3] Simulating unauthorized forensic database payload modification...")
        ledger = self.pipeline.crypto_ledger
        
        # Commit legitimate events
        ledger.commit_event("NOMINAL_EVENT_1", {"sensor": "V_GRID", "value": 120.4})
        ledger.commit_event("NOMINAL_EVENT_2", {"sensor": "I_GRID", "value": 45.2})
        
        valid_before, _, _ = ledger.verify_chain_integrity()
        if not valid_before:
            return False

        # Adversary mutates block 1 payload directly in SQLite
        conn = ledger._get_connection()
        conn.execute("UPDATE forensic_audit_ledger SET payload_json = ? WHERE block_index = 1", (json.dumps({"tampered": True}),))
        conn.commit()

        valid_after, count, errors = ledger.verify_chain_integrity()
        return (not valid_after) and (len(errors) > 0)

    def test_watchdog_deadlock_recovery(self) -> bool:
        """Attack 4: Simulates complete host thread deadlock and verifies autonomous fail-safe DER trip."""
        logging.info("  [TEST 4] Simulating thread deadlock / heartbeat starvation (350ms window)...")
        self.pipeline.watchdog.arm()
        time.sleep(0.40)
        
        status_ok = (self.pipeline.watchdog.status == "FAILSAFE_TRIPPED")
        der_isolated = (self.pipeline.relay.channels[BreakerChannel.CH2_SOLAR] == "TRIPPED")
        
        self.pipeline.watchdog.disarm()
        return status_ok and der_isolated

    def run_all_tests(self) -> bool:
        logging.info("=== STARTING ADVERSARIAL CYBER-PHYSICAL PENETRATION SUITE ===")
        
        t1 = self.test_forged_dual_key_attack()
        assert t1, "Test 1 Failed: Dual-Key security gate breached!"
        logging.info("  [PASS] Test 1: Forged Dual-Key Bypass Attempts Defeated 100%")

        t2 = self.test_modbus_frame_corruption_fuzzing()
        assert t2, "Test 2 Failed: Modbus parser accepted corrupted CRC!"
        logging.info("  [PASS] Test 2: RS-485 Modbus Bit-Flipping & CRC Mutation Rejected")

        t3 = self.test_merkle_ledger_tamper_detection()
        assert t3, "Test 3 Failed: Database tampering went undetected!"
        logging.info("  [PASS] Test 3: Unauthorized Forensic Database Tampering Detected Instantly")

        t4 = self.test_watchdog_deadlock_recovery()
        assert t4, "Test 4 Failed: Watchdog failed to execute autonomous DER trip!"
        logging.info("  [PASS] Test 4: Host Deadlock Starvation Forced Autonomous Fail-Safe Isolation")

        logging.info("=== ADVERSARIAL PENETRATION SUITE 100% NOMINAL -- ARCHITECTURE SECURED ===")
        return True

if __name__ == "__main__":
    suite = HVFPenetrationTestSuite()
    suite.run_all_tests()
