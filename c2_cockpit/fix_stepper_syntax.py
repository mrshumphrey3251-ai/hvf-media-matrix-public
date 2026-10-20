import sys
from pathlib import Path
import py_compile

target = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py")

if not target.exists():
    print(f"[CRITICAL ERROR] Target file not found: {target}")
    sys.exit(1)

content = target.read_text(encoding="utf-8")
lines = content.splitlines(keepends=True)

# Find all lines containing stepper_draft_
stepper_indices = [i for i, line in enumerate(lines) if "stepper_draft_" in line]
print(f"[+] Found {len(stepper_indices)} stepper_draft_ reference(s) at line(s): {[idx+1 for idx in stepper_indices]}")

fixed_count = 0
for idx in stepper_indices:
    # Walk backward to find the opening function call (e.g., st.text_area)
    call_start = idx
    while call_start >= 0 and "(" not in lines[call_start]:
        call_start -= 1
        
    # Walk forward to find the closing parenthesis of this call
    call_end = idx
    while call_end < len(lines) and ")" not in lines[call_end]:
        call_end += 1
        
    print(f"[*] Call boundaries detected: lines {call_start+1} through {call_end+1}")
    
    # Enforce trailing commas on all argument lines within this call
    for j in range(call_start + 1, call_end):
        raw = lines[j]
        stripped = raw.strip()
        if stripped and not stripped.startswith("#") and not stripped.endswith("(") and not stripped.endswith(","):
            lines[j] = raw.rstrip() + ",\n"
            print(f"[FIXED] Restored trailing comma on line {j+1}: {lines[j].strip()}")
            fixed_count += 1

if fixed_count > 0:
    target.write_text("".join(lines), encoding="utf-8")
    print(f"[UPDATED] Wrote {fixed_count} argument delimiter fix(es) to {target.name}")
else:
    print("[INFO] Delimiters verified intact.")

print("[*] Running py_compile verification...")
try:
    py_compile.compile(str(target), doraise=True)
    print("[SUCCESS] ebony_console_GREEN.py compiled cleanly with ZERO errors (Exit Code 0)!")
except py_compile.PyCompileError as e:
    print(f"[COMPILATION ERROR] {e}")
    sys.exit(1)