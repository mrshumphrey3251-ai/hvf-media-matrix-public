"""
HVFNexus Sovereign Industrial C2 — Deep Network Call Pinpointer
Extracts exact line numbers and code snippets where network calls are executed in Ebony files.
"""
from pathlib import Path
import re

repo_dir = Path("C:/hvf_c2/hvf-media-matrix-private")
target_files = [
    "ebony_console_GREEN.py",
    "ebony_console.py",
    "ebony_launch.py",
    "ebony_predict_and_act.py"
]

patterns = [
    r"requests\.(get|post|put|delete)",
    r"socket\.socket",
    r"socket\.connect",
    r"aiohttp\.ClientSession",
    r"http://",
    r"https://"
]

print("=== [HVFNexus C2] PINPOINTING OFFLINE BOTTLENECKS ===")

for target_name in target_files:
    matches = list(repo_dir.rglob(target_name))
    for p in matches:
        if ".git" in p.parts:
            continue
        print(f"\n[*] Scanning file: {p.relative_to(repo_dir)}")
        lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
        found = 0
        for idx, line in enumerate(lines, 1):
            for pat in patterns:
                if re.search(pat, line):
                    print(f"    Line {idx:4d}: {line.strip()[:90]}")
                    found += 1
                    break
        if found == 0:
            print("    [+] No active socket calls detected.")

print("\n=== PINPOINT AUDIT COMPLETE ===")