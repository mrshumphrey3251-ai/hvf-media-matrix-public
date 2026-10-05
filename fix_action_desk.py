from pathlib import Path
import py_compile

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\level5_extensions\action_desk.py"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\level5_extensions\action_desk.py")
]

for target in targets:
    if not target.exists():
        continue
    with open(target, "r", encoding="utf-8", errors="replace") as f:
        code = f.read()

    if "use_column_width" in code:
        code = code.replace("use_column_width=True", "use_container_width=True")
        code = code.replace("use_column_width", "use_container_width")
        with open(target, "w", encoding="utf-8") as f:
            f.write(code)
        py_compile.compile(str(target), doraise=True)
        print(f"[+] Fixed and compiled: {target}")
    else:
        print(f"[*] No use_column_width found in: {target}")
