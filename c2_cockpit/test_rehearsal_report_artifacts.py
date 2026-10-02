# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Rehearsal Report Test Suite
Validates existence and public contract schema of sanitized rehearsal deliverables.
"""
import os
import sys
import unittest
import json

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

class TestRehearsalReportArtifactsPublic(unittest.TestCase):
    def setUp(self):
        self.json_path = os.path.join(REPO_ROOT, "funding_engine", "OCTOBER_5_PREFLIGHT_AUDIT_REPORT.json")
        self.md_path   = os.path.join(REPO_ROOT, "funding_engine", "OCTOBER_5_DRY_RUN_REHEARSAL_CERTIFICATE.md")

    def test_public_preflight_report(self):
        self.assertTrue(os.path.exists(self.json_path), "Public pre-flight report JSON missing")
        with open(self.json_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        self.assertEqual(data["cage_code"], "1AHA8")
        self.assertEqual(data["status"], "PUBLIC_REHEARSAL_REPORT_ACTIVE")

    def test_public_rehearsal_certificate(self):
        self.assertTrue(os.path.exists(self.md_path), "Public rehearsal certificate markdown missing")
        with open(self.md_path, "r", encoding="utf-8-sig") as f:
            content = f.read()
        self.assertIn("CAGE: 1AHA8", content)
        self.assertIn("[PUBLIC CONTRACT]", content)
        self.assertIn("REDACTED", content)

if __name__ == "__main__":
    unittest.main()
