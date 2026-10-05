targets = [
    r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py",
    r"C:\HVF_Repos\hvf-media-matrix-public\c2_cockpit\ebony_console_GREEN.py"
]

import re

for filepath in targets:
    with open(filepath, "r", encoding="utf-8-sig") as f:
        content = f.read()

    # Ensure dynamic module loader helper is present
    dynamic_nav_code = """
import json
from pathlib import Path
SIDEBAR_REG_FILE = Path(__file__).resolve().parent.parent / "governance" / "architecture" / "SIDEBAR_MODULES.json"
DYNAMIC_MODULES = {}
if SIDEBAR_REG_FILE.exists():
    try:
        with open(SIDEBAR_REG_FILE, "r", encoding="utf-8") as f_reg:
            for item in json.load(f_reg):
                DYNAMIC_MODULES[item["title"]] = item["filename"]
    except Exception:
        DYNAMIC_MODULES = {}
"""

    if "SIDEBAR_REG_FILE =" not in content:
        content = content.replace("import streamlit as st", f"import streamlit as st\n{dynamic_nav_code}")

    # Inject dynamic modules into the radio list
    radio_target = 'active_module = st.sidebar.radio("Navigation", ['
    if radio_target in content and "+ list(DYNAMIC_MODULES.keys())" not in content:
        content = content.replace(
            radio_target,
            'nav_options = [\n        "🎛️ Master C2 Cockpit",\n        "⚡ Autonomous Build Forge",\n        "🛡️ CEO Authorization Gate",\n        "💬 Sovereign Command",\n        "🧪 Sandbox",\n        "⚙️ Empire Config",\n        "⬛ Media Matrix",\n        "🎨 Asset Synthesis",\n        "📘 Omni-Industry Matrix"\n    ] + list(DYNAMIC_MODULES.keys())\n    active_module = st.sidebar.radio("Navigation", nav_options'
        )

    # Dynamic execution block in main dispatch
    dyn_router = """
elif active_module in DYNAMIC_MODULES:
    mod_filename = DYNAMIC_MODULES[active_module]
    ext_path = Path(__file__).resolve().parent.parent / "level5_extensions" / mod_filename
    if ext_path.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location(f"dyn_{active_module}", str(ext_path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, "render"):
            mod.render()
        elif hasattr(mod, "execute"):
            st.json(mod.execute())
"""

    if "elif active_module in DYNAMIC_MODULES:" not in content:
        content = content.replace(
            'elif active_module == "💬 Sovereign Command":',
            f'{dyn_router.strip()}\n\nelif active_module == "💬 Sovereign Command":'
        )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Dynamic sidebar navigation enabled in: {filepath}")
