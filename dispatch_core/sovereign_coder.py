"""
EBONY SOVEREIGN CODER & SELF-REPAIR ENGINE
ROLE: Translates CEO directives into sandboxed modules, executes test runs,
      and applies deterministic self-repair against the Engineering Codex.
"""

import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SANDBOX_DIR = BASE_DIR / "sandbox_staging"
CODEX_PATH = BASE_DIR / "governance" / "architecture" / "ENGINEERING_CODEX.md"

sys.path.insert(0, str(SANDBOX_DIR))
import sandbox_harness

class SovereignCoder:
    def __init__(self):
        self.sandbox_dir = SANDBOX_DIR
        self.codex_rules = self._load_codex()

    def _load_codex(self) -> str:
        if CODEX_PATH.exists():
            with open(CODEX_PATH, "r", encoding="utf-8") as f:
                return f.read()
        return "Standard Sovereign Isolation Rules Apply."

    def write_draft_module(self, filename: str, code_content: str) -> Path:
        target = self.sandbox_dir / filename
        with open(target, "w", encoding="utf-8") as f:
            f.write(code_content)
        return target

    def test_and_verify(self, filename: str, max_retries: int = 3) -> dict:
        attempt = 1
        while attempt <= max_retries:
            run_result = sandbox_harness.execute_sandboxed_module(filename)
            if run_result.get("success"):
                return {
                    "verified": True,
                    "attempts": attempt,
                    "module": filename,
                    "stdout": run_result.get("stdout")
                }
            
            # Error detected - autonomous repair triggered
            error_trace = run_result.get("traceback") or run_result.get("error")
            print(f"[!] Sandbox Error on attempt {attempt}: {error_trace}")
            
            # In a live cycle, Ebony applies Codex repair here. For this verification baseline, we log and return report.
            attempt += 1

        return {
            "verified": False,
            "attempts": max_retries,
            "module": filename,
            "last_error": error_trace
        }

if __name__ == "__main__":
    coder = SovereignCoder()
    print("[+] Sovereign Coder & Self-Repair Engine Online.")
