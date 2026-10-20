import os
import sys
import re
from pathlib import Path
import py_compile

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
gold_file = cockpit_dir / "ebony_console_GOLD.py"

if gold_file.exists():
    lines = gold_file.read_text(encoding="utf-8").splitlines(keepends=True)
    
    # 1. Locate the CEO Authorization Gate line
    target_idx = None
    for i, line in enumerate(lines):
        if 'active_module == "🛡️ CEO Authorization Gate"' in line:
            target_idx = i
            break
            
    if target_idx is not None:
        # 2. Search backwards for the preceding active_module branch to get exact indentation
        correct_indent = 0
        for k in range(target_idx - 1, -1, -1):
            if 'active_module ==' in lines[k]:
                correct_indent = len(lines[k]) - len(lines[k].lstrip())
                print(f"[+] Found parent branch at line {k+1} with {correct_indent} leading spaces.")
                break
                
        # 3. Apply exact matching indentation to target line
        lines[target_idx] = (' ' * correct_indent) + lines[target_idx].lstrip()
        body_indent = correct_indent + 4
        
        # 4. Align subsequent body lines until the next branch or function
        for m in range(target_idx + 1, len(lines)):
            s = lines[m].strip()
            if not s:
                continue
            if 'active_module ==' in s or s.startswith('else:') or s.startswith('def ') or s.startswith('class '):
                break
            lines[m] = (' ' * body_indent) + s + '\n'
            
        gold_file.write_text("".join(lines), encoding="utf-8")
        print("[+] Realigned line 594 in ebony_console_GOLD.py.")

# 5. Verify compilation across all cockpit consoles
all_targets = [
    cockpit_dir / "ebony_console_GREEN.py",
    cockpit_dir / "ebony_console_GOLD.py",
    cockpit_dir / "ebony_console.py",
    cockpit_dir / "app.py"
]

print("\n" + "=" * 84)
print("     COMPILATION VERIFICATION MATRIX (ALL COCKPIT CONSOLES)     ")
print("=" * 84)

all_passed = True
for f in all_targets:
    if not f.exists():
        continue
    try:
        py_compile.compile(str(f), doraise=True)
        print(f"[COMPILED OK] {f.name:<25} -> Exit Code 0 Verified.")
    except py_compile.PyCompileError as e:
        print(f"[COMPILE FAIL] {f.name:<25} -> {e}")
        all_passed = False

print("=" * 84)
if not all_passed:
    sys.exit(1)