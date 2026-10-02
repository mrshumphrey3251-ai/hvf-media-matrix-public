# -*- coding: utf-8 -*-
import os, sys, unittest, json
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path: sys.path.insert(0, REPO_ROOT)

class TestGoldenMasterCommissioningPublic(unittest.TestCase):
    def setUp(self):
        self.j = os.path.join(REPO_ROOT, "funding_engine", "CHRONOS_GOLDEN_MASTER_COMMISSIONING_REPORT.json")
        self.m = os.path.join(REPO_ROOT, "funding_engine", "CHRONOS_GOLDEN_MASTER_COMMISSIONING_REPORT.md")

    def test_public_commissioning_json(self):
        self.assertTrue(os.path.exists(self.j))
        with open(self.j, "r", encoding="utf-8-sig") as f: data = json.load(f)
        self.assertEqual(data["cage_code"], "1AHA8")
        self.assertEqual(data["commissioning_status"], "PUBLIC_GOLDEN_MASTER_ACTIVE")
        self.assertEqual(data["data_rights"], "DFARS 252.227-7018 (GPR)")

    def test_public_commissioning_markdown(self):
        self.assertTrue(os.path.exists(self.m))
        with open(self.m, "r", encoding="utf-8-sig") as f: content = f.read()
        self.assertIn("CAGE: 1AHA8", content)
        self.assertIn("[PUBLIC CONTRACT]", content)
        self.assertIn("REDACTED", content)

if __name__ == "__main__": unittest.main()
