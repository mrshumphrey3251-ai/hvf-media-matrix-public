"""
HVFNexus Sovereign Industrial C2 — Hardcopy Executive Binder Exporter
Verifies the HTML executive packet, seals compilation in WORM ledger, and launches system viewer.
"""
import webbrowser
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path

cockpit_dir = Path("C:/HVF_Repos/hvf-media-matrix-private/c2_cockpit")
packet_path = cockpit_dir / "HVF_EXECUTIVE_MEETING_PACKET.html"
db_path = cockpit_dir / "matrix_ledger.db"

print("=== [HVFNexus C2] HARDCOPY EXECUTIVE BINDER EXPORT ENGINE ===")

if not packet_path.exists():
    raise FileNotFoundError(f"Packet missing at {packet_path}")

file_size = packet_path.stat().st_size
file_sha256 = hashlib.sha256(packet_path.read_bytes()).hexdigest()
ts = datetime.utcnow().isoformat()

print(f"[+] Verified Executive Packet Artifact: {packet_path.name} ({file_size} bytes)")
print(f"[+] Artifact SHA-256: {file_sha256}")

# Seal export event in WORM ledger
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()
cursor.execute("""
    INSERT INTO executive_authorizations 
    (timestamp, core, authorized_by, cage_code, uei, action, artifact_hash, proof_hash)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (ts, "EBONY_BINDER_ENGINE_V1", "CEO Jeffery Humphrey", "1AHA8", "S1M4ENLHTDH5",
      "EXECUTIVE_BINDER_EXPORTED", packet_path.name, file_sha256))

conn.commit()
conn.execute("PRAGMA wal_checkpoint(FULL);")
conn.close()

print(f"[+] Physical binder generation permanently recorded in matrix_ledger.db.")
print(f"[+] Launching packet in system browser for printing/PDF export...")
webbrowser.open(packet_path.as_uri())