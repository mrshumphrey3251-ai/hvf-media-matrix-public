"""
Project Ebony: Master Historical Live Launcher (Streamlit Native Interface)
Launches the complete historical console from commit 504dd58 with verified Brain 3 LPU Core.
Sole Controlling Authority: Jeffery Humphrey (100% Absolute Authority).
"""

import os
import sys
import subprocess

print("=" * 64)
print("  PROJECT EBONY // HISTORICAL C2 CONSOLE LAUNCHER")
print("  Sole Authority: Jeffery Humphrey (100% Absolute Authority)")
print("  Architecture: Commit 504dd58 Native Console + Brain 3 Groq LPU")
print("=" * 64)

cmd = [sys.executable, "-m", "streamlit", "run", "c2_cockpit/ebony_console.py", "--server.port=8501", "--server.headless=false"]
print(f"\nExecuting: {' '.join(cmd)}\n")
subprocess.run(cmd)
