import sqlite3
import os
import sys

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")

print("=" * 80)
print("UPGRADING HVF MEMORY VAULT TO WRITE-AHEAD LOGGING (WAL)")
print("=" * 80)

if not os.path.exists(DB_PATH):
    print(f"[FAIL] Database not found at: {DB_PATH}")
    sys.exit(1)

try:
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    cur = conn.cursor()
    
    # Enable WAL mode so concurrent reads and writes never block
    cur.execute("PRAGMA journal_mode = WAL;")
    mode = cur.fetchone()[0]
    
    cur.execute("PRAGMA synchronous = NORMAL;")
    cur.execute("PRAGMA busy_timeout = 30000;")
    cur.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    conn.commit()
    conn.close()
    
    print(f"[SUCCESS] Journal mode set to: [{mode.upper()}]")
    print("[SUCCESS] Synchronous set to NORMAL, busy_timeout set to 30,000ms.")
    print("=" * 80)
except Exception as e:
    print(f"[FAIL] Could not enable WAL mode: {e}")
    sys.exit(1)
