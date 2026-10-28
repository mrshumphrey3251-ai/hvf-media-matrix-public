"""
HUMPHREY VIRTUAL FARMS LLC // USACE ERDC ROLLING BAA WHITE PAPER & PDF COMPILER
Solicitation Target: USACE-ERDC-BAA-2026 (U.S. Army Engineer Research & Development Center)
Prime Identifiers: CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | Active Tradewinds Docket: 10-26-3976 (TRL 4)
Statutory Framework: 10 U.S.C. Section 4022 | FAR 35.016 (Broad Agency Announcement) | DFARS 252.227-7018
"""
import hashlib
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

COCKPIT_DIR = Path(__file__).resolve().parent
REPO_ROOT = COCKPIT_DIR.parent
IS_PUBLIC = "public" in str(REPO_ROOT).lower()

if str(COCKPIT_DIR) not in sys.path:
    sys.path.insert(0, str(COCKPIT_DIR))

import hvf_pdf_engine as hpe


def generate_erdc_whitepaper_markdown(is_public: bool = IS_PUBLIC) -> str:
    contact_email = "[REDACTED-FOR-PUBLIC-RELEASE]" if is_public else "humphreyvirtualfarm@gmail.com"
    return f"""# U.S. ARMY ENGINEER RESEARCH AND DEVELOPMENT CENTER (ERDC) // ROLLING BAA WHITE PAPER
## DETERMINISTIC THREE-BRAIN TELEMETRY, NON-DESTRUCTIVE STRUCTURAL DIAGNOSTICS (STR-01/PAV-01), AND AIR-GAPPED WORM PROVENANCE FOR CONTESTED CIVIL & MILITARY INFRASTRUCTURE
**Solicitation Identifier:** `USACE-ERDC-BAA-2026` (FAR 35.016 Basic & Applied Research / 10 U.S.C. Section 4022)
**Submitting Prime Contractor:** Humphrey Virtual Farms LLC (100% Sovereign Small Business Prime)
**Corporate Identifiers:** `CAGE: 1AHA8` | `UEI: S1M4ENLHTDH5` | **Cross-Referenced DoD CDAO Docket:** `10-26-3976`
**Principal Investigator & Apex Architect:** Jeffery Humphrey, Founder, President & CEO (`{contact_email}`)
**Current Technology Readiness Level:** `TRL 4` (Laboratory Software Emulation Testbed & Mathematical Proof-of-Concept)
**Proposed Funding & Period of Performance:** `$1,200,000.00` Total (`12 Months` | `$0.00` Cash Match Required | `$150,000.00` M1A Mobilization)
**Intellectual Property & Data Rights:** 100% Small Business Background IP Retained under `DFARS 252.227-7018` (Government Purpose Rights)

---

## 1. EXECUTIVE SUMMARY & ERDC LABORATORY ALIGNMENT
Humphrey Virtual Farms LLC (`CAGE: 1AHA8` | `UEI: S1M4ENLHTDH5`) submits this Executive Technical White Paper to the **U.S. Army Engineer Research and Development Center (ERDC)** targeting the **Geotechnical and Structures Laboratory (GSL)**, **Coastal and Hydraulics Laboratory (CHL)**, and **Information Technology Laboratory (ITL)** research areas.

**Project Ebony (v8.0.0)** solves civil and military infrastructure telemetry vulnerabilities through an air-gapped, zero-cloud **Three-Brain Software Emulation Testbed (`TRL 4`)** operating at `100%` local loopback (`127.0.0.1` | `0%` external cloud dependency), backed by **`84 / 84` passing automated unit and stress test suites**, **`17 / 17` blocked adversarial red-team penetration vectors**, and **`1,420` verified civil/structural engineering assessment modules** (`STR-01`, `PAV-01`, `ENV-01`, `AUT-01`).

---

## 2. PROPOSED 12-MONTH PHASE-1 RESEARCH & PROTOTYPE MILESTONE SCHEDULE ($1,200,000.00)
* **M1A: Kickoff & Mobilization (Day 15-30):** `$150,000.00`
* **M2: TRL 5 Benchtop Integration (Month 4):** `$350,000.00`
* **M3: TRL 6 Field Emulation (Month 8):** `$400,000.00`
* **M4: Final ERDC Dossier & Audit (Month 12):** `$300,000.00`
* **TOTAL PROPOSED AWARD:** `$1,200,000.00` (`0%` Cash Match)
"""


