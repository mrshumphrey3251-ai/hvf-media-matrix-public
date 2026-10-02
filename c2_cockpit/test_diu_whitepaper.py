# -*- coding: utf-8 -*-
"""
Ebony Chronos Public DIU Whitepaper Test Suite
Validates public contract and redaction boundaries of the public executive brief.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from funding_engine.generate_diu_whitepaper import generate_diu_whitepaper_public

class TestDIUWhitepaperPublic(unittest.TestCase):
    def setUp(self):
        self.md_path = os.path.join(REPO_ROOT, "funding_engine", "DIU_PHASE_3_SOLUTION_BRIEF.md")

    def test_public_whitepaper_contracts(self):
        self.assertTrue(os.path.exists(self.md_path), "Public DIU whitepaper markdown file missing")
        with open(self.md_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        self.assertIn("CAGE: 1AHA8", content)
        self.assertIn("[PUBLIC INTERFACE]", content)
        self.assertIn("PUBLIC_RELEASE_SPECIFICATION_ACTIVE", content)
        self.assertIn("REDACTED", content)
        self.assertIn("DFARS 252.227-7018", content)

    def test_public_whitepaper_regeneration(self):
        out = generate_diu_whitepaper_public()
        self.assertTrue(os.path.exists(out))
        self.assertEqual(out, self.md_path)

if __name__ == "__main__":
    unittest.main()
