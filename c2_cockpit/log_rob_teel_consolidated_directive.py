import sqlite3
import json
from datetime import datetime, timezone
from pathlib import Path

base_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private")
db_paths = [
    base_dir / "matrix_ledger.db",
    base_dir / "c2_cockpit" / "matrix_ledger.db"
]

target_db = None
for p in db_paths:
    if p.exists():
        target_db = p
        break

if not target_db:
    target_db = base_dir / "matrix_ledger.db"

conn = sqlite3.connect(str(target_db))
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS outward_dispatches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient TEXT NOT NULL,
    subject TEXT NOT NULL,
    dispatch_type TEXT NOT NULL,
    cage_code TEXT NOT NULL,
    statutory_authority TEXT NOT NULL,
    contractor_status TEXT NOT NULL,
    grant_submission_status TEXT NOT NULL,
    named_grants TEXT NOT NULL,
    timestamp_utc TEXT NOT NULL
)
""")

named_grants_payload = json.dumps([
    "Oklahoma State Energy Program (SEP) Clean Energy & Microgrid Modernization Grant",
    "USDA Rural Energy for America Program (REAP) Renewable Infrastructure Grant",
    "OCAST Applied Research UAS Grant",
    "USDA NIFA SBIR Phase I UAS Precision Agriculture Grant"
])

cur.execute("""
INSERT INTO outward_dispatches (
    recipient, subject, dispatch_type, cage_code, statutory_authority, contractor_status, grant_submission_status, named_grants, timestamp_utc
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "Rob Teel",
    "E.B.O.N.Y. Deployment Directive // Operational Enclave Certification, State Contractor Standing & Targeted Energy/UAS Grant Submissions",
    "CONSOLIDATED_EXECUTIVE_DIRECTIVE",
    "1AHA8",
    "Oklahoma Title 61 & OK HB 2992",
    "EXECUTING_STATE_CONTRACTOR_REGISTRATION_TODAY",
    "SUBMITTING_PRIOR_TO_NEXT_WEEK_CONVENING",
    named_grants_payload,
    datetime.now(timezone.utc).isoformat()
))

conn.commit()
conn.close()

print(f"[+] Successfully logged Consolidated Executive Directive into: {target_db.name}")