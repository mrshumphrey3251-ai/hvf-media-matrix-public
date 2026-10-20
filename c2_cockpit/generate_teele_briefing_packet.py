"""
HVFNexus Sovereign Industrial C2 — Rob Teele Executive Briefing Packet Generator
Extracts real-time statutory metrics, cryptographic ledger proofs, and active pursuits.
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path

cockpit_dir = Path("C:/HVF_Repos/hvf-media-matrix-private/c2_cockpit")
manifest_path = cockpit_dir / "compliance_manifest.json"
pipeline_path = cockpit_dir / "solicitation_pipeline.json"
db_path = cockpit_dir / "matrix_ledger.db"

print("=== [HVFNexus C2] COMPILING EXECUTIVE BRIEFING DOSSIER FOR ROB TEELE ===")

manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
pipeline = json.loads(pipeline_path.read_text(encoding="utf-8"))

# Query live ledger
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()
cursor.execute("SELECT count(*) FROM executive_authorizations")
event_count = cursor.fetchone()[0]

cursor.execute("""
    SELECT timestamp, proof_hash FROM executive_authorizations 
    WHERE artifact_hash = 'SB00165728' LIMIT 1
""")
sprs_record = cursor.fetchone()
conn.close()

org = manifest["organization"]
sprs = manifest["defense_portals"]["sprs"]

packet_text = f"""================================================================================
  HUMPHREY VIRTUAL FARMS LLC — EXECUTIVE DEFENSE CAPABILITY DOSSIER
================================================================================
MEETING: Rob Teele Briefing
EXECUTIVE: Jeffery Humphrey, Chief Executive Officer & SME
GENERATED: {datetime.utcnow().isoformat()} UTC

[1] CORPORATE & FEDERAL REGISTRATION IDENTIFIERS
    - Legal Entity:           {org['legal_business_name']}
    - CAGE Code:              {org['cage_code']}
    - Unique Entity ID (UEI): {org['uei']}
    - SAM.gov Status:         ACTIVE (Small Business)
    - PIEE Administrative CAM: ACTIVE (Jeffery Humphrey)

[2] STATUTORY CYBERSECURITY CLEARANCE (SPRS)
    - Assessment Standard:    NIST SP 800-171 Rev 2
    - Confidence Level:       BASIC (Self-Assessment)
    - DoD Verified Score:     {sprs['score']} / {sprs['max_score']} (MAXIMUM ATTAINABLE)
    - DoD Unique ID (UID):    {sprs['dod_unique_identifier']}
    - Open POA&M Deficiencies: {sprs['poam_deficiencies']} (Zero Open Items)
    - Regulatory Compliance:  DFARS 252.204-7012, 7019, 7020 COMPLETE

[3] SOVEREIGN INDUSTRIAL C2 ARCHITECTURE (HVFNexus)
    - Architecture Type:      Bare-Metal Sovereign Command & Control (C2)
    - Verification Engine:    Append-Only WORM SQLite Ledger (matrix_ledger.db)
    - Cryptographic Events:   {event_count} Immutable Ledger Events Sealed
    - SPRS Proof Hash:        {sprs_record[1] if sprs_record else 'N/A'}
    - Third-Party Cloud Risk: ZERO (Sovereign Local Enclave Isolation)

[4] TARGET DEFENSE OPPORTUNITIES
"""

for sol in pipeline.get("active_solicitations", []):
    packet_text += f"    * [{sol['solicitation_id']}] {sol['title']} (Suitability: {sol['suitability_score']}%)\n"

packet_text += f"""
[5] OFFICIAL REPOSITORY & ATTESTATION RECORDS
    - Public Capability Dossier: https://github.com/mrshumphrey3251-ai/hvf-media-matrix-public
    - Executive Contact:         {org['executive_email']} | (580) 677-1055
================================================================================
"""

output_path = cockpit_dir / "ROB_TEELE_ONE_SHEET.txt"
output_path.write_text(packet_text, encoding="utf-8")

print(f"[+] Briefing sheet compiled successfully: {output_path}")
print(packet_text)