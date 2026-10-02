# -*- coding: utf-8 -*-
"""
Ebony Chronos Public Sentinel Daemon Test Suite
Sanitized Interface Contract Tests for Open Source Builds
Redacted Implementation: Internal RTOS timer threads and hardware locks removed.
"""
import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
for d in ["dsp", "guardian", "companion", "ptsd", "mesh", "hal", "runtime", "c2", "daemon"]:
    p = os.path.join(REPO_ROOT, "chronos_core", d)
    if p not in sys.path:
        sys.path.insert(0, p)

from chronos_sentinel_daemon import (
    ChronosSentinelDaemon, DaemonRunState, ServiceHealthStatus
)

class TestChronosSentinelDaemonPublic(unittest.TestCase):
    def setUp(self):
        self.daemon = ChronosSentinelDaemon()

    def test_public_interface_contracts(self):
        self.assertTrue(self.daemon.start_service())
        health = self.daemon.get_service_health()
        self.assertIsInstance(health, ServiceHealthStatus)
        self.assertEqual(health.run_state, "RUNNING_ACTIVE")
        self.assertTrue(self.daemon.stop_service())
        self.assertEqual(self.daemon.run_state, DaemonRunState.STOPPED)

if __name__ == "__main__":
    unittest.main()
