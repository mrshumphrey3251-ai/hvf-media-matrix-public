import sys
from pathlib import Path
import py_compile

target = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py")
try:
    py_compile.compile(str(target), doraise=True)
    print(f"[SUCCESS] {target.name} compiled cleanly with ZERO errors (Exit Code 0)!")
except py_compile.PyCompileError as e:
    print(f"[FAIL] {e}")
    sys.exit(1)