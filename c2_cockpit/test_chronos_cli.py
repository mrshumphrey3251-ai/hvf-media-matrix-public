# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Production CLI Test Suite
Sanitized Interface Contract Tests for Open Source Builds
Redacted Implementation: Bare-metal ledger auditing logic removed.
"""
import os
import sys
import unittest
import subprocess
import json

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

class TestChronosCLIPublic(unittest.TestCase):
    def test_public_cli_contract(self):
        res = subprocess.run(
            [sys.executable, "chronos_cli.py", "--mode", "report", "--terminal", "atak"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True
        )
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data["status"], "PUBLIC_CLI_ACTIVE")
        self.assertEqual(data["mode"], "report")
        self.assertEqual(data["terminal"], "atak")

if __name__ == "__main__":
    unittest.main()
