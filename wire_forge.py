targets = [
    r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py",
    r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\ebony_console_GREEN.py"
]

for filepath in targets:
    with open(filepath, "r", encoding="utf-8-sig") as f:
        content = f.read()

    if "import c2_forge_dashboard" not in content:
        content = content.replace("import c2_gate_dashboard", "import c2_gate_dashboard\nimport c2_forge_dashboard")

    # Add option to navigation radio list if not present
    if '"⚡ Autonomous Build Forge"' not in content:
        content = content.replace(
            '"🎛️ Master C2 Cockpit",',
            '"🎛️ Master C2 Cockpit",\n        "⚡ Autonomous Build Forge",'
        )

    # Route execution to forge dashboard
    forge_render_block = """elif active_module == "⚡ Autonomous Build Forge":
        c2_forge_dashboard.render()"""

    if 'elif active_module == "⚡ Autonomous Build Forge":' not in content:
        content = content.replace(
            'elif active_module == "🛡️ CEO Authorization Gate":',
            f'{forge_render_block}\n    elif active_module == "🛡️ CEO Authorization Gate":'
        )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Wired Build Forge into navigation: {filepath}")
