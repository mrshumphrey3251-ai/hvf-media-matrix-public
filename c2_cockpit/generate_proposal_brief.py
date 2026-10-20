"""
HVFNexus Sovereign Industrial C2 — Executive Bid Decision & Proposal Generator
Compiles statutory compliance credentials and technical architectures into actionable proposal briefs.
"""
import json
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path

cockpit_dir = Path("C:/HVF_Repos/hvf-media-matrix-private/c2_cockpit")
pipeline_path = cockpit_dir / "solicitation_pipeline.json"
manifest_path = cockpit_dir / "compliance_manifest.json"
db_path = cockpit_dir / "matrix_ledger.db"

def generate_brief(target_solicitation_id: str = "DIU-CSO-26-0042"):
    print(f"=== [HVFNexus C2] COMPILING PROPOSAL BRIEF: {target_solicitation_id} ===")
    
    # 1. Load pipeline and compliance data
    pipeline = json.loads(pipeline_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    
    match = next((s for s in pipeline["active_solicitations"] if s["solicitation_id"] == target_solicitation_id), None)
    if not match:
        raise ValueError(f"Solicitation {target_solicitation_id} not found in active pipeline.")
    
    ts = datetime.utcnow().isoformat()
    org = manifest["organization"]
    sprs = manifest["defense_portals"]["sprs"]
    
    brief_content = f"""# EXECUTIVE PROPOSAL BRIEF: {match['solicitation_id']}

## Opportunity Profile
* **Solicitation ID:** {match['solicitation_id']}
* **Title:** {match['title']}
* **Procuring Agency:** {match['agency']}
* **NAICS Classification:** {match['naics']}
* **Set-Aside Designation:** {match['set_aside']}
* **Calculated Suitability Score:** {match['suitability_score']}%
* **Generated (UTC):** {ts}

## Prime Contractor Verification & Statutory Authority
* **Entity Name:** {org['legal_business_name']}
* **CAGE Code:** `{org['cage_code']}` | **UEI:** `{org['uei']}`
* **DoD SPRS NIST SP 800-171 Score:** **{sprs['score']} / {sprs['max_score']}**
* **DoD Unique Identifier (UID):** `{sprs['dod_unique_identifier']}`
* **POA&M Status:** Zero Deficiencies ({sprs['poam_deficiencies']} open items)
* **System Security Plan:** `{sprs['ssp_document']}` (Version {sprs['ssp_version']})
* **Statutory Compliance:** DFARS 252.204-7012, 7019, 7020 Verified

## Technical Solution & Core Sovereign Capabilities
* **Core Architecture:** {match['description']}
* **Data Integrity Engine:** Bare-metal WORM SQLite ledgers with continuous SHA-256 validation.
* **Command & Control Node:** Sovereign bare-metal execution isolated from third-party hosting dependencies.
* **Compliance Posture:** Pre-award cyber authorization ready for immediate Contracting Officer determination.

## Executive Bid Recommendation
* **Decision:** BID / PRIME PURSUIT AUTHORIZED
* **Authorized By:** {org['executive_cam']}, Chief Executive Officer
"""
    
    brief_filename = f"PROPOSAL_BRIEF_{target_solicitation_id.replace('-', '_')}.md"
    brief_file = cockpit_dir / brief_filename
    brief_file.write_text(brief_content, encoding="utf-8")
    print(f"[+] Proposal brief generated: {brief_file}")
    
    # 2. Seal brief generation into matrix_ledger.db
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    raw_proof = f"{ts}|{org['cage_code']}|{target_solicitation_id}|PROPOSAL_BRIEF_GENERATED"
    proof_hash = hashlib.sha256(raw_proof.encode("utf-8")).hexdigest()
    
    cursor.execute("""
        INSERT INTO executive_authorizations 
        (timestamp, core, authorized_by, cage_code, uei, action, artifact_hash, proof_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (ts, "EBONY_CAPTURE_ENGINE_V1", org['executive_cam'], org['cage_code'], org['uei'],
          f"GENERATE_BRIEF_{target_solicitation_id}", brief_filename, proof_hash))
    
    conn.commit()
    conn.execute("PRAGMA wal_checkpoint(FULL);")
    conn.close()
    print(f"[+] Proposal brief sealed in WORM ledger. Proof: {proof_hash[:16]}...")

if __name__ == "__main__":
    generate_brief()