"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
AUTONOMOUS BATCH PATCHER & REMEDIATION ENGINE
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
"""

from pathlib import Path
import ast
import json
import shutil

ROOT_DIR = Path(__file__).resolve().parent.parent
STAGING_DIR = ROOT_DIR / "sandbox_staging"
COCKPIT_DIR = ROOT_DIR / "c2_cockpit"
EXT_DIR = ROOT_DIR / "level5_extensions"
ARCH_DIR = ROOT_DIR / "governance" / "architecture"

STAGING_DIR.mkdir(parents=True, exist_ok=True)
ARCH_DIR.mkdir(parents=True, exist_ok=True)

def encapsulate(code_str: str, file_name: str) -> str:
    if "def render(" in code_str:
        return code_str
    header = f'''"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: {Path(file_name).stem.upper()}
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
'''
    body_lines = ["    " + line if line.strip() else "" for line in code_str.splitlines()]
    footer = "\n\nif __name__ == '__main__':\n    render()\n"
    wrapped = header + "\n".join(body_lines) + footer
    try:
        ast.parse(wrapped)
        return wrapped
    except Exception:
        return code_str

def run_batch_patch():
    staged = []
    candidates = list(COCKPIT_DIR.glob("*.py")) + list(EXT_DIR.glob("*.py"))
    
    for cand in candidates:
        if cand.name.startswith("__") or cand.name in ["ebony_console_GREEN.py", "c2_gate_dashboard.py"]:
            continue
        try:
            raw = cand.read_text(encoding="utf-8", errors="replace")
            wrapped = encapsulate(raw, cand.name)
            out_file = STAGING_DIR / cand.name
            out_file.write_text(wrapped, encoding="utf-8")
            staged.append(cand.name)
        except Exception:
            continue

    log_file = ARCH_DIR / "BATCH_PATCH_LOG.json"
    log_data = {"total_staged": len(staged), "staged_candidates": staged}
    log_file.write_text(json.dumps(log_data, indent=2), encoding="utf-8")
    print(f"[+] Staged {len(staged)} modules with AST render() encapsulation.")

if __name__ == "__main__":
    run_batch_patch()
