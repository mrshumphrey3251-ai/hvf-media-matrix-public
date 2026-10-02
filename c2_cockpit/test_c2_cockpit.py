# -*- coding: utf-8 -*-
"""
Ebony Chronos Public C2 Cockpit Test Suite
Sanitized Interface Contract Tests for Open Source Builds
Redacted Implementation: Internal NVG shaders and proprietary coordinate rendering removed.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
for d in ["dsp", "guardian", "companion", "ptsd", "mesh", "hal", "runtime", "c2"]:
    p = os.path.join(REPO_ROOT, "chronos_core", d)
    if p not in sys.path:
        sys.path.insert(0, p)

from chronos_c2_cockpit import (
    ChronosC2CockpitEngine, HUDDisplayMode, HUDTelemetrySnapshot
)

class TestChronosC2CockpitPublic(unittest.TestCase):
    def setUp(self):
        self.cockpit = ChronosC2CockpitEngine()

    def test_public_interface_contracts(self):
        snapshot = self.cockpit.generate_hud_frame()
        self.assertIsInstance(snapshot, HUDTelemetrySnapshot)
        self.assertEqual(snapshot.display_mode, "OPERATOR_TACTICAL_HUD")
        self.assertIn("heart_rate_bpm", snapshot.vitals_gauge)
        self.assertTrue(len(snapshot.integrity_token) > 0)

if __name__ == "__main__":
    unittest.main()
