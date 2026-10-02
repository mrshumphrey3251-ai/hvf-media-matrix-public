# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Native Win32 C2 Orchestrator Contract Test Suite
Validates Win32 C2 orchestrator interface schema and statutory data rights boundaries.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from c2_cockpit.chronos_native_c2_orchestrator import ChronosNativeC2Orchestrator

class TestNativeC2OrchestratorPublic(unittest.TestCase):
    def setUp(self):
        self.orchestrator = ChronosNativeC2Orchestrator(
            cage_code="1AHA8",
            presenter="CEO Jeffery Humphrey"
        )

    def test_public_quadrant_contract(self):
        geom = self.orchestrator.get_quadrant_geometry()
        for key in ["Q1_TOP_LEFT", "Q2_BOTTOM_LEFT", "Q3_TOP_RIGHT", "Q4_BOTTOM_RIGHT"]:
            self.assertIn(key, geom)
            coords = geom[key]
            self.assertEqual(len(coords), 4)

if __name__ == "__main__":
    unittest.main()
