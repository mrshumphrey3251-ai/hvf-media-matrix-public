"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: DIU COMPANY INTEREST PAYLOAD
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    """

    HVF Omni-Industrial Matrix | SOVEREIGN PRIME SYSTEMS

    Module: diu_company_interest_payload.py

    Author: Jeffery Humphrey, Founder & CEO (Apex Architect)

    Classification: PROPRIETARY & CONFIDENTIAL | 100% UNENCUMBERED PRIME

    Protocol: DIU COMMERCIAL INTEREST WEBFORM INGESTION & SUBMISSION

    """



    import os

    import sys

    import sqlite3

    import subprocess

    import webbrowser

    from datetime import datetime



    BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"

    DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")

    PDF_FILE = os.path.join(BASE_DIR, "proposals", "DIU_SOLUTION_BRIEF_PROJECT_EBONY_HVF.pdf")

    FORM_URL = "https://www.diu.mil/work-with-us/company-interest"



    # Calibrated strictly to DIU webform bounds (300-char max technical field)

    PITCH_300 = "HVF is a nontraditional prime submitting Project Ebony: an air-gapped Three-Brain SCADA & edge autonomy defense runtime. Features sub-us Kinetic Guillotine physical cutoffs and sub-ms Merkle DAG telemetry provenance (10 U.S.C. 4022 Prototype OT; CAGE: 1AHA8; UEI: S1M4ENLHTDH5)."



    FORM_FIELDS = [

        ("First Name", "Jeffery"),

        ("Last Name", "Humphrey"),

        ("Email Address", "[LOCAL_ARCHIVE_ONLY: C:\HVF_Repos\Archive]"),

        ("Company Name", "HVF Omni-Industrial Matrix"),

        ("Company Website", "https://github.com/hvf-media-matrix-public"),

        ("UEI Number", "S1M4ENLHTDH5"),

        ("Street Address", "PO Box / Prototyping Laboratory"),

        ("City", "Oklahoma City"),

        ("Postal Code", "73101"),

        ("Subsidiary Status", "No (100% Independent Sovereign Prime)"),

        ("Technology Readiness Level", "TRL 7 - System prototype demonstration in operational environment"),

        ("DIU Portfolio Alignment", "Autonomous Warfare / AI"),

        ("Technical Summary (300 Chars Max)", PITCH_300),

        ("5-Page Solution Brief Deliverable Path", PDF_FILE)

    ]



    def pipe_to_clipboard(text: str):

        p = subprocess.Popen(["clip"], stdin=subprocess.PIPE)

        p.communicate(text.strip().encode("utf-8"))



    def log_interest_dispatch(field_name: str):

        conn = sqlite3.connect(DB_PATH, timeout=10.0, isolation_level=None)

        conn.execute("""

            INSERT INTO corporate_governance_log (authority, target_entity, action, details, timestamp, status)

            VALUES (?, ?, ?, ?, ?, ?)

        """, (

            "Jeffery Humphrey, CEO",

            "Defense Innovation Unit (DIU)",

            "DIU_COMPANY_INTEREST_FIELD_DISPATCHED",

            f"Injected field '{field_name}' into clipboard buffer for DIU Commercial Intake.",

            datetime.now().isoformat(),

            "FIELD_DISPATCHED"

        ))

        conn.close()



    def main():

        print("=" * 80)

        print("HVF Omni-Industrial Matrix | DIU COMPANY INTEREST INTAKE DISPENSER")

        print("Target: https://www.diu.mil/work-with-us/company-interest")

        print("Prime CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | Authority: Jeffery Humphrey, CEO")

        print("=" * 80)

        print(f"Technical Summary Character Count: {len(PITCH_300)} / 300 chars (COMPLIANT)")

        print("-" * 80)



        print("\n[STEP 1] Launching DIU Company Interest Intake Portal in default browser...")

        webbrowser.open(FORM_URL)



        for label, val in FORM_FIELDS:

            print("\n" + "-" * 80)

            input(f">>> Press [ENTER] to copy [{label}] to Clipboard... ")

            pipe_to_clipboard(val)

            log_interest_dispatch(label)

            print(f"  [COPIED] {label}: {val}")

            print("  --> Click into the corresponding webform field and press [Ctrl + V].")



        print("\n" + "=" * 80)

        print("[FINAL SUBMISSION CONFIRMATION]")

        print("In your browser, confirm all required fields are filled, verify the selections:")

        print("  - Subsidiary: No")

        print("  - TRL Level: TRL 7")

        print("  - Portfolio: Autonomous Warfare")

        print("Then click 'Submit' on the DIU form.")

        print("=" * 80)



        confirm = input("\nHave you clicked 'Submit' on the DIU form? (y/n): ").strip().lower()

        if confirm == 'y':

            conn = sqlite3.connect(DB_PATH, timeout=10.0, isolation_level=None)

            conn.execute("""

                INSERT INTO corporate_governance_log (authority, target_entity, action, details, timestamp, status)

                VALUES (?, ?, ?, ?, ?, ?)

            """, (

                "Jeffery Humphrey, CEO",

                "Defense Innovation Unit (DIU)",

                "DIU_COMPANY_INTEREST_SUBMISSION_COMPLETED",

                "Officially transmitted Company Interest intake package to DIU Autonomous Warfare portfolio. 100% Solo Prime.",

                datetime.now().isoformat(),

                "INTEREST_PACKAGE_TRANSMITTED"

            ))

            conn.close()

            print("\n[SUCCESS] DIU Company Interest Submission officially recorded and sealed in vault.")

        else:

            print("\n[INFO] Session left open. Re-run script when ready to finalize submission recording.")



    if __name__ == "__main__":

        main()




if __name__ == "__main__":
    render()