def generate_erdc_clean_pdf_text(is_public: bool = IS_PUBLIC) -> str:
    contact_email = "[REDACTED-FOR-PUBLIC-RELEASE]" if is_public else "humphreyvirtualfarm@gmail.com"
    lines = [
        "U.S. ARMY ENGINEER RESEARCH AND DEVELOPMENT CENTER (ERDC) // ROLLING BAA WHITE PAPER",
        "TITLE: DETERMINISTIC THREE-BRAIN TELEMETRY, NON-DESTRUCTIVE STRUCTURAL DIAGNOSTICS",
        "       (STR-01/PAV-01), AND AIR-GAPPED WORM PROVENANCE FOR CIVIL & MILITARY INFRASTRUCTURE",
        "--------------------------------------------------------------------------------------------",
        "SOLICITATION IDENTIFIER : USACE-ERDC-BAA-2026 (FAR 35.016 / 10 U.S.C. Section 4022)",
        "SUBMITTING PRIME        : Humphrey Virtual Farms LLC (100% Sovereign Small Business Prime)",
        "CORPORATE IDENTIFIERS   : CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | DoD CDAO Docket: 10-26-3976",
        f"PRINCIPAL INVESTIGATOR  : Jeffery Humphrey, Founder, President & CEO ({contact_email})",
        "CURRENT READINESS LEVEL : TRL 4 (Laboratory Software Emulation Testbed & Math Proof-of-Concept)",
        "PROPOSED FUNDING SCOPE  : $1,200,000.00 Total (12 Months | $0.00 Cash Match | $150,000.00 M1A)",
        "INTELLECTUAL PROPERTY   : 100% Small Business Background IP Retained under DFARS 252.227-7018",
        "--------------------------------------------------------------------------------------------",
        "",
        "SECTION 1. EXECUTIVE SUMMARY & ERDC LABORATORY ALIGNMENT (GSL / CHL / ITL)",
        "",
        "Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5) submits this Technical White",
        "Paper to the U.S. Army Engineer Research and Development Center (ERDC) targeting the",
        "Geotechnical and Structures Laboratory (GSL), Coastal and Hydraulics Laboratory (CHL),",
        "and Information Technology Laboratory (ITL) research portfolios.",
        "",
        "Modern civil works, navigation locks, flood-control dams, tactical airfields, and highway",
        "bridges face an acute dual operational vulnerability:",
        "  1. Cloud-Dependent SCADA & Inspection Fragility under EMI or bandwidth denial.",
        "  2. Unverified Structural & Hydrological Sensor Provenance at the tactical edge.",
        "",
        "Project Ebony (v8.0.0) resolves both vulnerabilities through an air-gapped, zero-cloud",
        "Three-Brain Software Emulation Testbed (TRL 4) operating at 100% local loopback (127.0.0.1",
        "with 0% external cloud dependency), verified across 84 / 84 passing automated unit and",
        "stress test suites, 17 / 17 blocked adversarial red-team penetration vectors, and 1,420",
        "verified civil and structural engineering assessment modules (STR-01, PAV-01, ENV-01).",
        "",
        "--------------------------------------------------------------------------------------------",
        "SECTION 2. THREE-BRAIN ARCHITECTURAL SPECIFICATION (TRL 4 SOFTWARE EMULATION TESTBED)",
        "--------------------------------------------------------------------------------------------",
        "  A. BRAIN ONE - DETERMINISTIC SAFETY & ACTUATION INTERLOCK ENGINE:",
        "     SPICE and mathematical model targeting a 36.75ns physical analog MOSFET cutoff",
        "     (Kinetic Guillotine at 28.5W / 24V DC) to sever compromised actuation buses.",
        "  B. BRAIN TWO - AIR-GAPPED STRUCTURAL & PAVEMENT DIAGNOSTIC ENGINE (STR-01/PAV-01/ENV-01):",
        "     Processes NDE bridge metrics (23 CFR 650), ASTM D6433 PCI pavement deductions, and",
        "     hydraulic flow anomalies locally with zero internet connectivity.",
        "  C. BRAIN THREE - BARE-METAL SQLITE WORM & SHA-256 MERKLE DAG VAULT:",
        "     Seals every sensor frame and command into 52 verified WORM SQLite tables.",
        "",
        "--------------------------------------------------------------------------------------------",
        "SECTION 3. PROPOSED 12-MONTH PHASE-1 MILESTONE SCHEDULE ($1,200,000.00 | ZERO CASH MATCH)",
        "--------------------------------------------------------------------------------------------",
        "  * M1A: Kickoff & Mobilization (Day 15-30)  :  $150,000.00 (Edge Nodes & NDE Sensor Rig)",
        "  * M2 : TRL 5 Bench Integration (Month 4)   :  $350,000.00 (36.75ns Guillotine PCB & HIL)",
        "  * M3 : TRL 6 Field Emulation (Month 8)     :  $400,000.00 (Closed-Loop STR-01/PAV-01/ENV-01)",
        "  * M4 : Final ERDC Dossier & Audit (Mo 12)  :  $300,000.00 (TRL 6/7 Package & WORM Binder)",
        "  * TOTAL PROPOSED PHASE-1 BAA ALLOCATION    : $1,200,000.00 (100% Non-Dilutive / $0 Match)",
    ]
    return "\n".join(lines)


