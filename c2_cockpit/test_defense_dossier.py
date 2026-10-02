# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Defense Dossier Test Suite
Sanitized Interface Contract Tests for Open Source Builds
Redacted Implementation: Proprietary defense telemetry and payload hashes removed.
"""
import os
import sys
import unittest
import tempfile

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from chronos_defense_dossier import ChronosDefenseDossierExporter

class TestChronosDefenseDossierPublic(unittest.TestCase):
    def setUp(self):
        self.exporter = ChronosDefenseDossierExporter()

    def test_public_interface_contracts(self):
        dossier = self.exporter.compile_dossier()
        self.assertEqual(dossier["cage_code"], "1AHA8")
        self.assertEqual(dossier["status"], "PUBLIC_EVALUATION_DOSSIER_ACTIVE")
        self.assertIn("statutory_standards", dossier)

    def test_public_file_export(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            temp_path = tf.name
        try:
            out_file = self.exporter.export_dossier_file(temp_path)
            self.assertTrue(os.path.exists(out_file))
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

if __name__ == "__main__":
    unittest.main()
