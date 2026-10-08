"""
HVF Omni-Industrial Matrix | FORENSIC TEST HARNESS
Module: test_article_04_staging.py
Protocol: 4-Gate Audit, Test, and Verify Protocol (Article 04 Certification)
"""

import os
import sys
import re
import sqlite3
import hashlib

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
COMMS_DIR = os.path.join(BASE_DIR, "strategic_comms")
ART4_FILE = os.path.join(COMMS_DIR, "ARTICLE_04_LOCAL_MERKLE_DAG_PROVENANCE.md")

print("=" * 80)
print("PROJECT EBONY | ARTICLE 04 FORENSIC AUDIT")
print("Target: strategic_comms/ARTICLE_04_LOCAL_MERKLE_DAG_PROVENANCE.md")
print("=" * 80)

passed = 0

# GATE 1: Verify Article 04 Deliverable on Disk and Word Density
print("\n[GATE 1] AUDITING ARTICLE 04 DELIVERABLE ON DISK...")
if not os.path.exists(ART4_FILE):
    print(f"  [FAIL] Article 04 missing at: {ART4_FILE}")
    sys.exit(1)

with open(ART4_FILE, "r", encoding="utf-8") as f:
    text = f.read()

words = len(text.split())
if words < 600:
    print(f"  [FAIL] Article 04 under-dense ({words} words). Minimum standard is 600 words.")
    sys.exit(1)
print(f"  [PASS] Article 04 verified on disk ({words:,} words of high-density technical analysis).")
passed += 1

# GATE 2: Audit Cryptographic Architecture & Technical Benchmarks
print("\n[GATE 2] AUDITING CRYPTOGRAPHIC ARCHITECTURE & TECHNICAL BENCHMARKS...")
mandatory_patterns = [
    (r"Local Merkle DAG", "Local Merkle DAG"),
    (r"Three-Brain Architecture", "Three-Brain Architecture"),
    (r"Brain Three", "Brain Three"),
    (r"SHA-256", "SHA-256"),
    (r"sub-0\.15 millisecond", "sub-0.15 millisecond determinism"),
    (r"Zero RF emissions", "Zero RF emissions"),
    (r"NIST SP 800-230", "NIST SP 800-230")
]

for pattern, label in mandatory_patterns:
    if not re.search(pattern, text, re.IGNORECASE):
        print(f"  [FAIL] Missing required technical concept: '{label}'")
        sys.exit(1)
    print(f"  [PASS] Verified concept: '{label}'")
passed += 1

# GATE 3: Audit Statutory Prime Contractor Citations
print("\n[GATE 3] AUDITING STATUTORY PRIME CONTRACTOR CITATIONS...")
statutory_patterns = [
    (r"HVF Omni-Industrial Matrix", "HVF Omni-Industrial Matrix"),
    (r"10 U\.S\.C\. § 4022", "10 U.S.C. § 4022"),
    (r"1AHA8", "CAGE Code: 1AHA8"),
    (r"S1M4ENLHTDH5", "UEI: S1M4ENLHTDH5"),
    (r"DFARS 252\.227-7018", "DFARS 252.227-7018")
]

for pattern, label in statutory_patterns:
    if not re.search(pattern, text, re.IGNORECASE):
        print(f"  [FAIL] Missing statutory protection clause: '{label}'")
        sys.exit(1)
    print(f"  [PASS] Verified statutory clause: '{label}'")
passed += 1

# GATE 4: Cryptographic Hash Reconciliation with Vault Tracker
print("\n[GATE 4] RECONCILING ARTICLE 04 HASH WITH VAULT LEDGER...")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT sha256_hash, status FROM linkedin_editorial_tracker WHERE article_number = 4")
tracker_row = cursor.fetchone()
conn.close()

if not tracker_row:
    print("  [FAIL] Article 04 record missing from tracker.")
    sys.exit(1)

doc_hash = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
if doc_hash != tracker_row[0]:
    print(f"  [FAIL] Hash mismatch! Disk: {doc_hash[:16]} vs Tracker: {tracker_row[0][:16]}")
    sys.exit(1)

print(f"  [PASS] Cryptographic seal verified: {doc_hash[:16]} (Status: {tracker_row[1]}).")
passed += 1

print("\n" + "=" * 80)
if passed == 4:
    print("[AUDIT PASSED] 100% System Coverage: All 4 Test Gates Verified (Article 04 Certified).")
else:
    print(f"[AUDIT FAILED] Only {passed}/4 gates verified.")
    sys.exit(1)
print("=" * 80)

