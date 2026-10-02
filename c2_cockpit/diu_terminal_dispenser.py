"""
HVF Omni-Industrial Matrix | SOVEREIGN PRIME SYSTEMS
Module: diu_terminal_dispenser.py
Author: Jeffery Humphrey, Founder & CEO (Apex Architect)
Classification: PROPRIETARY & CONFIDENTIAL | 100% UNENCUMBERED PRIME
Protocol: DIU COMMERCIAL SOLUTIONS OPENING (CSO) TERMINAL DISPATCH
"""

import os
import sys
import re
import sqlite3
import subprocess
import webbrowser

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
BRIEF_FILE = os.path.join(BASE_DIR, "proposals", "TAILORED_BRIEF_DIU-AOI-2026-AUTONOMY.md")
DIU_PORTAL_URL = "https://www.diu.mil/work-with-us/companies/cso-process"

def pipe_to_clipboard(text: str):
    # Executing clip directly as a list to bypass cmd.exe AutoRun hooks
    p = subprocess.Popen(["clip"], stdin=subprocess.PIPE)
    p.communicate(text.strip().encode("utf-8"))

def parse_brief_sections():
    if not os.path.exists(BRIEF_FILE):
        print(f"[ERROR] DIU Brief file missing at: {BRIEF_FILE}")
        sys.exit(1)

    with open(BRIEF_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    raw_sections = re.split(r'\n(?=## \d+\. )', content)
    header = raw_sections[0].strip()
    
    sections = {0: {"title": "Header & Executive Identifiers", "body": header}}
    for idx, sec in enumerate(raw_sections[1:], 1):
        lines = sec.strip().split("\n")
        title = lines[0].replace("## ", "").strip()
        body = "\n".join(lines[1:]).strip()
        sections[idx] = {
            "title": title,
            "body": f"## {title}\n\n{body}"
        }
    return sections

def log_diu_dispatch(action_desc: str):
    conn = sqlite3.connect(DB_PATH, timeout=10.0, isolation_level=None)
    conn.execute("""
        INSERT INTO corporate_governance_log (authority, target_entity, action, details, timestamp, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "Jeffery Humphrey, CEO",
        "Defense Innovation Unit (DIU)",
        "DIU_SOLUTION_BRIEF_DISPATCHED",
        action_desc,
        os.popen("date /t").read().strip(),
        "BRIEF_DISPATCHED"
    ))
    conn.close()

def main():
    sections = parse_brief_sections()

    print("\n" + "=" * 80)
    print("HVF Omni-Industrial Matrix | DIU DEFENSE SOLUTION BRIEF DISPENSER")
    print("Program: Contested Logistics & Edge Autonomy Resiliency ($1,650,000 USD)")
    print("Prime CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | 10 U.S.C. § 4022 Prototype OT")
    print("=" * 80)
    print(" [1] Copy Section 1: Operational Entity & Prime Authority -> Clipboard")
    print(" [2] Copy Section 2: Architectural Solution: Project Ebony  -> Clipboard")
    print(" [3] Copy Section 3: Milestone Schedule ($150k Mobilization) -> Clipboard")
    print(" [4] Copy Section 4: IP Rights & DFARS 252.227-7018 Terms  -> Clipboard")
    print(" [A] Stream ENTIRE 5-Page Solution Brief to Console")
    print(" [C] Copy ENTIRE 5-Page Solution Brief to Clipboard")
    print(" [O] Open DIU CSO Portal in Default Browser")
    print(" [Q] Quit Dispenser")
    print("=" * 80)

    if len(sys.argv) > 1:
        choice = sys.argv[1].upper()
    else:
        choice = input("Enter Command [1/2/3/4/A/C/O/Q]: ").strip().upper()

    if choice in ['1', '2', '3', '4']:
        idx = int(choice)
        sec = sections[idx]
        pipe_to_clipboard(sec["body"])
        log_diu_dispatch(f"Injected DIU Brief Section {idx} ({sec['title']}) into OS clipboard.")
        print(f"\n[COPIED TO CLIPBOARD] >>> {sec['title']} <<<")
        print("-" * 80)
        print(sec["body"])
        print("-" * 80)
        print("[SUCCESS] Section copied to clipboard.")

    elif choice == 'A':
        with open(BRIEF_FILE, "r", encoding="utf-8") as f:
            full_text = f.read()
        print("\n" + "#" * 80)
        print("STREAMING COMPLETE DIU 5-PAGE SOLUTION BRIEF")
        print("#" * 80)
        print(full_text)
        print("\n[SUCCESS] Full brief rendered to console.")

    elif choice == 'C':
        with open(BRIEF_FILE, "r", encoding="utf-8") as f:
            full_text = f.read()
        pipe_to_clipboard(full_text)
        log_diu_dispatch("Injected entire DIU 5-Page Solution Brief into OS clipboard.")
        print("\n[SUCCESS] Entire 5-Page Brief copied to clipboard. Ready for portal upload.")

    elif choice == 'O':
        print(f"\n[LAUNCHING PORTAL] Opening {DIU_PORTAL_URL}...")
        webbrowser.open(DIU_PORTAL_URL)
        print("[SUCCESS] DIU CSO portal opened in browser.")

    elif choice == 'Q':
        print("\nExiting dispenser.")
    else:
        print("\n[INVALID SELECTION] Run script again with 1, 2, 3, 4, A, C, or O.")

if __name__ == "__main__":
    main()

