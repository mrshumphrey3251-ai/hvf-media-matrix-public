targets = [
    r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py",
    r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\ebony_console_GREEN.py"
]

for filepath in targets:
    with open(filepath, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    fixed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Clean up any malformed forge / gate routing insertions
        if 'active_module == "⚡ Autonomous Build Forge"' in line:
            # Look at previous or next elif indentation
            indent = "    "
            for j in range(max(0, i-5), min(len(lines), i+5)):
                if lines[j].strip().startswith("if active_module ==") or lines[j].strip().startswith("elif active_module =="):
                    indent = lines[j][:len(lines[j]) - len(lines[j].lstrip())]
                    break
            
            fixed_lines.append(f'{indent}elif active_module == "⚡ Autonomous Build Forge":\n')
            fixed_lines.append(f'{indent}    c2_forge_dashboard.render()\n')
            # Skip any malformed duplicate renders
            i += 1
            if i < len(lines) and "c2_forge_dashboard.render()" in lines[i]:
                i += 1
            continue

        if 'active_module == "🛡️ CEO Authorization Gate"' in line:
            indent = "    "
            for j in range(max(0, i-5), min(len(lines), i+5)):
                if lines[j].strip().startswith("if active_module ==") or lines[j].strip().startswith("elif active_module =="):
                    indent = lines[j][:len(lines[j]) - len(lines[j].lstrip())]
                    break
            fixed_lines.append(f'{indent}elif active_module == "🛡️ CEO Authorization Gate":\n')
            i += 1
            continue

        fixed_lines.append(line)
        i += 1

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(fixed_lines)
    print(f"[+] Repaired routing indentation in: {filepath}")
