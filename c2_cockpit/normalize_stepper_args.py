import re
import sys
from pathlib import Path
import py_compile

target = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py")

if not target.exists():
    print(f"[CRITICAL ERROR] Target file not found: {target}")
    sys.exit(1)

content = target.read_text(encoding="utf-8")
lines = content.splitlines(keepends=True)

# 1. Locate the stepper_draft_ call
stepper_indices = [i for i, line in enumerate(lines) if "stepper_draft_" in line]
if not stepper_indices:
    print("[ERROR] Could not find stepper_draft_ in file.")
    sys.exit(1)

target_idx = stepper_indices[0]

# 2. Find opening and closing boundaries of the st.text_area call
call_start = target_idx
while call_start >= 0 and "(" not in lines[call_start]:
    call_start -= 1

call_end = target_idx
while call_end < len(lines) and ")" not in lines[call_end]:
    call_end += 1

print(f"[+] Call boundaries: lines {call_start + 1} through {call_end + 1}")
print("--- ORIGINAL ARGUMENTS ---")
for idx in range(call_start, call_end + 1):
    print(f"  Line {idx + 1}: {repr(lines[idx])}")

header = lines[call_start]
footer = lines[call_end]
raw_args = lines[call_start + 1 : call_end]

# 3. Extract and sanitize arguments
parsed_args = []
for l in raw_args:
    s = l.strip().rstrip(",")
    if s and not s.startswith("#"):
        parsed_args.append(s)

if not parsed_args:
    print("[ERROR] No arguments found inside call.")
    sys.exit(1)

label = parsed_args[0]
other_args = parsed_args[1:]

keyword_args = []
for a in other_args:
    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*=', a):
        keyword_args.append(a)
    elif a.isdigit():
        keyword_args.append(f"height={a}")
    else:
        keyword_args.append(f"value={a}")

# 4. Reconstruct call with matching indentation
indent = "    "
for l in raw_args:
    if l.strip():
        indent = l[:len(l) - len(l.lstrip())]
        break

new_arg_lines = [f"{indent}{label},\n"] + [f"{indent}{kw},\n" for kw in keyword_args]
new_call_lines = [header] + new_arg_lines + [footer]

print("--- NORMALIZED RECONSTRUCTED CALL ---")
for l in new_call_lines:
    print("  " + l.strip())

# 5. Commit fix to file
lines = lines[:call_start] + new_call_lines + lines[call_end + 1:]
target.write_text("".join(lines), encoding="utf-8")

print("[*] Running py_compile verification...")
try:
    py_compile.compile(str(target), doraise=True)
    print("[SUCCESS] ebony_console_GREEN.py compiled cleanly with ZERO errors (Exit Code 0)!")
except py_compile.PyCompileError as e:
    print(f"[COMPILATION ERROR] {e}")
    sys.exit(1)