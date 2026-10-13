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

fixed_lines = []
broken_found = False
token = 'st.subheader("🛡️ Real-Time Telemetry HUD")'

for line in lines:
    if token in line and "tab_ledger" in line:
        indent = line[:len(line) - len(line.lstrip())]
        idx = line.find(token)
        
        part1 = line[:idx + len(token)] + "\n"
        part2 = indent + line[idx + len(token):].lstrip()
        
        fixed_lines.append(part1)
        fixed_lines.append(part2)
        broken_found = True
        print(f"[+] Located broken line. Split into:\n    Line 1: {part1.strip()}\n    Line 2: {part2.strip()}")
    else:
        fixed_lines.append(line)

if not broken_found:
    print("[*] Direct match not found. Applying regex normalization...")
    new_content = re.sub(
        r'(st\.subheader\("🛡️ Real-Time Telemetry HUD"\))\s*(tab_ledger)',
        r'\1\n        \2',
        content
    )
    target.write_text(new_content, encoding="utf-8")
else:
    target.write_text("".join(fixed_lines), encoding="utf-8")

print("[*] Running py_compile verification...")
py_compile.compile(str(target), doraise=True)
print("[SUCCESS] ebony_console_GREEN.py compiled with ZERO errors (Exit Code 0)!")