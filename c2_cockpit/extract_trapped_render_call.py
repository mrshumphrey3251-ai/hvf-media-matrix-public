import sys
from pathlib import Path
import py_compile

target = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py")

if not target.exists():
    print(f"[CRITICAL ERROR] Target file not found: {target}")
    sys.exit(1)

content = target.read_text(encoding="utf-8")
lines = content.splitlines(keepends=True)

# 1. Remove all non-definition calls to render_communications_dispatch_ui
cleaned_lines = []
for line in lines:
    stripped = line.strip()
    if "render_communications_dispatch_ui(" in stripped and not stripped.startswith("def "):
        continue
    cleaned_lines.append(line)

print(f"[*] Stripped trapped call. Current line count: {len(cleaned_lines)}")

# 2. Locate stepper_draft_ line
stepper_idx = -1
for i, line in enumerate(cleaned_lines):
    if "stepper_draft_" in line:
        stepper_idx = i
        break

if stepper_idx == -1:
    print("[ERROR] Could not find stepper_draft_ in console script.")
    sys.exit(1)

# 3. Locate opening line of st.text_area
ta_start = stepper_idx
while ta_start >= 0 and "st.text_area" not in cleaned_lines[ta_start]:
    ta_start -= 1

# 4. Locate closing parenthesis of st.text_area
close_idx = stepper_idx
while close_idx < len(cleaned_lines) and ")" not in cleaned_lines[close_idx]:
    close_idx += 1

base_indent = cleaned_lines[ta_start][:len(cleaned_lines[ta_start]) - len(cleaned_lines[ta_start].lstrip())]
print(f"[+] Located st.text_area between lines {ta_start + 1} and {close_idx + 1}")

# 5. Rebuild clean argument block inside st.text_area
args_block = []
for j in range(ta_start + 1, close_idx):
    s = cleaned_lines[j].strip()
    if not s or s.startswith("#"):
        continue
    arg_indent = cleaned_lines[j][:len(cleaned_lines[j]) - len(cleaned_lines[j].lstrip())]
    if not arg_indent:
        arg_indent = base_indent + "    "
    args_block.append(f"{arg_indent}{s.rstrip(',')},\n")

clean_call = [cleaned_lines[ta_start]] + args_block + [cleaned_lines[close_idx]]

# 6. Append standalone render_communications_dispatch_ui call immediately AFTER st.text_area
clean_call.append(f"\n{base_indent}render_communications_dispatch_ui(key_suffix=\"sovereign_deck_main\")\n")

final_lines = cleaned_lines[:ta_start] + clean_call + cleaned_lines[close_idx + 1:]
target.write_text("".join(final_lines), encoding="utf-8")

print("[*] Running py_compile verification...")
try:
    py_compile.compile(str(target), doraise=True)
    print("[SUCCESS] ebony_console_GREEN.py compiled cleanly with ZERO errors (Exit Code 0)!")
except py_compile.PyCompileError as e:
    print(f"[COMPILATION ERROR] {e}")
    sys.exit(1)