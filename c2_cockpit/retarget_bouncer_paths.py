import os
import sys
import re
from pathlib import Path
import py_compile

base_dir = Path(r"[REDACTED-PRIVATE-ROOT]")
cockpit_dir = base_dir / "c2_cockpit"

legacy_str = r"[REDACTED-PRIVATE-ROOT]\hvf_shell_bouncer.ps1"
active_str = r"[REDACTED-PRIVATE-ROOT]\hvf_shell_bouncer.ps1"

retargeted = 0
for py_file in base_dir.rglob("*.py"):
    if ".git" in py_file.parts:
        continue
    try:
        content = py_file.read_text(encoding="utf-8")
        if legacy_str in content or "hvf_shell_bouncer.ps1" in content:
            updated = content.replace(legacy_str, active_str)
            if updated != content:
                py_file.write_text(updated, encoding="utf-8")
                print(f"[RETARGETED] {py_file.name} -> Updated to active bouncer path.")
                retargeted += 1
                try:
                    py_compile.compile(str(py_file), doraise=True)
                except Exception as e:
                    print(f"[!] Warning on {py_file.name}: {e}")
    except Exception:
        pass

print(f"Total modules retargeted: {retargeted}")