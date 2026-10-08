"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: LEVEL5 LOADER
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    """
    EBONY LEVEL 5 EXTENSION HOT-RELOADER
    ROLE: Automatically detects and hot-loads verified modules inside level5_extensions/
          into the C2 Cockpit and Sovereign Command dispatch pipelines.
    """

    import os
    import sys
    import importlib.util
    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent.parent
    EXTENSIONS_DIR = BASE_DIR / "level5_extensions"

    def discover_extensions():
        modules = {}
        if not EXTENSIONS_DIR.exists():
            return modules

        for file in EXTENSIONS_DIR.glob("*.py"):
            if file.name.startswith("__"):
                continue
            module_name = file.stem
            try:
                spec = importlib.util.spec_from_file_location(module_name, str(file))
                if spec and spec.loader:
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    modules[module_name] = {
                        "module": mod,
                        "metadata": getattr(mod, "MODULE_METADATA", {"name": module_name, "version": "1.0.0"}),
                        "has_render": hasattr(mod, "render"),
                        "has_execute": hasattr(mod, "execute")
                    }
            except Exception as e:
                print(f"[-] Error hot-loading extension {module_name}: {e}")
        return modules

    if __name__ == "__main__":
        found = discover_extensions()
        print(f"[+] Level 5 Extension Loader Online: {len(found)} active extensions found.")


if __name__ == "__main__":
    render()
