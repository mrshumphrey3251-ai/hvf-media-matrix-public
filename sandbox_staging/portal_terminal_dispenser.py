"""
HVF Omni-Industrial Matrix | SOVEREIGN PRIME SYSTEMS
Module: portal_terminal_dispenser.py
Author: Jeffery Humphrey, Founder & CEO (Apex Architect)
Classification: PROPRIETARY & CONFIDENTIAL | 100% UNENCUMBERED PRIME
Protocol: TERMINAL-FIRST PAYLOAD DISPATCH & CLIPBOARD INJECTION
"""

import os
import sys
import re
import sqlite3
import subprocess
import webbrowser

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
PAYLOAD_FILE = os.path.join(BASE_DIR, "proposals", "NSF_PORTAL_CLIPBOARD_READY.txt")
PORTAL_URL = "https://seedfund.nsf.gov/apply/project-pitch/"

def copy_to_clipboard(text: str):
    """Pipes text directly into Windows OS clipboard via native clip.exe"""
    p = subprocess.Popen("clip", stdin=subprocess.PIPE, shell=True)
    p.communicate(text.strip().encode("utf-8"))

def parse_fields():
    if not os.path.exists(PAYLOAD_FILE):
        print(f"[ERROR] Payload file missing at: {PAYLOAD_FILE}")
        sys.exit(1)

    with open(PAYLOAD_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"--- \[START (Field \d: [^\]]+)\] --- \(Word Count: (\d+)/\d+\)\n(.*?)\n--- \[END \1\] ---"
    matches = re.findall(pattern, content, re.DOTALL)
    
    fields = {}
    for idx, (title, wc, body) in enumerate(matches, 1):
        fields[idx] = {
            "title": title.strip(),
            "word_count": int(wc),
            "body": body.strip()
        }
    return fields

def log_dispatch(action_desc: str):
    conn = sqlite3.connect(DB_PATH, timeout=10.0, isolation_level=None)
    conn.execute("""
        INSERT INTO corporate_governance_log (authority, target_entity, action, details, timestamp, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "Jeffery Humphrey, CEO",
        "NSF Seed Fund Portal",
        "TERMINAL_PAYLOAD_DISPATCHED",
        action_desc,
        os.popen("date /t").read().strip(),
        "CLIPBOARD_COPIED"
    ))
    conn.close()

def main():
    fields = parse_fields()
    
    print("\n" + "=" * 80)
    print("HVF Omni-Industrial Matrix | NSF SEED FUND TERMINAL DISPENSER")
    print("Authority: Jeffery Humphrey, Founder & CEO | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5")
    print("=" * 80)
    print(" [1] Copy Field 1: Technology Innovation (413 words) -> Windows Clipboard")
    print(" [2] Copy Field 2: Technical Objectives   (114 words) -> Windows Clipboard")
    print(" [3] Copy Field 3: Market Opportunity     (123 words) -> Windows Clipboard")
    print(" [4] Copy Field 4: Company and Team       (78 words)  -> Windows Clipboard")
    print(" [A] Stream ALL 4 Fields to Terminal Screen (Full Output)")
    print(" [O] Open NSF Submission Portal in Default Browser")
    print(" [Q] Quit Terminal Dispenser")
    print("=" * 80)

    if len(sys.argv) > 1:
        choice = sys.argv[1].upper()
    else:
        choice = input("Enter Command [1/2/3/4/A/O/Q]: ").strip().upper()

    if choice in ['1', '2', '3', '4']:
        idx = int(choice)
        f = fields[idx]
        copy_to_clipboard(f["body"])
        log_dispatch(f"Injected {f['title']} into OS clipboard buffer.")
        print(f"\n[COPIED TO CLIPBOARD] >>> {f['title']} <<<")
        print("-" * 80)
        print(f["body"])
        print("-" * 80)
        print("[SUCCESS] Text is now in your clipboard. Press Ctrl+V in the portal field.")

    elif choice == 'A':
        print("\n" + "#" * 80)
        print("STREAMING COMPLETE PROPOSAL PAYLOAD TO TERMINAL")
        print("#" * 80)
        for idx in range(1, 5):
            f = fields[idx]
            print(f"\n>>> [{f['title']}] (Word Count: {f['word_count']}) <<<")
            print(f["body"])
            print("-" * 60)
        print("\n[SUCCESS] Full proposal rendered to console.")

    elif choice == 'O':
        print(f"\n[LAUNCHING PORTAL] Opening {PORTAL_URL}...")
        webbrowser.open(PORTAL_URL)
        print("[SUCCESS] NSF submission portal opened in browser.")

    elif choice == 'Q':
        print("\nExiting dispenser.")
    else:
        print("\n[INVALID SELECTION] Run script again with 1, 2, 3, 4, A, or O.")

if __name__ == "__main__":
    main()

