# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Live Mission Dispatch Test Suite
Validates public interface contracts and redactions for open source release.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from c2_cockpit.chronos_live_mission_dispatch import ChronosLiveMissionDispatch

class TestLiveMissionDispatchPublic(unittest.TestCase):
    def setUp(self):
        self.dispatch = ChronosLiveMissionDispatch(cage_code="1AHA8")

    def test_public_dispatch_contract(self):
        status = self.dispatch.dispatch_mission_flight_deck(dry_run=True)
        self.assertEqual(status["cage_code"], "1AHA8")
        self.assertEqual(status["status"], "PUBLIC_MISSION_DISPATCH_ACTIVE")
        self.assertEqual(status["data_rights"], "DFARS 252.227-7018 (GPR)")

    def test_public_dispatch_operations(self):
        slide = self.dispatch.advance_briefing_slide(1)
        self.assertEqual(slide["slide_number"], 1)

        rebuttal = self.dispatch.execute_objection_rapid_response("OBJ-01")
        self.assertEqual(rebuttal["id"], "OBJ-01")

if __name__ == "__main__":
    unittest.main()
