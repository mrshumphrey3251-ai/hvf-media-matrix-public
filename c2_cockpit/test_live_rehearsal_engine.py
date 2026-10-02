# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Live Rehearsal Engine Test Suite
Validates public interface contracts and redactions for open source release.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from c2_cockpit.chronos_live_rehearsal_engine import ChronosLiveRehearsalEngine

class TestLiveRehearsalEnginePublic(unittest.TestCase):
    def setUp(self):
        self.engine = ChronosLiveRehearsalEngine(cage_code="1AHA8")

    def test_public_preflight_contract(self):
        report = self.engine.execute_preflight_audit()
        self.assertEqual(report["cage_code"], "1AHA8")
        self.assertEqual(report["status"], "PUBLIC_PREFLIGHT_INTERFACE_ACTIVE")
        self.assertEqual(report["data_rights"], "DFARS 252.227-7018 (GPR)")

    def test_public_dry_run_contract(self):
        result = self.engine.execute_dry_run_rehearsal()
        self.assertEqual(result["cage_code"], "1AHA8")
        self.assertEqual(result["status"], "PUBLIC_REHEARSAL_CONTRACT_ACTIVE")

if __name__ == "__main__":
    unittest.main()
