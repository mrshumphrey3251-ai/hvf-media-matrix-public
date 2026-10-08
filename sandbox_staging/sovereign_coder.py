"""
PROJECT EBONY: DYNAMIC COGNITIVE SYNTHESIS ENGINE
ROLE: Reads the Universal Law, accepts unrestricted user ideas, and synthesizes dynamic code.
"""
import os, sys, re, subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SANDBOX_DIR = BASE_DIR / "sandbox_staging"
SPECS_DIR = BASE_DIR / "architectural_specs"
HARNESS_PATH = SANDBOX_DIR / "sandbox_harness.py"

for p in [str(BASE_DIR / "dispatch_core"), str(BASE_DIR)]:
    if p not in sys.path: sys.path.insert(0, p)

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
        self.specs_dir = SPECS_DIR

    def get_existing_modules(self) -> list:
        return [f.name for f in (BASE_DIR / "level5_extensions").glob("*.py") if f.name != "__init__.py"]

    def generate_and_stage(self, module_name: str, specification: str, target_mode: str = "standalone", merge_target: str = None) -> dict:
        if not module_name.endswith(".py"): module_name += ".py"
        target_path = self.sandbox_dir / module_name
        law_path = self.specs_dir / "LEVEL_5_UI_LAW.md"

        # Step 1: Ingest the Universal Law
        if law_path.exists():
            with open(law_path, "r", encoding="utf-8") as f:
                universal_law = f.read()
        else:
            universal_law = "CRITICAL: Wrap code in `def render():`. Use Streamlit."

        # Step 2: Combine Law with the User's Dynamic Idea
        prompt = (
            f"{universal_law}\n\n"
            f"USER DIRECTIVE (THE IDEA):\n{specification}\n\n"
            "Execute the synthesis now."
        )

        raw_code = _execute_llm_synthesis(prompt)

        # Trap API Timeout
        if "[SOVEREIGN SAFE-STATE]" in raw_code or "timed out" in raw_code.lower():
            return {"success": False, "error": "API TIMEOUT: Your local or cloud AI inference engine is offline. Cannot synthesize dynamic code until the AI is online."}

        # Strip markdown if the AI disobeys
        if "```" in raw_code:
            match = re.search(r'```(?:python)?\s*(.*?)\s*```', raw_code, re.DOTALL)
            raw_code = match.group(1) if match else raw_code.replace("```python", "").replace("```", "")

        # Step 3: Write to Quarantine
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(raw_code.strip())

        # Step 4: Validate in Harness
        try:
            res = subprocess.run([sys.executable, str(HARNESS_PATH), module_name], capture_output=True, text=True, timeout=15)
            if res.returncode == 0:
                return {"success": True, "module": module_name, "target_path": str(target_path), "mode": target_mode, "merged_with": None, "harness_output": res.stdout.strip()}
            return {"success": False, "error": f"Harness verification failed:\n{res.stderr.strip() or res.stdout.strip()}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
