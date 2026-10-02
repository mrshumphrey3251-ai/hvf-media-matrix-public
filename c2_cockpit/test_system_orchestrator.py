# -*- coding: utf-8 -*-
"""
Ebony Chronos Public System Orchestrator Test Suite
Sanitized Interface Contract Tests for Open Source Builds
Redacted Implementation: Bare-metal hardware registers and internal security keys removed.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from chronos_core.system.chronos_system_orchestrator import (
    ChronosSystemOrchestrator, SystemPlatformReport
)

class TestChronosSystemOrchestratorPublic(unittest.TestCase):
    def setUp(self):
        self.orchestrator = ChronosSystemOrchestrator()

    def test_public_interface_contracts(self):
        res = self.orchestrator.bootstrap_platform()
        self.assertEqual(res["status"], "BOOTSTRAP_COMPLETE")

        report = self.orchestrator.generate_system_report()
        self.assertEqual(report.__class__.__name__, "SystemPlatformReport")
        self.assertIsInstance(report, SystemPlatformReport)
        self.assertEqual(report.operational_state, "SOVEREIGN_SYSTEM_OPERATIONAL")

        self.assertTrue(self.orchestrator.shutdown_platform())

if __name__ == "__main__":
    unittest.main()
