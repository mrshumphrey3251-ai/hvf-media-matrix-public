"""
HVFNexus Sovereign Industrial C2 — Forensic Desktop Offline Probe
Identifies runtime failures and socket bottlenecks on the local desktop.
"""
import sys
import subprocess
from pathlib import Path

repo_dir = Path("C:/hvf_c2/hvf-media-matrix-private")
cockpit_dir = repo_dir / "c2_cockpit"

print(f"[*] Python Executable: {sys.executable}")
print(f"[*] Python Version:    {sys.version}")

scripts_to_test = [
    repo_dir / "ebony_console_GREEN.py",
    repo_dir / "ebony_launch.py",
    cockpit_dir / "pre_meeting_launchpad.py",
    cockpit_dir / "ebony_executive_demo.py"
]

print("\n=== EXECUTING FORENSIC TEST CYCLES ===")
for script in scripts_to_test:
    if not script.exists():
        print(f"[-] FILE MISSING: {script.name}")
        continue
    print(f"\n[*] Probing {script.name}...")
    try:
        res = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
            timeout=3
        )
        if res.returncode == 0:
            print(f"    [+] SUCCESS: {script.name} executed cleanly (ReturnCode: 0)")
        else:
            print(f"    [-] FAILURE in {script.name} (ReturnCode: {res.returncode}):")
            print("    --- STDERR TRACEBACK ---")
            for line in res.stderr.strip().splitlines()[-8:]:
                print(f"    {line}")
    except subprocess.TimeoutExpired:
        print(f"    [-] TIMEOUT: {script.name} hung (waiting on socket or user input)")
    except Exception as e:
        print(f"    [-] EXCEPTION: {e}")

print("\n=== FORENSIC PROBE COMPLETE ===")