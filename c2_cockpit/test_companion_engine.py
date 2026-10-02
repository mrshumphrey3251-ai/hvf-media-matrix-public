# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Companion Engine Test Suite
Sanitized Interface Contract Tests for Open Source Builds
Redacted Implementation: Proprietary Socratic weighting functions removed.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
COMP_DIR = os.path.join(REPO_ROOT, "chronos_core", "companion")
if COMP_DIR not in sys.path:
    sys.path.insert(0, COMP_DIR)

from chronos_companion_engine import (
    ChronosCompanionEngine, ComprehensionTier, WellnessCheckType,
    SocraticAssessmentResult, WellnessDialogueResult
)

class TestChronosCompanionEnginePublic(unittest.TestCase):
    def setUp(self):
        self.engine = ChronosCompanionEngine()

    def test_public_interface_contracts(self):
        # Socratic evaluation contract
        res = self.engine.evaluate_socratic_response(
            topic="Safety Verification",
            stated_answer="Verification test payload.",
            accuracy_score=0.95,
            phasic_scr_amplitude=0.1,
            vocal_latency_sec=1.0,
            current_rmssd=40.0
        )
        self.assertIsInstance(res, SocraticAssessmentResult)
        self.assertEqual(res.comprehension_tier, ComprehensionTier.GROUNDED_MASTERY.value)

        # Wellness check contract
        well = self.engine.generate_wellness_check(current_hr_bpm=65.0, current_rmssd=42.0, current_tonic_scl=3.5)
        self.assertIsInstance(well, WellnessDialogueResult)
        self.assertEqual(well.check_type, WellnessCheckType.AUTONOMIC_RECOVERY.value)

if __name__ == "__main__":
    unittest.main()
