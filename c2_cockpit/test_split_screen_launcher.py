# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Split-Screen Launcher Test Suite
Validates public interface contracts and redactions for open source release.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from c2_cockpit.chronos_split_screen_launcher import SplitScreenBriefingLauncher

class TestSplitScreenLauncherPublic(unittest.TestCase):
    def setUp(self):
        self.launcher = SplitScreenBriefingLauncher(cage_code="1AHA8")

    def test_public_readiness_contract(self):
        readiness = self.launcher.inspect_flight_readiness()
        self.assertEqual(readiness["cage_code"], "1AHA8")
        self.assertEqual(readiness["status"], "PUBLIC_SPLIT_SCREEN_INTERFACE_ACTIVE")
        self.assertEqual(readiness["data_rights"], "DFARS 252.227-7018 (GPR)")

    def test_public_manifest_contract(self):
        manifest = self.launcher.generate_launch_manifest()
        self.assertEqual(manifest["cage_code"], "1AHA8")
        self.assertEqual(manifest["status"], "PUBLIC_LAUNCHER_CONTRACT_ACTIVE")

if __name__ == "__main__":
    unittest.main()
