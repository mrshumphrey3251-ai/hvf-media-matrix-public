from pathlib import Path
import re

repo = Path(r"C:\HVF_Repos\hvf-media-matrix-private")

print("[*] Scanning portal controllers for status string definitions...")
for py_file in repo.rglob("*.py"):
    if any(k in py_file.name for k in ["feedback", "submission", "portal", "console", "c2"]):
        try:
            with open(py_file, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
                if "Queued for Assessment" in content or "Queued for Next Cycle" in content or "Compliant" in content:
                    print(f"\n[+] Status mapping found in: {py_file.relative_to(repo)}")
                    for line_no, line in enumerate(content.splitlines(), 1):
                        if any(s in line for s in ["Queued for", "Compliant/", "Status", "STATUS_"]):
                            if len(line.strip()) < 120:
                                print(f"    L{line_no}: {line.strip()}")
        except Exception:
            pass
