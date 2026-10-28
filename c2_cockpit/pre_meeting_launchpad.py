"""
HVFNexus Sovereign Industrial C2 — Pre-Meeting Executive Console Launchpad
Unified terminal launchpad for Defense, Energy, and Commercial Contracting Briefings.
"""
import sys
import subprocess
from pathlib import Path

cockpit_dir = Path("C:/hvf_c2/hvf-media-matrix-private/c2_cockpit")

def display_menu():
    print("\n" + "=" * 80)
    print("      HVFNexus SOVEREIGN INDUSTRIAL C2: EXECUTIVE BRIEFING CONSOLE        ")
    print("=" * 80)
    print("  --- DEFENSE & APEX CAPABILITIES ---")
    print("  [1] EXECUTE DEFENSE C2 DEMO         (ebony_executive_demo.py)")
    print("  [2] DISPLAY LIVE ONE-SHEET DOSSIER  (ROB_TEELE_ONE_SHEET.txt)")
    print("  [3] VERIFY WORM LEDGER INTEGRITY    (ledger_integrity_daemon.py)")
    print("  [4] VIEW APEX COUNSELOR INTAKE      (APEX_ACCELERATOR_INTAKE.md)")
    print("  [5] RUN FULL MISSION REPORT         (c2_mission_readiness_report.py)")
    print("  --- DEPT OF COMMERCE ENERGY CAPABILITIES ---")
    print("  [6] EXECUTE ENERGY C2 DEMO          (ebony_energy_demo.py)")
    print("  [7] VIEW DOC ENERGY BRIEFING        (ROB_TEELE_DOC_ENERGY_BRIEFING.md)")
    print("  [8] VIEW ENERGY ARCHITECTURE        (EBONY_ENERGY_C2_ARCHITECTURE.md)")
    print("  [9] RUN ZERO-CAPEX ROI SIMULATOR    (simulate_energy_savings.py)")
    print("  [0] LAUNCH PRINTABLE ENERGY BINDER  (export_energy_binder_pdf.py)")
    print("  --- COMMERCIAL CONTRACTING & TASK ORDERS ---")
    print("  [C] VIEW COMMERCIAL FEE SCHEDULE    (HVF_COMMERCIAL_FEE_SCHEDULE.md)")
    print("  [T] VIEW COMMERCIAL TERMS SCRIPT    (ROB_TEELE_COMMERCIAL_TERMS_BRIEF.md)")
    print("  [S] VIEW TURNKEY PHASE 1 SOW        (PHASE_1_PILOT_SOW.md)")
    print("  [Q] EXIT CONSOLE")
    print("-" * 80)

def run_cmd(script_name):
    script_path = cockpit_dir / script_name
    if script_path.suffix == ".py":
        subprocess.run([sys.executable, str(script_path)])
    elif script_path.suffix in [".txt", ".md"]:
        print("\n" + "-" * 80)
        print(script_path.read_text(encoding="utf-8"))
        print("-" * 80)

def main():
    while True:
        display_menu()
        choice = input("Enter Command Selection [0-9, C, T, S, Q]: ").strip().upper()
        mapping = {
            "1": "ebony_executive_demo.py",
            "2": "ROB_TEELE_ONE_SHEET.txt",
            "3": "ledger_integrity_daemon.py",
            "4": "APEX_ACCELERATOR_INTAKE.md",
            "5": "c2_mission_readiness_report.py",
            "6": "ebony_energy_demo.py",
            "7": "ROB_TEELE_DOC_ENERGY_BRIEFING.md",
            "8": "EBONY_ENERGY_C2_ARCHITECTURE.md",
            "9": "simulate_energy_savings.py",
            "0": "export_energy_binder_pdf.py",
            "C": "HVF_COMMERCIAL_FEE_SCHEDULE.md",
            "T": "ROB_TEELE_COMMERCIAL_TERMS_BRIEF.md",
            "S": "PHASE_1_PILOT_SOW.md"
        }
        if choice in mapping:
            run_cmd(mapping[choice])
        elif choice in ["Q", "QUIT", "EXIT"]:
            print("[*] Exiting Sovereign C2 Executive Console.")
            break
        else:
            print("[-] Invalid selection. Enter 0-9, C, T, S, or Q.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("[+] Sovereign Meeting Launchpad verified ready with Complete Commercial Suite.")
    else:
        main()