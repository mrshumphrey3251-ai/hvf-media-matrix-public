# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Mission Operator Console Test Suite
Validates public interface contracts and redactions for open source release.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from c2_cockpit.chronos_mission_operator_console import ChronosMissionOperatorConsole

class TestMissionOperatorConsolePublic(unittest.TestCase):
    def setUp(self):
        self.console = ChronosMissionOperatorConsole(cage_code="1AHA8")

    def test_public_console_contract(self):
        status = self.console.launch_mission_console()
        self.assertEqual(status["cage_code"], "1AHA8")
        self.assertEqual(status["status"], "PUBLIC_OPERATOR_CONSOLE_ACTIVE")
        self.assertEqual(status["data_rights"], "DFARS 252.227-7018 (GPR)")

    def test_public_operations_contract(self):
        slide = self.console.advance_to_slide(1)
        self.assertEqual(slide["slide_number"], 1)

        rebuttal = self.console.retrieve_objection_rebuttal("OBJ-01")
        self.assertEqual(rebuttal["id"], "OBJ-01")

        snap = self.console.get_telemetry_snapshot()
        self.assertEqual(snap["status"], "PUBLIC_TELEMETRY_SNAPSHOT_ACTIVE")

if __name__ == "__main__":
    unittest.main()
