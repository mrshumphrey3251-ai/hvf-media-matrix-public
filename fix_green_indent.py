from pathlib import Path
import re
import py_compile

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\ebony_console_GREEN.py")
]

for p in targets:
    if not p.exists():
        continue

    with open(p, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    clean_lines = []
    skip_broken_block = False

    # Remove any broken injected block first to get back to a clean baseline
    for line in lines:
        if 'elif active_module == "⚡ Action Desk"' in line or 'import action_desk' in line or 'action_desk.render()' in line:
            continue
        clean_lines.append(line)

    # Re-insert with the exact indentation of the matching if-branch
    final_lines = []
    for line in clean_lines:
        final_lines.append(line)
        if "c2_gate_dashboard.render()" in line:
            # Measure indentation of the line containing c2_gate_dashboard.render()
            indent_len = len(line) - len(line.lstrip())
            # The elif matches the parent block (indent_len - 4 if inside an if block, or matching if directly)
            base_indent = " " * max(0, indent_len - 4) if indent_len >= 4 else ""
            body_indent = " " * (len(base_indent) + 4)

            action_desk_block = [
                f'{base_indent}elif "Action Desk" in str(active_module):\n',
                f'{body_indent}import sys\n',
                f'{body_indent}ext_dir = str(BASE_DIR / "level5_extensions")\n',
                f'{body_indent}if ext_dir not in sys.path:\n',
                f'{body_indent}    sys.path.insert(0, ext_dir)\n',
                f'{body_indent}import action_desk\n',
                f'{body_indent}action_desk.render()\n'
            ]
            final_lines.extend(action_desk_block)

    with open(p, "w", encoding="utf-8") as f:
        f.writelines(final_lines)

    try:
        py_compile.compile(str(p), doraise=True)
        print(f"[+] Fixed indentation cleanly and compiled: {p}")
    except py_compile.PyCompileError as e:
        print(f"[-] Indentation error remaining on {p}: {e}")
