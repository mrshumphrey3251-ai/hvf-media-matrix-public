import sqlite3
import hashlib
from datetime import datetime, timezone
from pathlib import Path

base_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private")
zip_path = Path(r"C:\hvf_c2\releases\ebony_client_rob_teel.zip")
target_db = base_dir / "matrix_ledger.db"

if not zip_path.exists():
    print(f"[CRITICAL ERROR] Archive not found: {zip_path}")
    exit(1)

sha256_hash = hashlib.sha256(zip_path.read_bytes()).hexdigest()

conn = sqlite3.connect(str(target_db))
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS client_release_dockets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient TEXT NOT NULL,
    package_name TEXT NOT NULL,
    sha256_checksum TEXT NOT NULL,
    license_tier TEXT NOT NULL,
    max_nodes INTEGER NOT NULL,
    pilot_days INTEGER NOT NULL,
    delivery_timestamp_utc TEXT NOT NULL,
    statutory_authority TEXT NOT NULL,
    cage_code TEXT NOT NULL
)
""")

cur.execute("""
INSERT INTO client_release_dockets (
    recipient, package_name, sha256_checksum, license_tier, max_nodes, pilot_days, delivery_timestamp_utc, statutory_authority, cage_code
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "Rob Teel",
    "ebony_client_rob_teel.zip",
    sha256_hash,
    "TIER_COMMAND (Tier 1 & 1.5 Pilot)",
    3,
    7,
    datetime.now(timezone.utc).isoformat(),
    "Oklahoma Title 61 & OK HB 2992",
    "1AHA8"
))

conn.commit()
conn.close()

print(f"[+] Recorded client release docket into: {target_db.name}")
print(f"[*] Package:   {zip_path.name}")
print(f"[*] SHA-256:   {sha256_hash}")
print(f"[*] Recipient: Rob Teel (Tier 1 & 1.5 Sovereign Pilot | 3 Authorized Nodes)")