# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Evaluator Ingress Server Test Suite
Sanitized Interface Contract Tests for Open Source Builds
Redacted Implementation: Proprietary defense inquiry endpoints removed.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from c2_cockpit.evaluator_ingress_server import ChronosEvaluatorIngressServer

class TestChronosEvaluatorIngressPublic(unittest.TestCase):
    def setUp(self):
        self.server = ChronosEvaluatorIngressServer()

    def test_public_interface_contracts(self):
        self.assertTrue(self.server.start())
        self.server.stop()

if __name__ == "__main__":
    unittest.main()
