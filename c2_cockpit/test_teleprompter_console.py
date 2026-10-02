# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Teleprompter Console Test Suite
Validates public interface contracts and redactions for open source release.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from c2_cockpit.briefing_teleprompter_console import BriefingTeleprompterConsole

class TestTeleprompterConsolePublic(unittest.TestCase):
    def setUp(self):
        self.console = BriefingTeleprompterConsole(cage_code="1AHA8")

    def test_public_manifest(self):
        m = self.console.get_full_presentation_manifest()
        self.assertEqual(m["cage_code"], "1AHA8")
        self.assertEqual(m["status"], "PUBLIC_TELEPROMPTER_INTERFACE_ACTIVE")
        self.assertEqual(m["data_rights"], "DFARS 252.227-7018 (GPR)")

    def test_public_render_slide(self):
        card = self.console.render_slide_card(1)
        self.assertEqual(card["slide_number"], 1)
        self.assertEqual(card["status"], "PUBLIC_SLIDE_FRAMEWORK_ACTIVE")

if __name__ == "__main__":
    unittest.main()
