from pathlib import Path
import py_compile

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\c2_gate_dashboard.py"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\c2_gate_dashboard.py")
]

for p in targets:
    if not p.exists():
        continue

    with open(p, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Replace selected_file.stem with Path(selected_file).stem
    old_target = "f\"test_{selected_file.stem}\""
    new_target = "f\"test_{Path(selected_file).stem}\""

    if old_target in content:
        content = content.replace(old_target, new_target)
    else:
        # Fallback regex/string replacement if formatted slightly differently
        content = content.replace("selected_file.stem", "Path(selected_file).stem")

    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

    py_compile.compile(str(p), doraise=True)
    print(f"[+] Successfully fixed Path(selected_file).stem and compiled: {p}")
