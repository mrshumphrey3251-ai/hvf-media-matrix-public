"""
PROJECT EBONY: SOVEREIGN DYNAMIC AI CODER (v3.0)
ROLE: Real-time LLM-driven code generation, Codex enforcement, quarantine staging, and harness validation.
"""

import os
import sys
import re
import subprocess
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SANDBOX_DIR = BASE_DIR / "sandbox_staging"
HARNESS_PATH = SANDBOX_DIR / "sandbox_harness.py"

for p in [str(BASE_DIR / "dispatch_core"), str(BASE_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import sovereign_comms

SYSTEM_CODEX_PROMPT = """You are Ebony, an autonomous Level 5 software architect.
Write a COMPLETE, self-contained Python module for a Streamlit application based on the user specification.

STRICT ARCHITECTURAL INVARIANTS:
1. Must define MODULE_METADATA dictionary at top level with 'name', 'version', 'author', 'description'.
2. Must define an execute(context=None) -> dict function for headless harness testing.
3. Must define a render() function containing the complete Streamlit UI.
4. Do NOT use fake/mock individual names unless explicitly asked. Use real operational interfaces, database inputs, file uploaders, API payload builders, or configurable forms.
5. Return ONLY executable raw Python code. Do NOT wrap in markdown fences (no ```python). Zero preamble, zero explanation."""

class SovereignCoder:
    def __init__(self):
        self.sandbox_dir = SANDBOX_DIR
        self.sandbox_dir.mkdir(parents=True, exist_ok=True)

    def generate_and_stage(self, module_name: str, specification: str) -> dict:
        if not module_name.endswith(".py"):
            module_name = f"{module_name}.py"

        target_path = self.sandbox_dir / module_name

        # Call live inference cascade
        prompt = f"USER SPECIFICATION:\n{specification}\n\nDeliver the production-ready Level 5 module."
        raw_code = sovereign_comms.generate_chat_response(prompt)

        # Sanitize markdown artifacts if returned by LLM
        if "```" in raw_code:
            match = re.search(r'```(?:python)?\s*(.*?)\s*```', raw_code, re.DOTALL)
            if match:
                raw_code = match.group(1)
            else:
                raw_code = raw_code.replace("```python", "").replace("```", "")

        # Write clean code to quarantine staging
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(raw_code.strip())

        # Run sandbox harness self-test
        try:
            res = subprocess.run(
                [sys.executable, str(HARNESS_PATH), module_name],
                capture_output=True,
                text=True,
                timeout=12
            )
            if res.returncode == 0:
                return {
                    "success": True,
                    "module": module_name,
                    "target_path": str(target_path),
                    "harness_output": res.stdout.strip()
                }
            else:
                return {
                    "success": False,
                    "error": f"Harness verification failed:\n{res.stderr.strip() or res.stdout.strip()}"
                }
        except Exception as e:
            return {"success": False, "error": f"Execution exception: {e}"}
