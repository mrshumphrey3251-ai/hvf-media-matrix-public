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

print(f"[*] Total lines before purge: {len(lines)}")

# 1. Strip ALL calls to render_communications_dispatch_ui (preserving only the def)
cleaned_lines = []
for i, line in enumerate(lines):
    stripped = line.strip()
    
    # Preserve the function definition
    if stripped.startswith("def render_communications_dispatch_ui"):
        cleaned_lines.append(line)
        continue
        
    # Drop any call
    if "render_communications_dispatch_ui(" in stripped or stripped == "render_communications_dispatch_ui()":
        print(f"[PURGED] Line {i+1}: {stripped}")
        continue
        
    # Drop orphaned wrappers that were previously injected
    if 'with st.expander("📬 SOVEREIGN COMMUNICATIONS DISPATCH' in stripped:
        print(f"[PURGED] Line {i+1}: {stripped}")
        continue
    if stripped == "with tab_comm:":
        print(f"[PURGED] Line {i+1}: {stripped}")
        continue
        
    cleaned_lines.append(line)

print(f"[*] Total lines after purge: {len(cleaned_lines)}")

# 2. Locate the anchor inside Sovereign Dispatch Deck (below Tactical Executive Response Payload)
deck_idx = -1
deck_indent = "    "

for i, line in enumerate(cleaned_lines):
    if "Tactical Executive Response Payload" in line or "Inbound Threat Scrubber & Transmission Stepper" in line:
        deck_idx = i
        deck_indent = line[:len(line) - len(line.lstrip())]

if deck_idx == -1:
    for i, line in enumerate(cleaned_lines):
        if "SOVEREIGN DISPATCH & STRATEGIC TRIAGE DECK" in line:
            deck_idx = i
            deck_indent = line[:len(line) - len(line.lstrip())]

if deck_idx == -1:
    print("[ERROR] Could not find Sovereign Dispatch Deck anchor in script.")
    sys.exit(1)

print(f"[+] Located Sovereign Dispatch Deck anchor at line {deck_idx + 1}")

# 3. Locate the end of the Sovereign Dispatch Deck block
insert_idx = -1
for i in range(deck_idx + 1, len(cleaned_lines)):
    l = cleaned_lines[i]
    if l.strip() == "":
        continue
    l_indent = l[:len(l) - len(l.lstrip())]
    if len(l_indent) < len(deck_indent) or (len(l_indent) == len(deck_indent) and (l.strip().startswith("elif ") or l.strip().startswith("else:") or l.strip().startswith("def "))):
        insert_idx = i
        break

if insert_idx == -1:
    insert_idx = len(cleaned_lines)

# 4. Insert ONE authoritative call with unique key suffix
call_block = [
    f"\n{deck_indent}render_communications_dispatch_ui(key_suffix=\"sovereign_deck_main\")\n"
]

final_lines = cleaned_lines[:insert_idx] + call_block + cleaned_lines[insert_idx:]
print(f"[+] Mounted single authoritative dispatch UI at line {insert_idx + 1}")

new_content = "".join(final_lines)
target.write_text(new_content, encoding="utf-8")

print("[*] Running py_compile verification...")
py_compile.compile(str(target), doraise=True)
print("[SUCCESS] ebony_console_GREEN.py compiled cleanly with ZERO errors (Exit Code 0)!")