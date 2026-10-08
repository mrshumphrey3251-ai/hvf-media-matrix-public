"""
PROJECT EBONY: EBONY COMMAND MODULE INTERCONNECT (v6.0)
ROLE: Binds all promoted Level 5 modules directly to Ebony Command Core
      allowing conversational execution, telemetry ingestion, and autonomous task dispatch.
"""

import sys
import json
import importlib.util
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parent.parent
EXT_DIR = BASE_DIR / "level5_extensions"
REG_FILE = BASE_DIR / "governance" / "architecture" / "EBONY_COMMAND_REGISTRY.json"

class EbonyCommandBridge:
    def __init__(self):
        self.registry = {}
        self.refresh_registry()

    def refresh_registry(self):
        """Scans level5_extensions and compiles Ebony's operational tool manifest."""
        REG_FILE.parent.mkdir(parents=True, exist_ok=True)
        manifest = {}
        
        if EXT_DIR.exists():
            for py_file in EXT_DIR.glob("*.py"):
                if py_file.name.startswith("__"):
                    continue
                mod_name = py_file.stem
                try:
                    spec = importlib.util.spec_from_file_location(f"cmd_{mod_name}", str(py_file))
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    
                    has_exec = hasattr(mod, "execute")
                    has_render = hasattr(mod, "render")
                    doc = getattr(mod, "__doc__", "") or f"Level 5 Extension: {mod_name}"
                    
                    manifest[mod_name] = {
                        "filename": py_file.name,
                        "path": str(py_file),
                        "has_execute": has_exec,
                        "has_render": has_render,
                        "description": doc.strip().splitlines()[0] if doc else "Operational SCADA / Task Module",
                        "registered_at": datetime.now(timezone.utc).isoformat()
                    }
                except Exception as e:
                    manifest[mod_name] = {
                        "filename": py_file.name,
                        "path": str(py_file),
                        "error": str(e),
                        "status": "UNBOUND"
                    }

        self.registry = manifest
        with open(REG_FILE, "w", encoding="utf-8") as rf:
            json.dump(manifest, rf, indent=2)
        return manifest

    def execute_module_command(self, module_name: str, payload: dict = None) -> dict:
        """Executes the module on behalf of Ebony Command."""
        payload = payload or {}
        if module_name not in self.registry:
            self.refresh_registry()
            
        if module_name not in self.registry:
            return {"success": False, "error": f"Module {module_name} is not bound to Ebony Command."}

        mod_info = self.registry[module_name]
        py_path = Path(mod_info["path"])
        if not py_path.exists():
            return {"success": False, "error": f"Physical module file missing: {py_path}"}

        try:
            spec = importlib.util.spec_from_file_location(f"dyn_exec_{module_name}", str(py_path))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            if hasattr(mod, "execute"):
                res = mod.execute(payload)
                return {"success": True, "module": module_name, "result": res}
            else:
                return {"success": True, "module": module_name, "message": "Module mounted and active (UI-only render profile)."}
        except Exception as e:
            return {"success": False, "error": f"Execution fault in {module_name}: {str(e)}"}

if __name__ == "__main__":
    bridge = EbonyCommandBridge()
    reg = bridge.refresh_registry()
    print(f"[+] Ebony Command Bridge successfully bound {len(reg)} Level 5 modules.")