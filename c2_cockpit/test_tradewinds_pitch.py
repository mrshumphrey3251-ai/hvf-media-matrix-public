# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Tradewinds Pitch Test Suite
Validates public interface contracts and redactions for open source release.
"""
import os
import sys
import unittest
import tempfile

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from funding_engine.tradewinds_pitch_compiler import TradewindsPitchCompiler

class TestTradewindsPitchPublic(unittest.TestCase):
    def setUp(self):
        self.compiler = TradewindsPitchCompiler()

    def test_public_interface_contracts(self):
        pkg = self.compiler.compile_tradewinds_package()
        self.assertEqual(pkg["cage_code"], "1AHA8")
        self.assertEqual(pkg["status"], "PUBLIC_TRADEWINDS_INTERFACE_ACTIVE")
        self.assertEqual(pkg["data_rights"], "DFARS 252.227-7018 (GPR)")

    def test_public_file_export(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            temp_path = tf.name
        try:
            out_file = self.compiler.export_package(temp_path)
            self.assertTrue(os.path.exists(out_file))
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

if __name__ == "__main__":
    unittest.main()
