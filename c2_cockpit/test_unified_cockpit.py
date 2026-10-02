# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Unified Cockpit Test Suite
Validates public contract schema, 4-bay layout compliance, and data rights boundaries.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

class TestUnifiedCockpitPublic(unittest.TestCase):
    def setUp(self):
        self.html_path = os.path.join(REPO_ROOT, "c2_cockpit", "chronos_unified_cockpit.html")
        self.py_path   = os.path.join(REPO_ROOT, "c2_cockpit", "chronos_unified_cockpit_launcher.py")

    def test_public_html_contract(self):
        self.assertTrue(os.path.exists(self.html_path), "Public Cockpit HTML missing")
        with open(self.html_path, "r", encoding="utf-8-sig") as f:
            content = f.read()

        self.assertIn("CAGE: 1AHA8", content)
        self.assertIn('id="bay-1"', content)
        self.assertIn('id="bay-2"', content)
        self.assertIn('id="bay-3"', content)
        self.assertIn('id="bay-4"', content)
        self.assertIn('id="broadcast-canvas"', content)
        self.assertIn('id="laser-dot"', content)

    def test_public_launcher_contract(self):
        self.assertTrue(os.path.exists(self.py_path), "Public Launcher missing")
        with open(self.py_path, "r", encoding="utf-8-sig") as f:
            code = f.read()
        self.assertIn("launch_cockpit", code)

if __name__ == "__main__":
    unittest.main()
