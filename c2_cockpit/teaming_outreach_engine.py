"""
HVFNexus Sovereign Industrial C2 — Prime Contractor Teaming Outreach Engine
Generates authoritative executive teaming solicitations for defense prime contractors.
Designed for modular expansion without refactoring core logic.
"""
import json
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path

cockpit_dir = Path("C:/hvf_c2/hvf-media-matrix-private/c2_cockpit")
manifest_path = cockpit_dir / "compliance_manifest.json"
db_path = cockpit_dir / "matrix_ledger.db"

TARGET_PRIMES = [
    {
        "prime_name": "General Dynamics Land Systems / Mission Systems",
        "sblo_contact": "Small Business Liaison Officer",
        "focus_domain": "Autonomous Industrial C2 & Edge Telemetry",
        "target_naics": "541512"
    },
    {
        "prime_name": "Lockheed Martin Rotary and Mission Systems",
        "sblo_contact": "Supplier Diversity & Small Business Advocacy",
        "focus_domain": "Sovereign Compute Enclaves & WORM Ledgers",
        "target_naics": "541519"
    }
]

def generate_teaming_package():
    print("=== [HVFNexus C2] EXECUTING PRIME TEAMING OUTREACH ENGINE ===")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    org = manifest["organization"]
    sprs = manifest["defense_portals"]["sprs"]
    ts = datetime.utcnow().isoformat()
    
    generated_files = []
    
    for prime in TARGET_PRIMES:
        prime_slug = prime["prime_name"].split()[0].upper()
        letter_filename = f"TEAMING_OUTREACH_{prime_slug}.md"
        letter_path = cockpit_dir / letter_filename
        
        content = f"""# EXECUTIVE DEFENSE TEAMING SOLICITATION

**TO:** {prime['prime_name']} — {prime['sblo_contact']}  
**FROM:** Jeffery Humphrey, Chief Executive Officer, Humphrey Virtual Farms LLC  
**DATE:** {ts[:10]}  
**SUBJECT:** Small Business Subcontracting & Teaming Partnership — CAGE: {org['cage_code']}  

---

### 1. Executive Summary & Statutory Defense Clearance
Humphrey Virtual Farms LLC is an industrial technology provider operating the sovereign Command and Control (`HVFNexus`) bare-metal architecture. We provide small business subcontracting capabilities with pre-award cybersecurity qualifications already established in the Department of Defense registry:

* **Legal Business Name:** {org['legal_business_name']}
* **CAGE Code:** `{org['cage_code']}` | **UEI:** `{org['uei']}`
* **DoD SPRS NIST SP 800-171 Score:** **{sprs['score']} / {sprs['max_score']}** (Maximum BASIC Confidence)
* **DoD Unique Identifier (UID):** `{sprs['dod_unique_identifier']}`
* **Open POA&M Deficiencies:** {sprs['poam_deficiencies']} (Zero Open Items)
* **System Security Plan:** `{sprs['ssp_document']}` (v{sprs['ssp_version']})
* **Regulatory Compliance:** Fully Compliant with DFARS 252.204-7012, 7019, and 7020

### 2. Teaming Alignment: {prime['focus_domain']}
Under NAICS **{prime['target_naics']}**, Humphrey Virtual Farms LLC provides prime contractors with:
* Deterministic, high-assurance telemetry and bare-metal edge nodes.
* Tamper-evident Write-Once-Read-Many (WORM) audit ledgers for operational and supply chain verification.
* Instant eligibility for pre-award compliance determinations without prime sponsor remediation overhead.

### 3. Executive Contact & Engagement
We invite your Small Business Program Office to review our active public teaming matrix or schedule an executive technical briefing:
* **CEO Direct Contact:** {org['executive_email']} | (580) 677-1055
* **Public Capability Dossier:** https://github.com/mrshumphrey3251-ai/hvf-media-matrix-public
"""
        letter_path.write_text(content, encoding="utf-8")
        generated_files.append(letter_filename)
        print(f"[+] Teaming solicitation package compiled: {letter_filename}")
    
    # Seal outreach generation in matrix_ledger.db
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    raw_proof = f"{ts}|{org['cage_code']}|TEAMING_OUTREACH_BATCH|{len(TARGET_PRIMES)}"
    proof_hash = hashlib.sha256(raw_proof.encode("utf-8")).hexdigest()
    
    cursor.execute("""
        INSERT INTO executive_authorizations 
        (timestamp, core, authorized_by, cage_code, uei, action, artifact_hash, proof_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (ts, "EBONY_TEAMING_ENGINE_V1", org['executive_cam'], org['cage_code'], org['uei'],
          "TEAMING_OUTREACH_COMPILED", ",".join(generated_files), proof_hash))
    
    conn.commit()
    conn.execute("PRAGMA wal_checkpoint(FULL);")
    conn.close()
    print(f"[+] Teaming outreach batch sealed in WORM ledger. Proof: {proof_hash[:16]}...")

if __name__ == "__main__":
    generate_teaming_package()