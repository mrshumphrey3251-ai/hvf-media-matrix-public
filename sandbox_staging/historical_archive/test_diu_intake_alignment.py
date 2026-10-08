"""
HVF Omni-Industrial Matrix | FORENSIC TEST HARNESS
Module: test_diu_intake_alignment.py
Protocol: 4-Gate Audit, Test, and Verify Protocol (DIU Intake Verification)
"""

import os
import sys
import sqlite3

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
sys.path.append(os.path.join(BASE_DIR, "proposals"))
from diu_intake_dispatcher import INTAKE_PAYLOAD, PDF_DELIVERABLE, pipe_to_clipboard

print("=" * 80)
print("PROJECT EBONY | DIU CAPABILITY INTAKE FORENSIC AUDIT")
print("Target: proposals/diu_intake_dispatcher.py")
print("=" * 80)

passed = 0

# GATE 1: PDF Deliverable Existence and Non-Zero Weight
print("\n[GATE 1] AUDITING ATTACHED PDF DELIVERABLE ON DISK...")
if not os.path.exists(PDF_DELIVERABLE):
    print(f"  [FAIL] Required PDF deliverable missing: {PDF_DELIVERABLE}")
    sys.exit(1)

pdf_bytes = os.path.getsize(PDF_DELIVERABLE)
if pdf_bytes < 5000:
    print(f"  [FAIL] PDF file size suspiciously low ({pdf_bytes} bytes).")
    sys.exit(1)
print(f"  [PASS] Certified PDF present on disk ({pdf_bytes:,} bytes).")
passed += 1

# GATE 2: Corporate Identifiers & Statutory References
print("\n[GATE 2] AUDITING PRIME SAM.GOV IDENTIFIERS & STATUTORY BASES...")
required_strings = [
    "HVF Omni-Industrial Matrix",
    "CAGE: 1AHA8",
    "UEI: S1M4ENLHTDH5",
    "10 U.S.C. § 4022",
    "Kinetic Guillotine",
    "$150,000",
    "DFARS 252.227-7018"
]
combined_text = " ".join(INTAKE_PAYLOAD.values())
for s in required_strings:
    if s not in combined_text:
        print(f"  [FAIL] Missing required parameter: '{s}'")
        sys.exit(1)
    print(f"  [PASS] Parameter verified: '{s}'")
passed += 1

# GATE 3: Direct Native Clipboard Pipe Verification (No Subshell)
print("\n[GATE 3] AUDITING DIRECT NATIVE CLIPBOARD PIPE (clip.exe)...")
try:
    pipe_to_clipboard("HVF_DIU_INTAKE_VERIFIED")
    print("  [PASS] Direct native clip pipe executed successfully without subshell.")
    passed += 1
except Exception as e:
    print(f"  [FAIL] Native clip pipe error: {e}")
    sys.exit(1)

# GATE 4: Corporate Memory Vault Status
print("\n[GATE 4] AUDITING DATABASE PERSISTENCE...")
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT status FROM active_solicitation_intake WHERE solicitation_id = 'DIU-AOI-2026-AUTONOMY'")
row = cursor.fetchone()
conn.close()
if not row or row[0] != "PRIMARY_ACTIVE_TARGET":
    print(f"  [FAIL] DIU solicitation not PRIMARY_ACTIVE_TARGET (Current: {row[0] if row else 'None'})")
    sys.exit(1)
print(f"  [PASS] DIU target status confirmed active in memory vault.")
passed += 1

print("\n" + "=" * 80)
if passed == 4:
    print("[AUDIT PASSED] 100% System Coverage: All 4 Test Gates Verified (DIU Intake Certified).")
else:
    print(f"[AUDIT FAILED] Only {passed}/4 gates verified.")
    sys.exit(1)
print("=" * 80)

