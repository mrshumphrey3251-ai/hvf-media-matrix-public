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

    # If render function is missing, declare it and make top-level code callable
    if "def render(" not in code:
        # Check if code already runs at module level
        # We wrap the module execution inside render()
        lines = code.splitlines()
        import_lines = []
        body_lines = []
        
        for line in lines:
            if line.startswith("import ") or line.startswith("from ") or line.startswith("#"):
                import_lines.append(line)
            else:
                body_lines.append(line)
        
        new_code = "\n".join(import_lines) + "\n\n"
        new_code += "def render():\n"
        new_code += "    \"\"\"Standard render hook for C2 Cockpit integration.\"\"\"\n"
        for bl in body_lines:
            new_code += "    " + bl + "\n"
        new_code += "\nif __name__ == '__main__':\n    render()\n"
        
        with open(target, "w", encoding="utf-8") as f:
            f.write(new_code)
        print(f"[+] Wrapped {target.name} inside explicit def render()")
    else:
        print(f"[*] def render() already declared in {target.name}")

    py_compile.compile(str(target), doraise=True)
    print(f"[+] Compiled successfully: {target.name}")
