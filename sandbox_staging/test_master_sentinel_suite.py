# -*- coding: utf-8 -*-
"""
EBONY CHRONOS: MASTER SOVEREIGN REGRESSION SUITE & PLATFORM INTEGRITY AUDITOR
Classification: PUBLIC RELEASE // REVISION v8.0 // CAGE: 1AHA8
Contracting Entity: HVF Omni-Industrial Matrix (CAGE: 1AHA8)
System Designation: Ebony Chronos (Operational Brevity: Chronos)
Statutory Standards: NIST SP 800-82 Rev 2 | MIL-STD-810H | HL7 FHIR | HIPAA / SaMD | DFARS 252.227-7018
"""

import os
import sys
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

class TestMasterSentinelPlatformPublic(unittest.TestCase):
    def test_public_subsystem_interfaces_presence(self):
        required_modules = [
            "chronos_core/hal/chronos_mobile_adapter.py",
            "chronos_core/dsp/chronos_dsp_engine.py",
            "chronos_core/guardian/chronos_emergency_guardian.py",
            "chronos_core/companion/chronos_companion_engine.py",
            "chronos_core/ptsd/chronos_ptsd_deescalation.py",
            "chronos_core/mesh/chronos_mesh_network.py",
            "chronos_core/runtime/chronos_sentinel_runtime.py",
            "chronos_core/c2/chronos_c2_cockpit.py",
            "chronos_core/daemon/chronos_sentinel_daemon.py",
            "chronos_core/ui/chronos_tactical_hud.py",
            "chronos_core/system/chronos_system_orchestrator.py",
            "chronos_cli.py",
            "c2_cockpit/chronos_cockpit_app.py",
            "c2_cockpit/sentry_watchdog_daemon.py",
            "c2_cockpit/evaluator_ingress_server.py"
        ]
        for rel_path in required_modules:
            full_path = os.path.join(REPO_ROOT, rel_path)
            self.assertTrue(os.path.exists(full_path), f"Public interface file missing: {rel_path}")

    def test_public_orchestrator_contract(self):
        from chronos_core.system.chronos_system_orchestrator import ChronosSystemOrchestrator
        orchestrator = ChronosSystemOrchestrator()
        report = orchestrator.generate_system_report()
        self.assertEqual(report.operational_state, "SOVEREIGN_SYSTEM_OPERATIONAL")

if __name__ == "__main__":
    unittest.main()

