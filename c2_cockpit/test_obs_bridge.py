# -*- coding: utf-8 -*-
"""
Ebony Chronos Public OBS Broadcast Bridge Contract Test Suite
"""
import os, sys, unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from c2_cockpit.chronos_obs_bridge import ChronosOBSBridge

class TestOBSBridgePublic(unittest.TestCase):
    def setUp(self):
        self.bridge = ChronosOBSBridge(
            cage_code="1AHA8",
            presenter="CEO Jeffery Humphrey"
        )

    def test_public_bridge_contract(self):
        self.assertEqual(self.bridge.cage_code, "1AHA8")
        manifest = self.bridge.generate_scene_manifest()
        self.assertEqual(manifest["name"], "Ebony_Chronos_Studio")

    def test_public_scenes(self):
        manifest = self.bridge.generate_scene_manifest()
        self.assertGreaterEqual(len(manifest["scene_order"]), 2)

if __name__ == "__main__":
    unittest.main()
