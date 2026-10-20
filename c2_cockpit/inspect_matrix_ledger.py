import sqlite3
from pathlib import Path

db = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\matrix_ledger.db")

print("\n" + "=" * 86)
print("     LIVE WORM LEDGER VERIFICATION // C2 COCKPIT DATABASE AUDIT")
print("=" * 86)

if not db.exists():
    print("[CRITICAL] matrix_ledger.db not found at target path.")
else:
    conn = sqlite3.connect(str(db))
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cur.fetchall()]
    print(f"[ACTIVE TABLES] {tables}")

    if "audit_ledger" in tables:
        cur.execute("SELECT count(*) FROM audit_ledger")
        count = cur.fetchone()[0]
        print(f"[AUDIT RECORDS] Total committed attestations: {count}")
        cur.execute("SELECT timestamp, role, content FROM audit_ledger ORDER BY timestamp DESC LIMIT 1")
        row = cur.fetchone()
        if row:
            print(f"  - Latest Attestation: [{row[0][:19]} UTC] ({row[1]})")
            print(f"    Payload: {row[2][:100]}...")

    if "email_dispatch_ledger" in tables:
        cur.execute("SELECT count(*) FROM email_dispatch_ledger")
        e_count = cur.fetchone()[0]
        print(f"[EMAIL RECORDS] Total logged dispatches: {e_count}")
        cur.execute("SELECT timestamp, recipient, subject, status FROM email_dispatch_ledger ORDER BY timestamp DESC LIMIT 1")
        e_row = cur.fetchone()
        if e_row:
            print(f"  - Latest Dispatch: [{e_row[0][:19]} UTC] To: {e_row[1]}")
            print(f"    Subject: {e_row[2]} (Status: {e_row[3]})")

    print("=" * 86)
    conn.close()