import sqlite3
import sys
from pathlib import Path

db_path = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\matrix_ledger.db")

if not db_path.exists():
    print(f"[CRITICAL ERROR] Database not found at {db_path}")
    sys.exit(1)

conn = sqlite3.connect(str(db_path))
cur = conn.cursor()

try:
    cur.execute("SELECT message_uid FROM email_dispatch_ledger LIMIT 1")
    print("[+] Column 'message_uid' already exists. Schema is compliant.")
except sqlite3.OperationalError as e:
    if "no such column: message_uid" in str(e):
        print("[MIGRATION] Target column 'message_uid' missing. Commencing non-destructive schema update...")
        try:
            # Drop UNIQUE constraint to allow insertion into populated table
            cur.execute("ALTER TABLE email_dispatch_ledger ADD COLUMN message_uid TEXT")
            conn.commit()
            print("[SUCCESS] Column 'message_uid' appended cleanly. Pre-existing records preserved.")
        except Exception as alt_err:
            print(f"[CRITICAL ERROR] Failed to alter table: {alt_err}")
            sys.exit(1)

conn.close()