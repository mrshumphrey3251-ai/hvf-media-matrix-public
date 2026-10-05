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
        content = f.read()

    # Find the sidebar radio declaration
    # Pattern: radio_var = st.sidebar.radio(..., [options]...)
    print(f"[*] Inspecting {p.name}...")
    
    # Check where "Command Modules" or st.sidebar.radio is called
    lines = content.splitlines()
    for idx, l in enumerate(lines):
        if "st.sidebar.radio" in l or "Command Modules" in l:
            print(f"    Line {idx+1}: {l.strip()[:100]}")

    # Inject '⚡ Action Desk' into the options array if present
    # Look for options=[...] or direct list inside radio(...)
    match = re.search(r'st\.sidebar\.radio\s*\(\s*["\']🎛 Command Modules["\']\s*,\s*(\[[^\]]+\])', content)
    if match:
        raw_list = match.group(1)
        if "⚡ Action Desk" not in raw_list:
            new_list = raw_list.replace("[", '[\n        "⚡ Action Desk",')
            content = content.replace(raw_list, new_list)
            print(f"[+] Direct-wired '⚡ Action Desk' into radio options in {p.name}")
    else:
        # Fallback: look for modules = [...] right before st.sidebar.radio
        mod_match = re.search(r'([a-zA-Z0-9_]*modules\s*=\s*\[)(.*?)(\])', content, re.DOTALL)
        if mod_match and "⚡ Action Desk" not in mod_match.group(0):
            orig_block = mod_match.group(0)
            replaced_block = orig_block.replace(mod_match.group(1), mod_match.group(1) + '\n    "⚡ Action Desk",')
            content = content.replace(orig_block, replaced_block)
            print(f"[+] Prepend '⚡ Action Desk' to variable list in {p.name}")

    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

    py_compile.compile(str(p), doraise=True)
    print(f"[+] Clean compile verified: {p.name}")
