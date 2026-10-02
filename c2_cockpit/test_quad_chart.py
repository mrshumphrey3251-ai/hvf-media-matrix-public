# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Defense Quad Chart Test Suite
Validates existence, sanitized public specification, and HTML delivery contract.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

class TestQuadChartPublic(unittest.TestCase):
    def setUp(self):
        self.md_path   = os.path.join(REPO_ROOT, "CHRONOS_DEFENSE_QUAD_CHART.md")
        self.html_path = os.path.join(REPO_ROOT, "CHRONOS_DEFENSE_QUAD_CHART.html")

    def test_public_quad_chart_markdown(self):
        self.assertTrue(os.path.exists(self.md_path), "Public quad chart markdown missing")
        with open(self.md_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("CAGE: 1AHA8", content)
        self.assertIn("PUBLIC RELEASE", content)

    def test_public_quad_chart_html(self):
        self.assertTrue(os.path.exists(self.html_path), "Public quad chart HTML missing")
        with open(self.html_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("<!DOCTYPE html>", content)
        self.assertIn("1AHA8", content)

if __name__ == "__main__":
    unittest.main()