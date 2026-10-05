import os
import sys
import sqlite3

# ==============================================================================
# HVF Omni-Industrial Matrix | SIMULATED ARTIFACT PURGE UTILITY
# Authority: Jeffery Humphrey, Founder & CEO (CAGE: 1AHA8, UEI: S1M4ENLHTDH5)
# System: Complete Eradication of Synthetic AFWERX Data from Memory Vault
# ==============================================================================

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")

print("=" * 80)
print("PURGING ALL SIMULATED AFWERX RECORDS FROM SOVEREIGN VAULT")
print("=" * 80)

if not os.path.exists(DB_PATH):
    print(f"[FAIL] Database not found at: {DB_PATH}")
    sys.exit(1)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# 1. Audit and Delete Simulated Dispatches
cur.execute("""
SELECT id, sender_address, subject FROM staged_email_dispatches 
WHERE sender_address LIKE '%afwerx%' 
   OR recipient_address LIKE '%afwerx%' 
   OR subject LIKE '%AFWERX%' 
   OR raw_body_sanitized LIKE '%AFWERX%'
""")
dispatches_to_purge = cur.fetchall()

if dispatches_to_purge:
    print(f"[INFO] Found {len(dispatches_to_purge)} simulated AFWERX dispatch records:")
    for d in dispatches_to_purge:
        print(f"  * ID #{d[0]} | Sender: {d[1]} | Subject: {d[2]}")
    
    cur.execute("""
    DELETE FROM staged_email_dispatches 
    WHERE sender_address LIKE '%afwerx%' 
       OR recipient_address LIKE '%afwerx%' 
       OR subject LIKE '%AFWERX%' 
       OR raw_body_sanitized LIKE '%AFWERX%'
    """)
    print(f"[SUCCESS] Purged {len(dispatches_to_purge)} records from staged_email_dispatches.")
else:
    print("[INFO] No simulated AFWERX records found in staged_email_dispatches.")

# 2. Audit and Scrub Directives or Notes
cur.execute("""
DELETE FROM ceo_directives 
WHERE directive LIKE '%AFWERX%'
""")
print("[SUCCESS] Cleared any synthetic AFWERX references from ceo_directives.")

conn.commit()

# 3. Final Verification
cur.execute("SELECT COUNT(*) FROM staged_email_dispatches WHERE raw_body_sanitized LIKE '%AFWERX%'")
remaining = cur.fetchone()[0]
conn.close()

print("=" * 80)
print(f"STATUS: PURGE COMPLETE. REMAINING SIMULATED AFWERX RECORDS: {remaining}")
print("=" * 80)
