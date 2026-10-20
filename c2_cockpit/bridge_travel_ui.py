import sys
from pathlib import Path
import py_compile

target = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py")
content = target.read_text(encoding="utf-8")

start_idx = content.find("def render_communications_dispatch_ui")
if start_idx == -1:
    print("[ERROR] Function def render_communications_dispatch_ui not found in console script.")
    sys.exit(1)

lines = content[start_idx:].splitlines(keepends=True)
func_lines = [lines[0]]
rest_lines = []
found_end = False

for line in lines[1:]:
    if not found_end:
        if line.strip() and not line.startswith(" ") and not line.startswith("\t"):
            found_end = True
            rest_lines.append(line)
        else:
            func_lines.append(line)
    else:
        rest_lines.append(line)

bridge_func = """def render_communications_dispatch_ui(key_suffix="sovereign_deck_main"):
    import sys
    from pathlib import Path
    _p = str(Path(r"C:\\hvf_c2\\hvf-media-matrix-private\\c2_cockpit"))
    if _p not in sys.path:
        sys.path.insert(0, _p)
    from ebony_travel_ui import render_communications_dispatch_ui as _r
    return _r(key_suffix)"""

new_content = content[:start_idx] + bridge_func.strip() + "\n\n" + "".join(rest_lines)
target.write_text(new_content, encoding="utf-8")
print("[+] Console successfully bridged to ebony_travel_ui.py.")

print("[*] Running py_compile verification...")
py_compile.compile(str(target), doraise=True)
print("[SUCCESS] ebony_console_GREEN.py compiled cleanly with ZERO errors (Exit Code 0)!")