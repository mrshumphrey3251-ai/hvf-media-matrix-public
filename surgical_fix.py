targets = [
    r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py",
    r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\ebony_console_GREEN.py"
]

target_bad_block = """elif active_module == "⚡ Autonomous Build Forge":
    c2_forge_dashboard.render()
elif active_module == "🛡️ CEO Authorization Gate":
    c2_gate_dashboard.render()
    import c2_gate_dashboard
import c2_forge_dashboard
    c2_gate_dashboard.render()"""

clean_block = """elif active_module == "⚡ Autonomous Build Forge":
    import c2_forge_dashboard
    c2_forge_dashboard.render()

elif active_module == "🛡️ CEO Authorization Gate":
    import c2_gate_dashboard
    c2_gate_dashboard.render()"""

for filepath in targets:
    with open(filepath, "r", encoding="utf-8-sig") as f:
        content = f.read()

    # Normalize CRLF/LF for matching
    content_norm = content.replace("\r\n", "\n")
    target_bad_norm = target_bad_block.replace("\r\n", "\n")
    clean_norm = clean_block.replace("\r\n", "\n")

    if target_bad_norm in content_norm:
        content_norm = content_norm.replace(target_bad_norm, clean_norm)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content_norm)
        print(f"[+] Surgically replaced malformed lines in: {filepath}")
    else:
        # Regex fallback to capture any variation of the garbled block
        import re
        pattern = r'elif active_module == "⚡ Autonomous Build Forge":.*?c2_gate_dashboard\.render\(\)'
        replacement = clean_norm
        new_content, count = re.subn(pattern, replacement, content_norm, flags=re.DOTALL)
        if count > 0:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"[+] Regex-replaced malformed block in: {filepath}")
        else:
            print(f"[-] Target pattern not found in: {filepath}")
