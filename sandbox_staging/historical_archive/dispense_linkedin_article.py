"""
HVF Omni-Industrial Matrix | STRATEGIC COMMUNICATIONS
Module: dispense_linkedin_article.py
Author: Jeffery Humphrey, Founder & CEO (Apex Architect)
Classification: STRATEGIC BROADCAST UTILITY | 100% SOVEREIGN PRIME
Protocol: DYNAMIC EDITORIAL DISPENSER & OS CLIPBOARD INJECTION ENGINE
"""

import os
import sys
import sqlite3
import argparse
import subprocess
from datetime import datetime

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")

parser = argparse.ArgumentParser(description="HVF Strategic Article Dispenser CLI")
parser.add_argument("--article", type=int, default=1, choices=[1, 2, 3, 4, 5], help="Article number to dispense (1-5)")
parser.add_argument("--list", action="store_true", help="List all staged articles in the pipeline")
args = parser.parse_args()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
    SELECT article_number, title, word_count, file_path, scheduled_date, status, sha256_hash 
    FROM linkedin_editorial_tracker 
    ORDER BY article_number ASC
""")
articles = cursor.fetchall()

print("=" * 85)
print("HVF Omni-Industrial Matrix | EXECUTIVE LINKEDIN EDITORIAL DISPENSER")
print("Sovereign Prime: CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | 10 U.S.C. § 4022")
print("=" * 85)
for art in articles:
    num, title, words, path, sdate, status, h = art
    active_marker = "==> [SELECTED]" if num == args.article else "   "
    print(f"{active_marker} Article 0{num} | {title[:48]:<48} | {words:,}w | {sdate} | {status}")
print("-" * 85)

# Target article execution
target_row = next((a for a in articles if a[0] == args.article), None)

if not target_row:
    print(f"[FAIL] Article 0{args.article} not found in editorial tracker.")
    conn.close()
    sys.exit(1)

num, title, words, file_path, sdate, status, h = target_row

if not os.path.exists(file_path):
    print(f"[FAIL] Physical deliverable missing at {file_path}")
    conn.close()
    sys.exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    payload = f.read()

# Pipe payload directly to Windows clipboard buffer
p = subprocess.Popen(["clip"], stdin=subprocess.PIPE)
p.communicate(payload.strip().encode("utf-8"))

# Log dispensing event to memory vault
conn.execute("""
    INSERT INTO corporate_governance_log (authority, target_entity, action, details, timestamp, status)
    VALUES (?, ?, ?, ?, ?, ?)
""", (
    "Jeffery Humphrey, CEO",
    f"LinkedIn Publication Engine (Article 0{num})",
    "ARTICLE_DISPENSED_TO_CLIPBOARD",
    f"Dispensed Article 0{num} ('{title}', {words} words, Hash: {h[:16]}) to Windows clipboard buffer.",
    datetime.now().isoformat(),
    "DISPENSED_READY_TO_PASTE"
))
conn.commit()
conn.close()

print(f"DISPENSED ARTIFACT DETAILS:")
print(f"  Article Number   : 0{num}")
print(f"  Title            : {title}")
print(f"  Word Count       : {words:,} words (High-Density White Paper)")
print(f"  Scheduled Date   : {sdate}")
print(f"  Physical File    : {file_path}")
print(f"  Digest (SHA-256) : {h[:16]}")
print(f"  Windows Buffer   : LOADED INTO CLIPBOARD")
print("-" * 85)
print(f"[SUCCESS] Article 0{num} piped to Windows clipboard buffer (Ready for Ctrl + V in LinkedIn).")
print("=" * 85)

