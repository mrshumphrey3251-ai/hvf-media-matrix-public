from pathlib import Path
import re

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\sandbox_staging\api_gateway.py"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\sandbox_staging\api_gateway.py")
]

for p in targets:
    if p.exists():
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        # Filter out safe-state header on line 1
        filtered = [l for l in lines if not l.strip().startswith("[SOVEREIGN") and "Directive acknowledged" not in l]
        with open(p, "w", encoding="utf-8") as f:
            f.writelines(filtered)
        print(f"[+] Scrubbed line 1 preamble from: {p}")
