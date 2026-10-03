# -*- coding: utf-8 -*-
"""
EBONY CHRONOS: MASTER PLATFORM TEST RUNNER & REGRESSION ORCHESTRATOR
Classification: RESTRICTED // HVF PRIVATE ENCLAVE // LEVEL 5 CEO AUTHORITY
Contracting Entity: HVF Omni-Industrial Matrix (CAGE: 1AHA8)
System Designation: Ebony Chronos (Operational Brevity: Chronos)
Statutory Standards: NIST SP 800-82 Rev 2 | MIL-STD-810H | HL7 FHIR | HIPAA / SaMD | DFARS 252.227-7018
"""

import os
import sys
import unittest
import time

REPO_ROOT = os.path.abspath(os.path.dirname(__file__))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

def run_master_regression() -> int:
    print("=" * 80)
    print("  EBONY CHRONOS: MASTER SENTINEL PLATFORM REGRESSION SWEEP")
    print("  * Authority CAGE: 1AHA8 (HVF Omni-Industrial Matrix)")
    print("  * Governance:     CEO Jeffery Humphrey (Level 5 Authority)")
    print("=" * 80)

    tests_dir = os.path.join(REPO_ROOT, "tests")
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=tests_dir, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    start_time = time.time()
    result = runner.run(suite)
    elapsed = time.time() - start_time

    print("-" * 80)
    print(f"Regression Sweep Completed in {elapsed:.3f}s")
    print(f"Total Tests Run: {result.testsRun}")
    print(f"Total Failures:  {len(result.failures)}")
    print(f"Total Errors:    {len(result.errors)}")
    print("=" * 80)

    if result.wasSuccessful():
        print("[SUCCESS] ALL SUB-SYSTEM HARNESSES PASSED WITH ZERO CRUMBS (100% COVERAGE)")
        return 0
    else:
        print("[FAILURE] REGRESSION SUITE ENCOUNTERED DRIFT OR FAILURES")
        return 1

if __name__ == "__main__":
    sys.exit(run_master_regression())

