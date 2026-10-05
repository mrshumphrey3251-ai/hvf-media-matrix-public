targets = [
    r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py",
    r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\ebony_console_GREEN.py"
]

for filepath in targets:
    with open(filepath, "r", encoding="utf-8-sig") as f:
        content = f.read()

    # Ensure c2_forge_dashboard is imported alongside gate dashboard
    if "import c2_forge_dashboard" not in content:
        content = content.replace("import c2_gate_dashboard", "import c2_gate_dashboard\nimport c2_forge_dashboard")

    # Locate the active_module block
    lines = content.splitlines(keepends=True)
    fixed_lines = []
    
    # Track base indentation of active_module block
    base_indent = "    "
    for l in lines:
        if 'if active_module == "🎛️ Master C2 Cockpit":' in l:
            base_indent = l[:len(l) - len(l.lstrip())]
            break

    sub_indent = base_indent + "    "

    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Cleanly rebuild the Forge and CEO Gate branches
        if 'elif active_module == "⚡ Autonomous Build Forge":' in line or 'elif active_module == "🛡️ CEO Authorization Gate":' in line:
            # Skip any existing broken consecutive blocks
            while i < len(lines) and any(kw in lines[i] for kw in [
                'active_module == "⚡ Autonomous Build Forge"',
                'c2_forge_dashboard.render()',
                'active_module == "🛡️ CEO Authorization Gate"',
                'c2_gate_dashboard.render()'
            ]):
                i += 1
            
            # Inject properly indented blocks
            fixed_lines.append(f'{base_indent}elif active_module == "⚡ Autonomous Build Forge":\n')
            fixed_lines.append(f'{sub_indent}c2_forge_dashboard.render()\n')
            fixed_lines.append(f'{base_indent}elif active_module == "🛡️ CEO Authorization Gate":\n')
            fixed_lines.append(f'{sub_indent}c2_gate_dashboard.render()\n')
            continue

        fixed_lines.append(line)
        i += 1

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(fixed_lines)
    print(f"[+] Re-aligned routing block in: {filepath}")
