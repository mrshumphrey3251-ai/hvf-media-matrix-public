# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Tactical HUD Simulator Test Suite
Sanitized Interface Contract Tests for Open Source Builds
Redacted Implementation: Internal simulation curves and NVG palettes removed.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from chronos_core.ui.chronos_tactical_hud import (
    ChronosTacticalHUDApp, TacticalScenarioType
)
from chronos_core.c2.chronos_c2_cockpit import HUDTelemetrySnapshot

class TestChronosTacticalHUDPublic(unittest.TestCase):
    def setUp(self):
        self.hud_app = ChronosTacticalHUDApp()

    def test_public_interface_contracts(self):
        snapshot = self.hud_app.execute_scenario_step(TacticalScenarioType.NOMINAL_DISMOUNTED_PATROL)
        self.assertEqual(snapshot.__class__.__name__, "HUDTelemetrySnapshot")
        self.assertIsInstance(snapshot, HUDTelemetrySnapshot)
        rendered = self.hud_app.render_ansi_hud(snapshot)
        self.assertTrue(len(rendered) > 0)

if __name__ == "__main__":
    unittest.main()
