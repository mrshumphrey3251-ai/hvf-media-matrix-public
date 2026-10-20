import os
import sys
import re
from pathlib import Path
import py_compile

base_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private")
cockpit_dir = base_dir / "c2_cockpit"

broken_url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"
# Working public domain test clip for resilient edge fallback
replacement_url = "https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/person-bicycle-car-detection.mp4"

target_files = [
    cockpit_dir / "ebony_console_GREEN.py",
    cockpit_dir / "ebony_console_GOLD.py",
    cockpit_dir / "ebony_console.py",
    cockpit_dir / "app.py",
    base_dir / "app.py"
]

print("=" * 84)
print("     E.B.O.N.Y. SOVEREIGN CLOUD ENDPOINT REMEDIATION ENGINE     ")
print("=" * 84)

remediated_count = 0

for file_path in target_files:
    if not file_path.exists():
        continue
    
    content = file_path.read_text(encoding="utf-8")
    if broken_url in content:
        updated_content = content.replace(broken_url, replacement_url)
        file_path.write_text(updated_content, encoding="utf-8")
        print(f"[REMEDIATED] {file_path.name} -> Replaced dead Google Cloud bucket URL.")
        remediated_count += 1
        
        # Verify compilation immediately
        try:
            py_compile.compile(str(file_path), doraise=True)
            print(f"[COMPILED]   {file_path.name} compiled cleanly (Exit Code 0).")
        except py_compile.PyCompileError as e:
            print(f"[COMPILE FAIL] {file_path.name}: {e}")
            sys.exit(1)
    else:
        print(f"[*] {file_path.name} is clean.")

print("=" * 84)
print(f"Total Files Remediated & Certified: {remediated_count}")
print("=" * 84)