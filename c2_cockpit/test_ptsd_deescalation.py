# -*- coding: utf-8 -*-
"""
Ebony Chronos Public PTSD Engine Test Suite
Sanitized Interface Contract Tests for Open Source Builds
Redacted Implementation: Proprietary sensory resonance tables removed.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PTSD_DIR = os.path.join(REPO_ROOT, "chronos_core", "ptsd")
if PTSD_DIR not in sys.path:
    sys.path.insert(0, PTSD_DIR)

from chronos_ptsd_deescalation import (
    ChronosPTSDDeEscalationEngine, CrisisState, TactilePacingPattern,
    GroundingStage, DeEscalationStatus
)

class TestChronosPTSDDeEscalationPublic(unittest.TestCase):
    def setUp(self):
        self.engine = ChronosPTSDDeEscalationEngine()

    def test_public_interface_contracts(self):
        state = self.engine.evaluate_crisis_signature(
            tonic_scl_us=12.0, phasic_scr_amplitude=2.0, current_rmssd=10.0,
            net_acc_g=1.0, is_tremor=False, gait_state="STATIONARY"
        )
        self.assertEqual(state, CrisisState.ACUTE_SYMPATHETIC_FREEZE)

        status = self.engine.step_de_escalation()
        self.assertIsInstance(status, DeEscalationStatus)
        self.assertTrue(status.is_intervention_active)
        self.assertEqual(status.tactile_pattern, TactilePacingPattern.HEARTBEAT_55BPM.value)

if __name__ == "__main__":
    unittest.main()
