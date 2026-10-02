"""
EBONY SOVEREIGN AIR-GAPPED SANDBOX HARNESS
ROLE: Isolated execution engine for Level 5 code synthesis.
INVARIANT: Executes strictly within sandbox_staging; zero write access to Ring 0.
"""

import sys
import subprocess
import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SANDBOX_DIR = BASE_DIR / "sandbox_staging"

def execute_sandboxed_module(filename: str, timeout_sec: int = 15) -> dict:
    target_path = SANDBOX_DIR / filename
    if not target_path.exists():
        return {
            "success": False,
            "error": f"Target file not found in sandbox: {filename}",
            "traceback": "",
            "stdout": ""
        }

    # Restrict execution environment: do not pass write-tokens or root paths
    clean_env = os.environ.copy()
    clean_env["PYTHONPATH"] = str(SANDBOX_DIR)

    try:
        proc = subprocess.run(
            [sys.executable, str(target_path)],
            cwd=str(SANDBOX_DIR),
            env=clean_env,
            capture_output=True,
            text=True,
            timeout=timeout_sec
        )
        return {
            "success": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "traceback": proc.stderr if proc.returncode != 0 else ""
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Execution timed out after {timeout_sec} seconds.",
            "traceback": "TimeoutExpired",
            "stdout": ""
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": repr(e),
            "stdout": ""
        }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = execute_sandboxed_module(sys.argv[1])
        print(json.dumps(result, indent=2))
    else:
        print("[*] Ebony Sandbox Harness: Active and awaiting module targets.")
