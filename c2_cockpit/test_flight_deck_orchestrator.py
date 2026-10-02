# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Flight Deck Orchestrator Test Suite
Validates public interface contracts and redactions for open source release.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from c2_cockpit.chronos_flight_deck_orchestrator import ChronosFlightDeckOrchestrator

class TestFlightDeckOrchestratorPublic(unittest.TestCase):
    def setUp(self):
        self.orchestrator = ChronosFlightDeckOrchestrator(cage_code="1AHA8")

    def test_public_cockpit_contract(self):
        status = self.orchestrator.initialize_mission_cockpit()
        self.assertEqual(status["cage_code"], "1AHA8")
        self.assertEqual(status["status"], "PUBLIC_FLIGHT_DECK_INTERFACE_ACTIVE")
        self.assertEqual(status["data_rights"], "DFARS 252.227-7018 (GPR)")

    def test_public_ingress_and_operations(self):
        ingress = self.orchestrator.check_evaluator_ingress_stream()
        self.assertEqual(ingress["cage_code"], "1AHA8")
        self.assertEqual(ingress["status"], "PUBLIC_INGRESS_MONITOR_ACTIVE")

        slide = self.orchestrator.execute_slide_navigation(1)
        self.assertEqual(slide["slide_number"], 1)

        rebuttal = self.orchestrator.execute_objection_counter("OBJ-01")
        self.assertEqual(rebuttal["id"], "OBJ-01")

if __name__ == "__main__":
    unittest.main()
