# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Emergency Guardian Test Suite
Sanitized Interface Contract Tests for Open Source Builds
Redacted Implementation: Proprietary hemodynamic shock matrices removed.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GUARD_DIR = os.path.join(REPO_ROOT, "chronos_core", "guardian")
if GUARD_DIR not in sys.path:
    sys.path.insert(0, GUARD_DIR)

from chronos_emergency_guardian import (
    ChronosEmergencyGuardian, ThreatVector, ChallengePhase, EmergencyDispatchPayload
)

class TestChronosEmergencyGuardianPublic(unittest.TestCase):
    def setUp(self):
        self.guardian = ChronosEmergencyGuardian()

    def test_public_interface_contracts(self):
        # 1. Asystole contract
        threat = self.guardian.evaluate_vitals(
            heart_rate_bpm=0.0, spo2_pct=98.0, perfusion_index=1.0,
            rmssd_ms=0.0, net_acc_g=1.0, gait_state="STATIONARY"
        )
        self.assertEqual(threat, ThreatVector.ASYSTOLE_CARDIAC_ARREST)

        # 2. Dispatch contract
        payload = self.guardian.build_emergency_dispatch()
        self.assertIsInstance(payload, EmergencyDispatchPayload)
        self.assertEqual(payload.threat_vector, "ASYSTOLE_CARDIAC_ARREST")

        # 3. Disarm contract
        self.assertTrue(self.guardian.disarm_challenge())
        self.assertEqual(self.guardian.active_threat, ThreatVector.NONE)

if __name__ == "__main__":
    unittest.main()
