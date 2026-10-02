# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Cockpit Dashboard Test Suite
Sanitized Interface Contract Tests for Open Source Builds
Redacted Implementation: Proprietary GUI theme shaders removed.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from c2_cockpit.chronos_cockpit_app import ChronosCockpitDashboard
from chronos_core.ui.chronos_tactical_hud import TacticalScenarioType

class TestChronosCockpitDashboardPublic(unittest.TestCase):
    def setUp(self):
        self.dashboard = ChronosCockpitDashboard()

    def test_public_interface_contracts(self):
        state = self.dashboard.fetch_live_cockpit_state(TacticalScenarioType.NOMINAL_DISMOUNTED_PATROL)
        self.assertEqual(state["status"], "PUBLIC_DASHBOARD_ACTIVE")
        self.assertIn("report", state)

if __name__ == "__main__":
    unittest.main()
