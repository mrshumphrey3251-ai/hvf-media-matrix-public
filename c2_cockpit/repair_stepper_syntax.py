from pathlib import Path
import py_compile
import sys

target = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py")

if not target.exists():
    print(f"[CRITICAL ERROR] Target file not found: {target}")
    sys.exit(1)

content = target.read_text(encoding="utf-8")
lines = content.splitlines(keepends=True)

fixed = False
for i, line in enumerate(lines):
    if 'key=f"stepper_draft_' in line or "key=f'stepper_draft_" in line:
        print(f"[+] Located stepper_draft widget at line {i+1}: {line.strip()}")
        prev_idx = i - 1
        while prev_idx >= 0 and (lines[prev_idx].strip() == "" or lines[prev_idx].strip().startswith("#")):
            prev_idx -= 1
        
        prev_line = lines[prev_idx]
        print(f"[*] Preceding argument at line {prev_idx+1}: {prev_line.strip()}")
        
        if not prev_line.rstrip().endswith(","):
            lines[prev_idx] = prev_line.rstrip() + ",\n"
            print(f"[FIXED] Restored missing comma at line {prev_idx+1}: {lines[prev_idx].strip()}")
            fixed = True
        else:
            print("[*] Comma already present on preceding line.")

if fixed:
    target.write_text("".join(lines), encoding="utf-8")
    print("[UPDATED] ebony_console_GREEN.py written with argument delimiter restored.")
else:
    print("[INFO] No delimiter modifications required.")

print("[*] Running py_compile verification...")
py_compile.compile(str(target), doraise=True)
print("[SUCCESS] ebony_console_GREEN.py compiled cleanly with ZERO errors (Exit Code 0)!")