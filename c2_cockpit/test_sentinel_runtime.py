# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Master Runtime Test Suite
Sanitized Interface Contract Tests for Open Source Builds
Redacted Implementation: Internal thread scheduling and proprietary arbitration removed.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for d in ["dsp", "guardian", "companion", "ptsd", "mesh", "hal", "runtime"]:
    p = os.path.join(REPO_ROOT, "chronos_core", d)
    if p not in sys.path:
        sys.path.insert(0, p)

from chronos_sentinel_runtime import (
    ChronosSentinelRuntime, SentinelOperationalState, RuntimeTickSummary
)

class TestChronosSentinelRuntimePublic(unittest.TestCase):
    def setUp(self):
        self.runtime = ChronosSentinelRuntime()

    def test_public_interface_contracts(self):
        summary = self.runtime.execute_tick(
            ecg_window=[0.0] * 250,
            ppg_red_window=[1000.0] * 50,
            ppg_ir_window=[2000.0] * 50,
            eda_window=[3.5] * 10,
            acc_xyz=(0.0, 0.0, 1.0)
        )
        self.assertIsInstance(summary, RuntimeTickSummary)
        self.assertEqual(summary.tick_index, 1)
        self.assertEqual(summary.operational_state, "NOMINAL_ACTIVE")
        self.assertTrue(len(summary.integrity_token) > 0)

if __name__ == "__main__":
    unittest.main()
