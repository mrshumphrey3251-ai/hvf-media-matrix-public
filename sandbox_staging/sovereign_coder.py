"""
PROJECT EBONY: SOVEREIGN DYNAMIC CODER WITH FEATURE FUSION & TARGET ROUTING (v3.3)
ROLE: Standalone synthesis, cross-module feature fusion, and custom target staging.
"""

import os
import sys
import re
import subprocess
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SANDBOX_DIR = BASE_DIR / "sandbox_staging"
EXT_DIR = BASE_DIR / "level5_extensions"
HARNESS_PATH = SANDBOX_DIR / "sandbox_harness.py"

for p in [str(BASE_DIR / "dispatch_core"), str(BASE_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import sovereign_comms

def _execute_llm_synthesis(prompt: str) -> str:
    import os, toml
    from groq import Groq
    key = os.environ.get("GROQ_API_KEY", "")
    sec_path = r"C:\HVF_Repos\hvf-media-matrix-private\.streamlit\secrets.toml"
    if not key and os.path.exists(sec_path):
        try:
            sec = toml.load(sec_path)
            key = sec.get("GROQ_API_KEY", "").strip()
        except Exception: pass
    if not key: return "```python\n# ERROR: NO GROQ KEY\n```"

    client = Groq(api_key=key)

    try:
        models = client.models.list().data
        valid = [m.id for m in models]
        # Dynamically select highest available model tier
        target = next((m for m in valid if "70b" in m.lower()),
                 next((m for m in valid if "8b" in m.lower() or "11b" in m.lower()),
                 valid[0] if valid else "llama3-8b-8192"))
    except Exception:
        target = "llama3-8b-8192"

    print(f"[*] AUTONOMOUS ROUTING: Selected {target}")

    response = client.chat.completions.create(
        model=target,
        messages=[
            {"role": "system", "content": "You are E.B.O.N.Y., an elite Level 5 Autonomous AI writing precise Python code. Return ONLY valid, complete, operational Python code enclosed in ```python fences. No conversational text, no explanations."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )
    return response.choices[0].message.content

class SovereignCoder:
    def __init__(self):
        self.sandbox_dir = SANDBOX_DIR
        self.sandbox_dir.mkdir(parents=True, exist_ok=True)
        self.extensions_dir = EXT_DIR
        self.extensions_dir.mkdir(parents=True, exist_ok=True)

    def get_existing_modules(self) -> list:
        """Returns list of currently active production modules available for feature fusion."""
        return [f.name for f in self.extensions_dir.glob("*.py") if f.name != "__init__.py"]

    def generate_and_stage(self, module_name: str, specification: str, target_mode: str = "standalone", merge_target: str = None) -> dict:
        if not module_name.endswith(".py"):
            module_name = f"{module_name}.py"

        target_path = self.sandbox_dir / module_name

        if target_mode == "merge" and merge_target:
            source_file = self.extensions_dir / merge_target
            if source_file.exists():
                with open(source_file, "r", encoding="utf-8") as f:
                    base_code = f.read()
                prompt = (
                    f"EXISTING BASE MODULE ({merge_target}):\n{base_code}\n\n"
                    f"NEW FEATURE DIRECTIVE TO INTEGRATE:\n{specification}\n\n"
                    "INSTRUCTIONS: Merge the new feature cleanly into the existing base module. "
                    "Preserve all existing functionality, metadata, and controls while adding the new UI sections, "
                    "telemetry, and calculations. Deliver the COMPLETE, production-ready unified Python module. "
                    "Return ONLY valid raw Python code. Zero markdown fences, zero commentary."
                )
                target_path = self.sandbox_dir / merge_target
                module_name = merge_target
            else:
                prompt = f"USER SPECIFICATION:\n{specification}\n\nDeliver the production-ready Level 5 module."
        else:
            prompt = f"USER SPECIFICATION:\n{specification}\n\nDeliver the production-ready Level 5 module."

        raw_code = _execute_llm_synthesis(prompt)

        # Sanitize fences
        if "```" in raw_code:
            match = re.search(r'```(?:python)?\s*(.*?)\s*```', raw_code, re.DOTALL)
            if match:
                raw_code = match.group(1)
            else:
                raw_code = raw_code.replace("```python", "").replace("```", "")

        # Write code to quarantine
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(raw_code.strip())

        # Test against sandbox harness
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
                    "mode": target_mode,
                    "merged_with": merge_target if target_mode == "merge" else None,
                    "harness_output": res.stdout.strip()
                }
            else:
                return {
                    "success": False,
                    "error": f"Harness verification failed:\n{res.stderr.strip() or res.stdout.strip()}"
                }
        except Exception as e:
            return {"success": False, "error": f"Execution exception: {e}"}

