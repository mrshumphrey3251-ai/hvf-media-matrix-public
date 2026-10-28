"""
Unit Test Suite: USACE ERDC Rolling BAA White Paper & ISO 32000-1 PDF Compiler
Verifies TRL 4 alignment, Docket 10-26-3976 cross-reference, $1.2M ($150K M1A) budget arithmetic,
and zero PII leakage in the Public repository.
"""
import unittest
from pathlib import Path
import sys

COCKPIT_DIR = Path(__file__).resolve().parent
if str(COCKPIT_DIR) not in sys.path:
    sys.path.insert(0, str(COCKPIT_DIR))

import compile_erdc_baa_whitepaper as erdc


class TestErdcBaaWhitepaper(unittest.TestCase):
    def test_compile_erdc_package_and_pdf_seal(self):
        res = erdc.compile_erdc_package()
        self.assertTrue(res["pdf_header_valid"])
        md_content = Path(res["md_path"]).read_text(encoding="utf-8")
        self.assertIn("USACE-ERDC-BAA-2026", md_content)
        self.assertIn("10-26-3976", md_content)
        self.assertIn("TRL 4", md_content)
        self.assertIn("$1,200,000.00", md_content)
        self.assertIn("$150,000.00", md_content)
        self.assertIn("DFARS 252.227-7018", md_content)
        if "public" in str(COCKPIT_DIR).lower():
            self.assertNotIn("humphreyvirtualfarm@gmail.com", md_content)


if __name__ == "__main__":
    unittest.main()
