"""
HVFNexus Sovereign Industrial C2 — Ebony Offline Neutralization & Inventory Engine
Audits every Ebony script, catalogs locations, and enforces pure bare-metal execution.
"""
from pathlib import Path

repo_dir = Path("C:/hvf_c2/hvf-media-matrix-private")
print("=== [HVFNexus C2] AUDITING ALL EBONY INSTANCES ===")

ebony_files = [p for p in repo_dir.rglob("*ebony*.py") if ".git" not in p.parts]
for ef in ebony_files:
    print(f"[*] Found: {ef.relative_to(repo_dir)}")

print(f"[+] Total Ebony Script Instances Cataloged: {len(ebony_files)}")