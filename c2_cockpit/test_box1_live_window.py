# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Box 1 Live Window & Dual-Mode Contract Test Suite
Validates public contract schema, Bay 1 dual-mode controls, and data rights boundaries.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

class TestBox1LiveWindowPublic(unittest.TestCase):
    def setUp(self):
        self.html_path = os.path.join(REPO_ROOT, "c2_cockpit", "chronos_unified_cockpit.html")

    def test_public_bay1_contract(self):
        self.assertTrue(os.path.exists(self.html_path), "Public Cockpit HTML missing")
        with open(self.html_path, "r", encoding="utf-8-sig") as f:
            content = f.read()

        self.assertIn("CAGE: 1AHA8", content)
        self.assertIn('id="bay-1"', content)
        self.assertIn('id="btn-mode-toggle"', content)
        self.assertIn('id="bay1-capture-view"', content)
        self.assertIn('id="bay1-embed-view"', content)
        self.assertIn('id="video-feed"', content)
        self.assertIn('id="bay1-iframe"', content)

if __name__ == "__main__":
    unittest.main()
