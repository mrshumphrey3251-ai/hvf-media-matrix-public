# -*- coding: utf-8 -*-
"""
Ebony Chronos Public DSP Test Suite
Sanitized Interface Contract Tests for Open Source Builds
Redacted Implementation: Proprietary filter weights and calibration curves removed.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DSP_DIR = os.path.join(REPO_ROOT, "chronos_core", "dsp")
if DSP_DIR not in sys.path:
    sys.path.insert(0, DSP_DIR)

from chronos_dsp_engine import (
    ChronosDSPEngine, ECGAnalysisResult, PPGAnalysisResult, EDAResult, MotionStateResult
)

class TestChronosDSPEnginePublic(unittest.TestCase):
    def setUp(self):
        self.engine = ChronosDSPEngine()

    def test_public_interface_contracts(self):
        ecg_res = self.engine.process_ecg([0.0] * 500)
        self.assertIsInstance(ecg_res, ECGAnalysisResult)
        self.assertEqual(ecg_res.heart_rate_bpm, 72.0)

        ppg_res = self.engine.process_ppg([0.0] * 100, [0.0] * 100)
        self.assertIsInstance(ppg_res, PPGAnalysisResult)
        self.assertEqual(ppg_res.spo2_percentage, 98.0)

        eda_res = self.engine.process_eda([0.0] * 50)
        self.assertIsInstance(eda_res, EDAResult)
        self.assertEqual(eda_res.tonic_scl_us, 4.0)

        mot_res = self.engine.process_motion(0.0, 0.0, 1.0)
        self.assertIsInstance(mot_res, MotionStateResult)
        self.assertEqual(mot_res.gait_state, "STATIONARY")

if __name__ == "__main__":
    unittest.main()
