# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Briefing Session Artifacts Test Suite
Validates existence and public contract schema of sanitized session deliverables.
"""
import os
import sys
import unittest
import json

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

class TestBriefingSessionArtifactsPublic(unittest.TestCase):
    def setUp(self):
        self.json_path = os.path.join(REPO_ROOT, "funding_engine", "OCTOBER_5_BRIEFING_SESSION_MANIFEST.json")
        self.md_path   = os.path.join(REPO_ROOT, "funding_engine", "OCTOBER_5_LIVE_BRIEFING_RUNBOOK.md")

    def test_public_session_manifest(self):
        self.assertTrue(os.path.exists(self.json_path), "Public Briefing Session Manifest JSON missing")
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["cage_code"], "1AHA8")
        self.assertEqual(data["status"], "PUBLIC_SESSION_RUNNER_ACTIVE")

    def test_public_runbook_markdown(self):
        self.assertTrue(os.path.exists(self.md_path), "Public Briefing Runbook markdown missing")
        with open(self.md_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("CAGE: 1AHA8", content)
        self.assertIn("[PUBLIC CONTRACT]", content)
        self.assertIn("REDACTED", content)

if __name__ == "__main__":
    unittest.main()
