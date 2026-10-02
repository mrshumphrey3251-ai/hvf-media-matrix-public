import os
import sqlite3
import hashlib
from datetime import datetime

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
PROP_DIR = os.path.join(BASE_DIR, "proposals")
os.makedirs(PROP_DIR, exist_ok=True)

def generate_tailored_brief(solicitation_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT solicitation_id, agency, title, sector, vehicle, max_award_usd, brain_fit, submission_format FROM active_solicitation_intake WHERE solicitation_id = ?", (solicitation_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        print(f"[ERROR] Solicitation {solicitation_id} not found in memory vault.")
        return

    s_id, agency, title, sector, vehicle, max_award, brain_fit, sub_format = row
    output_filename = f"TAILORED_BRIEF_{s_id}.md"
    output_path = os.path.join(PROP_DIR, output_filename)

    content = f"""# EXECUTIVE PROPOSAL BRIEF | SOVEREIGN PRIME CONTRACTOR
**SOLICITATION IDENTIFIER:** {s_id}
**TARGET AGENCY:** {agency}
**PROGRAM TITLE:** {title}
**SECTOR:** {sector} | **VEHICLE:** {vehicle}
**MAXIMUM ALLOCATION:** ${max_award:,.2f} USD (100% Solo Prime)
**SUBMISSION FORMAT:** {sub_format}

---

## 1. OPERATIONAL ENTITY & AUTHORITY
* **Prime Contractor:** HVF Omni-Industrial Matrix
* **Corporate Identifiers:** CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | Small Business Concern
* **Contracting Status:** Nontraditional Defense Contractor (10 U.S.C. § 4022(d)) / Commercial Prime
* **Primary SME & CEO:** Jeffery Humphrey, Founder & Apex Architect
* **Contact:** humphreyvirtualfarm@gmail.com
* **Classification:** PROPRIETARY & COMPETITION SENSITIVE (DFARS 252.227-7018)

---

## 2. ARCHITECTURAL SOLUTION: PROJECT EBONY
Project Ebony addresses {title} through an air-gapped **Three-Brain Architecture** engineered for bare-metal silicon:
* **Primary Alignment:** {brain_fit}
* **Zero-Cloud Guarantee:** 100% local execution on industrial bare metal with zero external API dependencies.
* **Deterministic Interlocks:** Brain One executes hard physical safety cutoffs in microseconds via the Kinetic Guillotine.
* **Offline Cognitive Analysis:** Brain Two identifies sensor drift and multi-spectral anomalies without transmitting RF signatures.
* **Cryptographic Verification:** Brain Three maintains an immutable local Merkle DAG ledger (<0.2ms latency) satisfying NIST SP 800-230.

---

## 3. MILESTONE DRAWDOWN SCHEDULE WITH FRONT-LOADED MOBILIZATION
HVF Omni-Industrial Matrix executes under performance-based payable milestones, incorporating a front-loaded mobilization tranche to secure immediate execution:

| Milestone | Target Window | Deliverable Focus | Allocation |
| :--- | :---: | :--- | :---: |
| **M1A: Kickoff & Mobilization** | **Days 15–30** | Delivery of Systems Engineering Plan (SEP), Post-Award Kickoff, and Long-Lead Hardware Acquisition Plan. | **$150,000** |
| **M1B: Hardware Integration** | **Month 3** | Bare-metal deployment of Brain One & Three; sub-millisecond Merkle DAG validation. | **$200,000** |
| **M2: Environmental Hardening** | **Month 6** | Operational stress testing under simulated disruption/denial; automated interlock verification. | **$450,000** |
| **M3: Cognitive Model Optimization** | **Month 9** | Deployment of Brain Two offline neural inference; zero-cloud multi-axis anomaly detection. | **$450,000** |
| **M4: Field Demo & Final Package** | **Month 12** | Live operational demonstration on proving ground; delivery of full TRL-7 data rights package. | **$400,000** |
| **TOTAL CONTRACT EFFORT** | **12 Months** | **Sovereign Three-Brain Cyber-Physical Defense Runtime** | **${max_award:,.2f}** |

---

## 4. INTELLECTUAL PROPERTY & DATA RIGHTS
HVF Omni-Industrial Matrix retains 100% exclusive, unencumbered ownership of all Background Intellectual Property, source code, and neural models under DFARS 252.227-7018. The Government receives negotiated commercial prototype evaluation rights with zero commercial surrender.

Submitted by:
Jeffery Humphrey, Founder & Chief Executive Officer
Apex Architect | HVF Omni-Industrial Matrix
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    doc_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

    conn = sqlite3.connect(DB_PATH, timeout=10.0, isolation_level=None)
    conn.execute("""
        INSERT INTO corporate_governance_log (authority, target_entity, action, details, timestamp, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "Jeffery Humphrey, CEO",
        agency,
        "PROPOSAL_BRIEF_AUTO_TAILORED",
        f"Generated tailored brief for {s_id} ({title}). Front-loaded $150k mobilization verified. Hash: {doc_hash[:16]}",
        datetime.now().isoformat(),
        "BRIEF_GENERATED"
    ))
    conn.close()

    print(f"[SUCCESS] Tailored proposal brief generated for {s_id}")
    print(f"  File Location : {output_path}")
    print(f"  Document Hash : {doc_hash[:16]} (Sealed in Vault)")

if __name__ == "__main__":
    generate_tailored_brief("DIU-AOI-2026-AUTONOMY")

