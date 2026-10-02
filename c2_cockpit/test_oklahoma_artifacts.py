# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Oklahoma Artifacts Test Suite
Validates existence and public schema of sanitized Oklahoma deliverables.
"""
import os
import sys
import unittest
import json

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

class TestOklahomaArtifactsPublic(unittest.TestCase):
    def setUp(self):
        self.json_path = os.path.join(REPO_ROOT, "funding_engine", "OKLAHOMA_DEFENSE_TRANSITION_PACKAGE.json")
        self.md_path   = os.path.join(REPO_ROOT, "funding_engine", "OKLAHOMA_DEFENSE_TRANSITION_BRIEF.md")

    def test_public_oklahoma_json(self):
        self.assertTrue(os.path.exists(self.json_path), "Public Oklahoma JSON artifact missing")
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["cage_code"], "1AHA8")
        self.assertEqual(data["status"], "PUBLIC_OKLAHOMA_INTERFACE_ACTIVE")

    def test_public_oklahoma_memo(self):
        self.assertTrue(os.path.exists(self.md_path), "Public Oklahoma memo markdown missing")
        with open(self.md_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("CAGE: 1AHA8", content)
        self.assertIn("[PUBLIC CONTRACT]", content)
        self.assertIn("REDACTED", content)

if __name__ == "__main__":
    unittest.main()
