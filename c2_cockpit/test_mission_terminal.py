# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Mission Terminal Test Suite
Validates public interface contracts and redactions for open source release.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from c2_cockpit.chronos_mission_terminal import ChronosMissionTerminal

class TestMissionTerminalPublic(unittest.TestCase):
    def setUp(self):
        self.terminal = ChronosMissionTerminal(cage_code="1AHA8")

    def test_public_posture_contract(self):
        posture = self.terminal.get_system_posture()
        self.assertEqual(posture["cage_code"], "1AHA8")
        self.assertEqual(posture["status"], "PUBLIC_MISSION_TERMINAL_ACTIVE")
        self.assertEqual(posture["data_rights"], "DFARS 252.227-7018 (GPR)")

    def test_public_queries_contract(self):
        slide = self.terminal.query_slide_card(1)
        self.assertEqual(slide["slide_number"], 1)
        self.assertEqual(slide["status"], "PUBLIC_SLIDE_FRAMEWORK_ACTIVE")

        rebuttal = self.terminal.query_objection_counter("OBJ-01")
        self.assertEqual(rebuttal["id"], "OBJ-01")

if __name__ == "__main__":
    unittest.main()
