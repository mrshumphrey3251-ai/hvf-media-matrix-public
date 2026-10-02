# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Standby Lockdown Test Suite
Validates public demonstration launcher contract and public data rights markings.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

class TestStandbyLockdownPublic(unittest.TestCase):
    def setUp(self):
        self.bat_path = os.path.join(REPO_ROOT, "CHRONOS_LAUNCH_OCTOBER_5.bat")

    def test_public_launcher_contract(self):
        self.assertTrue(os.path.exists(self.bat_path), "Public batch launcher file missing")
        with open(self.bat_path, "r", encoding="utf-8-sig") as f:
            content = f.read()
        self.assertIn("1AHA8", content)
        self.assertIn("DFARS 252.227-7018", content)
        self.assertIn("CHRONOS_DEFENSE_QUAD_CHART.html", content)

    def test_public_redaction_boundary(self):
        with open(self.bat_path, "r", encoding="utf-8-sig") as f:
            content = f.read()
        self.assertNotIn("LEVEL_5_UNRESTRICTED", content)

if __name__ == "__main__":
    unittest.main()
