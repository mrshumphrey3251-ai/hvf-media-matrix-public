"""
HVF Omni-Industrial Matrix | SOVEREIGN PRIME SYSTEMS
Module: diu_intake_dispatcher.py
Author: Jeffery Humphrey, Founder & CEO (Apex Architect)
Classification: PROPRIETARY & CONFIDENTIAL | 100% UNENCUMBERED PRIME
Protocol: DIU DIRECT COMMERCIAL CAPABILITY & SOLUTION BRIEF INTAKE
"""

import os
import sys
import sqlite3
import subprocess
import webbrowser
from datetime import datetime

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
PROP_DIR = os.path.join(BASE_DIR, "proposals")
PDF_DELIVERABLE = os.path.join(PROP_DIR, "DIU_SOLUTION_BRIEF_PROJECT_EBONY_HVF.pdf")
DIU_CONNECT_URL = "https://www.diu.mil/work-with-us/company-interest"

INTAKE_PAYLOAD = {
    "COMPANY_INFO": (
        "HVF Omni-Industrial Matrix\n"
        "CAGE: 1AHA8 | UEI: S1M4ENLHTDH5\n"
        "Contracting Status: Nontraditional Defense Contractor (10 U.S.C. § 4022(d))\n"
        "Point of Contact: Jeffery Humphrey, Founder & CEO (Apex Architect)\n"
        "Email: humphreyvirtualfarm@gmail.com\n"
        "Location: Oklahoma, USA"
    ),
    "PORTFOLIO_ALIGNMENT": "Autonomy & Energy / Cyber (Contested Logistics & Edge Autonomy Resiliency)",
    "DUAL_USE_CAPABILITY": (
        "Project Ebony is a sovereign, zero-cloud cyber-physical defense architecture engineered for "
        "bare-metal industrial controllers and autonomous edge platforms operating in heavily contested "
        "electronic warfare (EW) environments. It decouples physical actuation, cognitive anomaly detection, "
        "and cryptographic provenance across an air-gapped Three-Brain Architecture:\n"
        "1. Brain One (Controller): Deterministic SCADA with the 'Kinetic Guillotine'—a physical interlock "
        "severing actuator power circuits in <1.0 microsecond upon boundary breach, immune to software override.\n"
        "2. Brain Two (Analyst): Zero-cloud edge neural inference identifying multi-spectral drift and sensor "
        "spoofing without emitting RF signatures or querying external clouds.\n"
        "3. Brain Three (Arbiter): Sub-millisecond (<0.2ms) local SHA-256 Merkle DAG logging providing an "
        "unalterable audit trail compliant with NIST SP 800-230.\n\n"
        "Commercial Track: Secures municipal water utilities, vertical farming CEA, and microgrids against nation-state kinetic sabotage."
    ),
    "PROTOTYPE_PROPOSAL": (
        "Vehicle: 10 U.S.C. § 4022 Prototype Other Transaction ($1,650,000 USD).\n"
        "Execution Structure: Performance-based milestone schedule featuring a front-loaded $150,000 Day 15-30 "
        "Kickoff & Mobilization tranche (M1A) for long-lead hardware fabrication and bench staging.\n"
        "Data Rights: 100% small-business Background IP retention under DFARS 252.227-7018."
    ),
    "ATTACHMENT_PATH": PDF_DELIVERABLE
}

def pipe_to_clipboard(text: str):
    p = subprocess.Popen(["clip"], stdin=subprocess.PIPE)
    p.communicate(text.strip().encode("utf-8"))

def log_dispatch(field_name: str):
    conn = sqlite3.connect(DB_PATH, timeout=10.0, isolation_level=None)
    conn.execute("""
        INSERT INTO corporate_governance_log (authority, target_entity, action, details, timestamp, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "Jeffery Humphrey, CEO",
        "Defense Innovation Unit (DIU)",
        "DIU_INTAKE_FIELD_DISPATCHED",
        f"Injected field '{field_name}' into clipboard for DIU Commercial Intake portal.",
        datetime.now().isoformat(),
        "CLIPBOARD_DISPATCHED"
    ))
    conn.close()

def main():
    print("=" * 80)
    print("HVF Omni-Industrial Matrix | DIU COMMERCIAL CAPABILITY DISPATCHER")
    print("Prime CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | 10 U.S.C. § 4022 Prototype OT")
    print("=" * 80)
    print("\n[STEP 1/5] Launching DIU Company Interest Intake Portal...")
    webbrowser.open(DIU_CONNECT_URL)

    fields = [
        ("COMPANY_INFO", "Company Profile & SAM Identifiers"),
        ("PORTFOLIO_ALIGNMENT", "DIU Focus Area / Portfolio Selection"),
        ("DUAL_USE_CAPABILITY", "Core Commercial Technology & Autonomous Architecture"),
        ("PROTOTYPE_PROPOSAL", "Prototype OT Request & $150K Mobilization Tranche")
    ]

    for key, label in fields:
        print("\n" + "-" * 80)
        input(f">>> Press [ENTER] to copy {label} to Clipboard... ")
        pipe_to_clipboard(INTAKE_PAYLOAD[key])
        log_dispatch(key)
        print(f"  [COPIED] {label} loaded into Windows clipboard.")
        print(f"  --> Paste into corresponding portal field using [Ctrl + V].")

    print("\n" + "-" * 80)
    print(">>> ATTACHMENT DELIVERABLE PATH:")
    print(f"  [PDF]: {PDF_DELIVERABLE}")
    input(">>> Press [ENTER] to copy file path to Clipboard for file-upload dialog... ")
    pipe_to_clipboard(PDF_DELIVERABLE)
    print("  [COPIED] File path loaded into clipboard. Paste into file upload box.")

    print("\n" + "=" * 80)
    confirm = input("\nHave you completed and submitted the DIU Intake Form? (y/n): ").strip().lower()
    if confirm == 'y':
        ref_id = input("Enter DIU Submission Confirmation / Reference Number (or press ENTER): ").strip()
        if not ref_id:
            ref_id = "DIU-DIRECT-INTAKE-CONFIRMED"

        conn = sqlite3.connect(DB_PATH, timeout=10.0, isolation_level=None)
        conn.execute("""
            INSERT INTO corporate_governance_log (authority, target_entity, action, details, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Jeffery Humphrey, CEO",
            "Defense Innovation Unit (DIU)",
            "DIU_DIRECT_CAPABILITY_INTAKE_SUBMITTED",
            f"Submitted direct capability package and 5-page brief PDF to DIU Autonomy Portfolio. Ref: {ref_id}",
            datetime.now().isoformat(),
            "CAPABILITY_PACKAGE_TRANSMITTED"
        ))
        conn.close()
        print(f"\n[SUCCESS] DIU Direct Capability Submission sealed in vault (Ref: {ref_id}).")
    else:
        print("\n[INFO] Session open. Re-run script when submission is finalized.")

if __name__ == "__main__":
    main()

