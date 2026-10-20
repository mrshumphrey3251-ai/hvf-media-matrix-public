import os
import sys
import re
from pathlib import Path
import py_compile

base_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private")
cockpit_dir = base_dir / "c2_cockpit"

broken_url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"
replacement_url = "https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/person-bicycle-car-detection.mp4"

# 1. Surgically realign line 594 in ebony_console_GOLD.py
gold_file = cockpit_dir / "ebony_console_GOLD.py"
if gold_file.exists():
    lines = gold_file.read_text(encoding="utf-8").splitlines(keepends=True)
    for iteration in range(10):
        try:
            py_compile.compile(str(gold_file), doraise=True)
            print("[+] ebony_console_GOLD.py compiled cleanly with Exit Code 0!")
            break
        except py_compile.PyCompileError as e:
            msg = str(e)
            match = re.search(r'line (\d+)', msg)
            if match and "IndentationError" in msg:
                bad_line = int(match.group(1))
                idx = bad_line - 1
                prev_idx = idx - 1
                while prev_idx >= 0 and not lines[prev_idx].strip():
                    prev_idx -= 1
                if prev_idx >= 0:
                    prev_line = lines[prev_idx]
                    prev_indent = len(prev_line) - len(prev_line.lstrip())
                    cur_line = lines[idx]
                    cur_indent = len(cur_line) - len(cur_line.lstrip())
                    if cur_indent > prev_indent and not prev_line.rstrip().endswith(':'):
                        diff = cur_indent - prev_indent
                        for j in range(idx, len(lines)):
                            if not lines[j].strip():
                                continue
                            j_indent = len(lines[j]) - len(lines[j].lstrip())
                            if j_indent >= cur_indent:
                                lines[j] = lines[j][diff:]
                            else:
                                break
                        gold_file.write_text("".join(lines), encoding="utf-8")
                        continue
            print(f"[!] Compilation notice for GOLD: {e}")
            break

# 2. Sweep all entry points and verify clean compilation
all_targets = [
    cockpit_dir / "ebony_console_GREEN.py",
    cockpit_dir / "ebony_console_GOLD.py",
    cockpit_dir / "ebony_console.py",
    cockpit_dir / "app.py",
    base_dir / "app.py"
]

print("\n" + "=" * 84)
print("     VERIFYING COMPILATION ACROSS ALL COCKPIT CONSOLES     ")
print("=" * 84)

for f in all_targets:
    if not f.exists():
        continue
    content = f.read_text(encoding="utf-8")
    if broken_url in content:
        content = content.replace(broken_url, replacement_url)
        f.write_text(content, encoding="utf-8")
        print(f"[REMEDIATED] {f.name} -> Cleaned dead cloud URL.")
    else:
        print(f"[CLEAN]      {f.name} -> Zero dead cloud URLs.")
    
    try:
        py_compile.compile(str(f), doraise=True)
        print(f"[COMPILED]   {f.name} -> Exit Code 0 verified.")
    except Exception as e:
        print(f"[NOTICE]     {f.name} compilation: {e}")

print("=" * 84)