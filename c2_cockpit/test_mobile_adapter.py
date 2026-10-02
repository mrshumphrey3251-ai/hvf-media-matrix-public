# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Mobile Adapter Test Suite
Sanitized Interface Contract Tests for Open Source Builds
Redacted Implementation: Proprietary camera PPG optical transfer curves removed.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HAL_DIR = os.path.join(REPO_ROOT, "chronos_core", "hal")
if HAL_DIR not in sys.path:
    sys.path.insert(0, HAL_DIR)

from chronos_mobile_adapter import (
    ChronosMobileAdapter, MobileTerminalMode, BiometricIngressSource, MobileDeviceTelemetryFrame
)

class TestChronosMobileAdapterPublic(unittest.TestCase):
    def setUp(self):
        self.adapter = ChronosMobileAdapter()

    def test_public_interface_contracts(self):
        # 1. Frame packaging contract
        frame = self.adapter.package_mobile_frame(
            acc_xyz=(0.0, 0.0, 1.0),
            gyro_xyz=(0.0, 0.0, 0.0)
        )
        self.assertIsInstance(frame, MobileDeviceTelemetryFrame)
        self.assertEqual(frame.terminal_mode, "STANDALONE_SMARTPHONE")

        # 2. Camera PPG interface contract
        red, ir = self.adapter.ingest_phone_camera_ppg([100.0, 102.0, 104.0])
        self.assertEqual(len(red), 3)
        self.assertEqual(len(ir), 3)

if __name__ == "__main__":
    unittest.main()
