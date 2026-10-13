import sys
from pathlib import Path
import py_compile

target = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py")

if not target.exists():
    print(f"[CRITICAL ERROR] Target file not found: {target}")
    sys.exit(1)

content = target.read_text(encoding="utf-8")
lines = content.splitlines(keepends=True)

# 1. Strip any orphaned `with tab_comm:` blocks from the bottom of the file
cleaned_lines = []
skip = False
for line in lines:
    if line.strip() == "with tab_comm:":
        skip = True
        continue
    if skip:
        if "render_communications_dispatch_ui" in line:
            skip = False
            continue
        elif line.strip() == "":
            continue
        else:
            skip = False
    cleaned_lines.append(line)

print(f"[+] Stripped orphaned global tab_comm calls. New line count: {len(cleaned_lines)}")

# 2. Locate `with tab_swarm:` and determine block indentation
swarm_idx = -1
swarm_indent = ""
for i, line in enumerate(cleaned_lines):
    if "with tab_swarm:" in line:
        swarm_idx = i
        swarm_indent = line[:len(line) - len(line.lstrip())]
        break

if swarm_idx == -1:
    print("[ERROR] Could not locate with tab_swarm: block in console script.")
    sys.exit(1)

print(f"[+] Located with tab_swarm: at line {swarm_idx + 1} with indentation level {len(swarm_indent)}.")

# 3. Locate the end of the `with tab_swarm:` block
end_swarm_idx = -1
for i in range(swarm_idx + 1, len(cleaned_lines)):
    line = cleaned_lines[i]
    if line.strip() == "":
        continue
    line_indent = line[:len(line) - len(line.lstrip())]
    if len(line_indent) <= len(swarm_indent):
        end_swarm_idx = i
        break

if end_swarm_idx == -1:
    end_swarm_idx = len(cleaned_lines)

# 4. Check if `with tab_comm:` is already properly nested inside the HUD tabs
has_comm = False
for i in range(swarm_idx, end_swarm_idx):
    if "with tab_comm:" in cleaned_lines[i]:
        has_comm = True
        break

if not has_comm:
    comm_block = [
        f"\n{swarm_indent}with tab_comm:\n",
        f"{swarm_indent}    render_communications_dispatch_ui()\n"
    ]
    final_lines = cleaned_lines[:end_swarm_idx] + comm_block + cleaned_lines[end_swarm_idx:]
    print(f"[+] Nested with tab_comm: directly inside HUD block at line {end_swarm_idx + 1}.")
else:
    final_lines = cleaned_lines
    print("[*] with tab_comm: already correctly nested inside HUD block.")

new_content = "".join(final_lines)
target.write_text(new_content, encoding="utf-8")

print("[*] Running py_compile syntax verification...")
py_compile.compile(str(target), doraise=True)
print("[SUCCESS] ebony_console_GREEN.py compiled cleanly with ZERO errors (Exit Code 0)!")