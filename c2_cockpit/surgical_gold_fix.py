import os
import sys
from pathlib import Path
import py_compile

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
gold_file = cockpit_dir / "ebony_console_GOLD.py"

broken_url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"
replacement_url = "https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/person-bicycle-car-detection.mp4"

content = gold_file.read_text(encoding="utf-8")

# Fix A: Replace dead cloud storage URL
if broken_url in content:
    content = content.replace(broken_url, replacement_url)
    print("[+] Replaced dead Google Cloud storage URL.")

# Fix B: Convert orphaned elif to if on CEO Authorization Gate
old_gate = 'elif active_module == "🛡️ CEO Authorization Gate":'
new_gate = 'if active_module == "🛡️ CEO Authorization Gate":'
if old_gate in content:
    content = content.replace(old_gate, new_gate, 1)
    print("[+] Converted orphaned elif to authoritative if branch.")

# Fix C: Indent unindented lines under Master C2 Cockpit
old_cockpit_block = """elif active_module == "🎛️ Master C2 Cockpit":
import c2_cockpit_dashboard
c2_cockpit_dashboard.render()"""

new_cockpit_block = """elif active_module == "🎛️ Master C2 Cockpit":
    import c2_cockpit_dashboard
    c2_cockpit_dashboard.render()"""

if old_cockpit_block in content:
    content = content.replace(old_cockpit_block, new_cockpit_block, 1)
    print("[+] Indented Master C2 Cockpit execution block by 4 spaces.")
else:
    # Alternative CRLF line endings check
    old_cockpit_block_crlf = old_cockpit_block.replace("\n", "\r\n")
    new_cockpit_block_crlf = new_cockpit_block.replace("\n", "\r\n")
    if old_cockpit_block_crlf in content:
        content = content.replace(old_cockpit_block_crlf, new_cockpit_block_crlf, 1)
        print("[+] Indented Master C2 Cockpit execution block by 4 spaces (CRLF).")

gold_file.write_text(content, encoding="utf-8")

# 4. Verify compilation across all cockpit consoles
all_consoles = [
    cockpit_dir / "ebony_console_GREEN.py",
    cockpit_dir / "ebony_console_GOLD.py",
    cockpit_dir / "ebony_console.py",
    cockpit_dir / "app.py"
]

print("\n" + "=" * 84)
print("     FINAL COMPILATION CERTIFICATION MATRIX     ")
print("=" * 84)

all_passed = True
for f in all_consoles:
    if not f.exists():
        continue
    try:
        py_compile.compile(str(f), doraise=True)
        print(f"[COMPILED OK] {f.name:<25} -> Exit Code 0 Certified.")
    except Exception as e:
        print(f"[COMPILE FAIL] {f.name:<25} -> {e}")
        all_passed = False

print("=" * 84)
if not all_passed:
    sys.exit(1)