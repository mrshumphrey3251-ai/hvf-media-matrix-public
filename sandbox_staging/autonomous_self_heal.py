"""
PROJECT EBONY: AUTONOMOUS SELF-HEALING & UI REPAIR DISPATCHER (v5.1)
ROLE: Intercepts runtime errors, scrubs conversational preambles/safe-state banners,
      extracts pure Python code, and verifies AST in quarantine.
"""

import sys
import os
import json
import re
import py_compile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SANDBOX_DIR = BASE_DIR / "sandbox_staging"
EXT_DIR = BASE_DIR / "level5_extensions"
GOV_DIR = BASE_DIR / "governance" / "architecture"
REG_FILE = GOV_DIR / "SIDEBAR_MODULES.json"

for p in [str(BASE_DIR / "dispatch_core"), str(BASE_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import sovereign_comms

def clean_pure_python(raw_text: str) -> str:
    """Strips conversational preambles, safe-state headers, and markdown fences."""
    # 1. Extract markdown fences if present
    if "```" in raw_text:
        match = re.search(r'```(?:python)?\s*(.*?)\s*```', raw_text, re.DOTALL)
        if match:
            raw_text = match.group(1)
        else:
            raw_text = raw_text.replace("```python", "").replace("```", "")

    # 2. Strip safe-state banners and LLM acknowledgement prefixes
    lines = raw_text.splitlines()
    clean_lines = []
    found_code_start = False

    for line in lines:
        stripped = line.strip()
        if not found_code_start:
            # Skip safe-state prefixes, acknowledgements, or conversational chatter
            if stripped.startswith("[SOVEREIGN") or "Directive acknowledged" in stripped or stripped.startswith("Here is") or stripped.startswith("Sure,"):
                continue
            # Legitimate Python code starts with docstrings, imports, assignments, defs, or comments
            if (stripped.startswith('"""') or stripped.startswith("'''") or
                stripped.startswith("import ") or stripped.startswith("from ") or
                stripped.startswith("#") or stripped.startswith("def ") or
                stripped.startswith("class ") or stripped.startswith("MODULE_") or
                "=" in stripped):
                found_code_start = True
                clean_lines.append(line)
        else:
            clean_lines.append(line)

    return "\n".join(clean_lines).strip()

def self_heal_candidate(filename: str, error_trace: str) -> dict:
    """Autonomously analyzes error trace, repairs candidate code in sandbox, and verifies."""
    target_path = SANDBOX_DIR / filename
    if not target_path.exists():
        return {"success": False, "error": f"File {filename} not found in staging."}

    with open(target_path, "r", encoding="utf-8", errors="replace") as f:
        broken_code = f.read()

    prompt = (
        f"AUTONOMOUS SELF-HEAL DIRECTIVE:\n"
        f"Target File: {filename}\n"
        f"Detected Error: {error_trace}\n\n"
        f"BROKEN CODE TO REPAIR:\n{broken_code}\n\n"
        "STRICT MANDATE: Return ONLY pure, executable Python code. "
        "Do NOT include conversational preambles, acknowledgements, safe-state banners, or markdown commentary. "
        "Start directly at Line 1 with valid Python imports or module docstrings."
    )

    raw_response = sovereign_comms.generate_chat_response(prompt)
    repaired_code = clean_pure_python(raw_response)

    # Write cleaned code back to quarantine file
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(repaired_code)

    # Validate syntax via compilation test
    try:
        py_compile.compile(str(target_path), doraise=True)
        return {"success": True, "message": "Code successfully sanitized, repaired, and compiled clean."}
    except Exception as e:
        return {"success": False, "error": f"Compilation check failed after repair: {e}"}
