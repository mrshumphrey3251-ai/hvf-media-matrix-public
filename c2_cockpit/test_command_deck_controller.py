# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Command Deck Controller Test Suite
Validates public interface contracts and redactions for open source release.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from c2_cockpit.chronos_command_deck_controller import ChronosCommandDeckController

class TestCommandDeckControllerPublic(unittest.TestCase):
    def setUp(self):
        self.controller = ChronosCommandDeckController(cage_code="1AHA8")

    def test_public_deck_contract(self):
        status = self.controller.initialize_command_deck()
        self.assertEqual(status["cage_code"], "1AHA8")
        self.assertEqual(status["status"], "PUBLIC_COMMAND_DECK_INTERFACE_ACTIVE")
        self.assertEqual(status["data_rights"], "DFARS 252.227-7018 (GPR)")

    def test_public_live_operations(self):
        slide = self.controller.execute_live_slide_advance(1)
        self.assertEqual(slide["slide_number"], 1)
        self.assertEqual(slide["status"], "PUBLIC_SLIDE_FRAMEWORK_ACTIVE")

        rebuttal = self.controller.execute_rebuttal_lookup("OBJ-01")
        self.assertEqual(rebuttal["id"], "OBJ-01")
        self.assertEqual(rebuttal["status"], "PUBLIC_REBUTTAL_CONTRACT_ACTIVE")

if __name__ == "__main__":
    unittest.main()
