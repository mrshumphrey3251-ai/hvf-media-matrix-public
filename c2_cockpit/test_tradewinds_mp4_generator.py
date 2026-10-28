# -*- coding: utf-8 -*-
"""
Unit Test Suite: Automated 1080p Full-HD Tradewinds MP4 Video & Competitor AoA Slide Renderer
"""
import tempfile
import unittest
from pathlib import Path
import sys
from PIL import Image

COCKPIT_DIR = Path(__file__).resolve().parent
if str(COCKPIT_DIR) not in sys.path:
    sys.path.insert(0, str(COCKPIT_DIR))

import generate_tradewinds_mp4_video as gtmv


class TestTradewindsMp4Generator(unittest.TestCase):
    def test_slide_specs_and_competitor_aoa_rendering(self):
        specs = gtmv.build_slide_specs()
        self.assertEqual(len(specs), 5)
        slide4_text = "\n".join(specs[3]["bullets"])
        self.assertIn("SIEMENS S7-1500", slide4_text)
        self.assertIn("DRAGOS PLATFORM", slide4_text)
        self.assertIn("TRICONEX", slide4_text)
        self.assertIn("1,360,544x", slide4_text)
        with tempfile.TemporaryDirectory() as tmp:
            png_out = Path(tmp) / "test_slide_4.png"
            gtmv.render_slide_image(specs[3], png_out)
            self.assertTrue(png_out.exists())
            with Image.open(png_out) as im:
                self.assertEqual(im.size, (1920, 1080))


if __name__ == "__main__":
    unittest.main()
