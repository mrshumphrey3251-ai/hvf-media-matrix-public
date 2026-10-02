# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Acquisition Artifacts Test Suite
Validates existence and public schema of sanitized exported deliverables.
"""
import os
import sys
import unittest
import json

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

class TestAcquisitionArtifactsPublic(unittest.TestCase):
    def setUp(self):
        self.sbir_path = os.path.join(REPO_ROOT, "funding_engine", "CHRONOS_SBIR_PHASE_TWO_PROPOSAL.json")
        self.diu_path  = os.path.join(REPO_ROOT, "funding_engine", "DIU_DRONE_DOMINANCE_PHASE_3_SOLUTION_BRIEF.json")

    def test_public_sbir_artifact(self):
        self.assertTrue(os.path.exists(self.sbir_path), "Public SBIR proposal artifact missing")
        with open(self.sbir_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["cage_code"], "1AHA8")
        self.assertEqual(data["status"], "PUBLIC_PROPOSAL_INTERFACE_ACTIVE")

    def test_public_diu_artifact(self):
        self.assertTrue(os.path.exists(self.diu_path), "Public DIU solution brief artifact missing")
        with open(self.diu_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["cage_code"], "1AHA8")
        self.assertEqual(data["status"], "PUBLIC_BRIEF_INTERFACE_ACTIVE")

if __name__ == "__main__":
    unittest.main()
