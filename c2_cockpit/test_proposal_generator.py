# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Proposal Generator Test Suite
Sanitized Interface Contract Tests for Open Source Builds
Redacted Implementation: Proprietary WBS budgets and IP strategy removed.
"""
import os
import sys
import unittest
import tempfile

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from funding_engine.chronos_proposal_generator import ChronosProposalGenerator

class TestChronosProposalGeneratorPublic(unittest.TestCase):
    def setUp(self):
        self.generator = ChronosProposalGenerator()

    def test_public_interface_contracts(self):
        proposal = self.generator.generate_sbir_direct_phase_two_proposal()
        self.assertEqual(proposal["cage_code"], "1AHA8")
        self.assertEqual(proposal["status"], "PUBLIC_PROPOSAL_INTERFACE_ACTIVE")

    def test_public_file_export(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            temp_path = tf.name
        try:
            out_file = self.generator.export_proposal(temp_path)
            self.assertTrue(os.path.exists(out_file))
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

if __name__ == "__main__":
    unittest.main()
