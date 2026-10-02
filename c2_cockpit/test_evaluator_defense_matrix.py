# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Evaluator Defense Matrix Test Suite
Validates public interface contracts and redactions for open source release.
"""
import os
import sys
import unittest
import tempfile

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from funding_engine.evaluator_defense_matrix import EvaluatorDefenseMatrix

class TestEvaluatorDefenseMatrixPublic(unittest.TestCase):
    def setUp(self):
        self.matrix = EvaluatorDefenseMatrix(cage_code="1AHA8")

    def test_public_matrix_contracts(self):
        data = self.matrix.get_defense_matrix()
        self.assertEqual(data["cage_code"], "1AHA8")
        self.assertEqual(data["status"], "PUBLIC_DEFENSE_MATRIX_ACTIVE")
        self.assertEqual(data["total_objection_rebuttals"], 10)
        self.assertEqual(data["data_rights"], "DFARS 252.227-7018 (GPR)")

    def test_public_matrix_export(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            temp_path = tf.name
        try:
            out_file = self.matrix.export_matrix(temp_path)
            self.assertTrue(os.path.exists(out_file))
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

if __name__ == "__main__":
    unittest.main()
