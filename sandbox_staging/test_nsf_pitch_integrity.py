"""
HVF Omni-Industrial Matrix | FORENSIC TEST HARNESS
Module: test_nsf_pitch_integrity.py
Protocol: 4-Gate Audit, Test, and Verify Protocol (NSF SBIR Compliance)
"""

import os
import sys
import sqlite3
import hashlib

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
PITCH_FILE = os.path.join(BASE_DIR, "proposals", "PROJECT_PITCH_NSF_SEED_FUND.md")

print("=" * 80)
print("PROJECT EBONY | NSF PROJECT PITCH FORENSIC AUDIT")
print("Authority: Jeffery Humphrey, Founder & CEO | CAGE: 1AHA8")
print("=" * 80)

passed = 0

# GATE 1: File Existence & Word Count (NSF requires strictly concise pitches < 1,500 words)
print("\n[GATE 1] AUDITING ARTIFACT PRESENCE & NSF WORD CONSTRAINTS...")
if not os.path.exists(PITCH_FILE):
    print("  [FAIL] NSF Pitch file not found on disk.")
    sys.exit(1)

with open(PITCH_FILE, "r", encoding="utf-8") as f:
    text = f.read()

word_count = len(text.split())
if word_count < 300 or word_count > 1500:
    print(f"  [FAIL] Word count violation: {word_count} words (Limit: 1,500).")
    sys.exit(1)
print(f"  [PASS] Artifact present. Word count compliant: {word_count} words (Within strict NSF limits).")
passed += 1

# GATE 2: Mandatory NSF Pitch Section Structure
print("\n[GATE 2] AUDITING NSF MANDATORY FOUR-SECTION TAXONOMY...")
required_sections = [
    "1. TECHNOLOGY INNOVATION",
    "2. TECHNICAL OBJECTIVES",
    "3. MARKET OPPORTUNITY",
    "4. COMPANY & TEAM"
]
for sec in required_sections:
    if sec not in text:
        print(f"  [FAIL] Missing mandatory NSF section: '{sec}'")
        sys.exit(1)
    print(f"  [PASS] Section verified: '{sec}'")
passed += 1

# GATE 3: Entity Authority & Technical Content
print("\n[GATE 3] AUDITING CORPORATE IDENTIFIERS & TECHNICAL SUBSTANCE...")
clauses = [
    "HVF Omni-Industrial Matrix",
    "CAGE: 1AHA8",
    "UEI: S1M4ENLHTDH5",
    "Kinetic Guillotine",
    "Three-Brain Architecture",
    "$275,000",
    "Bayh-Dole Act"
]
for c in clauses:
    if c not in text:
        print(f"  [FAIL] Missing mandatory substance clause: '{c}'")
        sys.exit(1)
    print(f"  [PASS] Verified clause: '{c}'")
passed += 1

# GATE 4: Cryptographic Ledger Digest Audit
print("\n[GATE 4] AUDITING VAULT CRYPTOGRAPHIC INTEGRITY...")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
    SELECT id, details FROM corporate_governance_log 
    WHERE action = 'NSF_PROJECT_PITCH_STAGED' 
    ORDER BY id DESC LIMIT 1
""")
row = cursor.fetchone()
conn.close()

if not row:
    print("  [FAIL] No NSF_PROJECT_PITCH_STAGED entry found in memory vault.")
    sys.exit(1)

doc_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
if doc_hash[:16] not in row[1]:
    print(f"  [FAIL] Hash mismatch! Disk: {doc_hash[:16]} vs Vault: {row[1]}")
    sys.exit(1)

print(f"  [PASS] Vault Record #{row[0]} cryptographically matches disk artifact (Hash: {doc_hash[:16]}).")
passed += 1

print("\n" + "=" * 80)
if passed == 4:
    print("[AUDIT PASSED] 100% System Coverage: All 4 Test Gates Verified.")
else:
    print(f"[AUDIT FAILED] Only {passed}/4 gates verified.")
    sys.exit(1)
print("=" * 80)

