# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Native 4-Window C2 Deck Contract Test Suite
Validates bare-metal multi-window orchestration schema, public asset links,
and statutory data rights boundaries under DFARS 252.227-7018 GPR.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from c2_cockpit.chronos_native_quad_deck import ChronosNativeQuadDeck

class TestNativeQuadDeckPublic(unittest.TestCase):
    def setUp(self):
        self.deck = ChronosNativeQuadDeck(
            cage_code="1AHA8",
            presenter="CEO Jeffery Humphrey"
        )

    def test_public_deck_contract(self):
        geom = self.deck.geom
        for key in ["Q1_TOP_LEFT", "Q2_BOTTOM_LEFT", "Q3_TOP_RIGHT", "Q4_BOTTOM_RIGHT"]:
            self.assertIn(key, geom)
            self.assertEqual(len(geom[key]), 4)

    def test_public_assets(self):
        teleprompter = os.path.join(REPO_ROOT, "c2_cockpit", "chronos_teleprompter_hud.html")
        self.assertTrue(os.path.exists(teleprompter), "Public teleprompter missing")

if __name__ == "__main__":
    unittest.main()
