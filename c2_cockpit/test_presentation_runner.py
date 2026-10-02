# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Presentation Runner Test Suite
Validates public interface contracts and redactions for open source release.
"""
import os
import sys
import unittest
import tempfile

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from c2_cockpit.chronos_presentation_runner import ChronosPresentationRunner

class TestPresentationRunnerPublic(unittest.TestCase):
    def setUp(self):
        self.runner = ChronosPresentationRunner(cage_code="1AHA8")

    def test_public_session_contracts(self):
        session = self.runner.initialize_session()
        self.assertEqual(session["cage_code"], "1AHA8")
        self.assertEqual(session["status"], "PUBLIC_SESSION_RUNNER_ACTIVE")
        self.assertEqual(session["data_rights"], "DFARS 252.227-7018 (GPR)")

    def test_public_queries_and_export(self):
        slide = self.runner.query_slide(1)
        self.assertEqual(slide["slide_number"], 1)
        self.assertEqual(slide["status"], "PUBLIC_SLIDE_FRAMEWORK_ACTIVE")

        rebuttal = self.runner.query_rebuttal("OBJ-01")
        self.assertEqual(rebuttal["id"], "OBJ-01")
        self.assertEqual(rebuttal["status"], "PUBLIC_REBUTTAL_CONTRACT_ACTIVE")

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            temp_path = tf.name
        try:
            out_file = self.runner.export_session_log(temp_path)
            self.assertTrue(os.path.exists(out_file))
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

if __name__ == "__main__":
    unittest.main()
