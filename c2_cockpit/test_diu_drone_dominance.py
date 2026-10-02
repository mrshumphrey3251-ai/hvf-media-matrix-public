# -*- coding: utf-8 -*-
"""
Ebony Chronos Public DIU Drone Dominance Test Suite
Sanitized Interface Contract Tests for Open Source Builds
Redacted Implementation: Proprietary unit costs and mission schemas removed.
"""
import os
import sys
import unittest
import tempfile

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from funding_engine.diu_drone_dominance_brief import DIUDroneDominanceBriefCompiler

class TestDIUDroneDominancePublic(unittest.TestCase):
    def setUp(self):
        self.compiler = DIUDroneDominanceBriefCompiler()

    def test_public_interface_contracts(self):
        brief = self.compiler.compile_solution_brief()
        self.assertEqual(brief["cage_code"], "1AHA8")
        self.assertEqual(brief["status"], "PUBLIC_BRIEF_INTERFACE_ACTIVE")
        self.assertIn("Deep Strike (20 km)", brief["mission_focus"])
        self.assertIn("Close Quarter Battle (CQB)", brief["mission_focus"])

    def test_public_file_export(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            temp_path = tf.name
        try:
            out_file = self.compiler.export_brief(temp_path)
            self.assertTrue(os.path.exists(out_file))
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

if __name__ == "__main__":
    unittest.main()
