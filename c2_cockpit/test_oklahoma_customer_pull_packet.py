#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Test Suite: Stage 8G Oklahoma DoD & USACE Tulsa District Customer-Pull Packet Compiler
"""
import sys
import unittest
from pathlib import Path

COCKPIT_DIR = Path(__file__).resolve().parent
if str(COCKPIT_DIR) not in sys.path:
    sys.path.insert(0, str(COCKPIT_DIR))

import compile_oklahoma_customer_pull_packet as ok_pull


class TestOklahomaCustomerPullPacket(unittest.TestCase):
    def test_compile_oklahoma_pull_package_and_1page_seal(self) -> None:
        res = ok_pull.compile_oklahoma_pull_package()
        self.assertTrue(res["pdf_header_valid"])
        self.assertTrue(res["page_count_marker"])
        md_content = Path(res["md_path"]).read_text(encoding="utf-8")
        pdf_text = ok_pull.generate_oklahoma_clean_pdf_text()
        self.assertNotIn("**", pdf_text)
        self.assertNotIn("`", pdf_text)
        for token in ["10-26-4046", "#0126", "#0069", "#0008", "#0005", "Tinker", "McAlester", "Tulsa District", "TRL 4", "$1,200,000.00", "$150,000.00", "DFARS 252.227-7018"]:
            self.assertIn(token, md_content)
        if "public" in str(COCKPIT_DIR).lower():
            self.assertNotIn("humphreyvirtualfarm@gmail.com", md_content)
            self.assertNotIn("humphreyvirtualfarm@gmail.com", pdf_text)


if __name__ == "__main__":
    unittest.main()
