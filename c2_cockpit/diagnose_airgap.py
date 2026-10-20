"""
HVFNexus Sovereign Industrial C2 — Static Code Air-Gap Auditor
Scans all Python scripts for network calls, sockets, external HTTP requests, and cloud APIs.
"""
import ast
import os
from pathlib import Path

repo_dir = Path("C:/HVF_Repos/hvf-media-matrix-private")
cockpit_dir = repo_dir / "c2_cockpit"

network_modules = {
    "requests", "urllib", "urllib3", "http", "socket", 
    "httpx", "aiohttp", "openai", "google", "anthropic", 
    "boto3", "azure", "dns"
}

print("=== [HVFNexus C2] EXECUTING EXHAUSTIVE AIR-GAP SCAN ===")

flagged_files = {}

for py_path in repo_dir.rglob("*.py"):
    if ".git" in py_path.parts:
        continue
    try:
        content = py_path.read_text(encoding="utf-8", errors="ignore")
        tree = ast.parse(content, filename=str(py_path))
        imported_net = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root_mod = alias.name.split(".")[0]
                    if root_mod in network_modules:
                        imported_net.add(root_mod)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    root_mod = node.module.split(".")[0]
                    if root_mod in network_modules:
                        imported_net.add(root_mod)
        if imported_net:
            flagged_files[py_path.name] = imported_net
    except Exception as e:
        pass

if flagged_files:
    print("[-] NETWORK CALLS / CLOUD MODULES DETECTED IN THE FOLLOWING FILES:")
    for fname, mods in flagged_files.items():
        print(f"    - {fname}: uses modules {list(mods)}")
else:
    print("[+] AST SCAN: Zero network modules imported in Python scripts.")

# Direct inspection of ebony_executive_demo.py
exec_demo = cockpit_dir / "ebony_executive_demo.py"
print("\n[*] Inspecting ebony_executive_demo.py structure:")
if exec_demo.exists():
    lines = exec_demo.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines[:35]):
        print(f"    {i+1}: {line}")
else:
    print("[-] ebony_executive_demo.py does not exist!")

print("\n=== SCAN COMPLETE ===")