def compile_erdc_package() -> dict:
    prop_dir = COCKPIT_DIR / "proposals"
    prop_dir.mkdir(parents=True, exist_ok=True)

    md_text = generate_erdc_whitepaper_markdown(is_public=IS_PUBLIC)
    md_path = prop_dir / "WHITE_PAPER_USACE_ERDC_BAA_2026.md"
    md_path.write_text(md_text, encoding="utf-8")

    pdf_clean_text = generate_erdc_clean_pdf_text(is_public=IS_PUBLIC)
    pdf_artifact = hpe.HVFSovereignPDFEngine().compile_sovereign_pdf(
        "USACE-ERDC-BAA-2026 // HVF TRL 4 WHITE PAPER (CAGE 1AHA8)",
        pdf_clean_text
    )
    pdf_path = prop_dir / "USACE_ERDC_BAA_2026_WHITE_PAPER_HVF.pdf"
    pdf_path.write_bytes(pdf_artifact.pdf_bytes)

    md_sha256 = hashlib.sha256(md_path.read_bytes()).hexdigest()
    pdf_sha256 = hashlib.sha256(pdf_path.read_bytes()).hexdigest()

    if not IS_PUBLIC:
        db_path = COCKPIT_DIR / "hvf_memory_vault.db"
        if db_path.exists():
            conn = sqlite3.connect(str(db_path))
            conn.execute(
                "UPDATE active_solicitation_intake SET status = ?, last_scanned = ? WHERE solicitation_id = ?",
                ("WHITE_PAPER_SEALED_READY_FOR_TPOC", datetime.now(timezone.utc).isoformat(), "USACE-ERDC-BAA-2026")
            )
            conn.commit()
            conn.close()

    return {
        "solicitation_id": "USACE-ERDC-BAA-2026",
        "md_path": str(md_path),
        "pdf_path": str(pdf_path),
        "md_sha256": md_sha256,
        "pdf_sha256": pdf_sha256,
        "pdf_header_valid": pdf_artifact.pdf_bytes.startswith(b"%PDF-1.4"),
        "pdf_page_count": pdf_artifact.page_count,
    }


if __name__ == "__main__":
    res = compile_erdc_package()
    print(f"[CLEAN ERDC PDF SEALED] Pages: {res['pdf_page_count']} | SHA-256: {res['pdf_sha256'][:16]}...")
