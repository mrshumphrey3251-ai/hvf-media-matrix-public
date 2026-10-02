# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Sentry Watchdog Test Suite
Sanitized Interface Contract Tests for Open Source Builds
Redacted Implementation: Automated process self-healing loops removed.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from c2_cockpit.sentry_watchdog_daemon import (
    ChronosSentryWatchdog, WatchdogAlertLevel, WatchdogStatusReport
)

class TestChronosSentryWatchdogPublic(unittest.TestCase):
    def setUp(self):
        self.watchdog = ChronosSentryWatchdog()

    def test_public_interface_contracts(self):
        report = self.watchdog.execute_watchdog_cycle()
        self.assertIsInstance(report, WatchdogStatusReport)
        self.assertEqual(report.alert_level, "GREEN_NOMINAL")
        self.assertTrue(self.watchdog.start_watchdog())
        self.assertTrue(self.watchdog.stop_watchdog())

if __name__ == "__main__":
    unittest.main()
