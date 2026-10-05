from pathlib import Path
import re

target = Path(r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py")

if not target.exists():
    print(f"[-] Target missing: {target}")
else:
    with open(target, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    
    print(f"[*] Total lines in {target.name}: {len(lines)}")
    print("[*] Searching for system prompt assignments & API payload construction:\n")
    for i, line in enumerate(lines):
        if any(keyword in line for keyword in ["role\": \"system\"", "role\":\"system\"", "system_prompt", "SOVEREIGN_OPERATIONAL_DOCTRINE", "load_ultimate_law_context", "messages_payload"]):
            print(f"  Line {i+1}: {line.strip()[:100]}")
