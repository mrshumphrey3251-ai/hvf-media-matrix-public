"""
HVF Media Matrix - Media Processing & Sovereign C2 Subsystem
Package Initialization and Automatic Submodule Resolution (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)
"""
import importlib
import sys
from pathlib import Path

__version__ = "1.0.0"

_C2_DIR = Path(__file__).resolve().parent
if str(_C2_DIR) not in sys.path:
    sys.path.insert(0, str(_C2_DIR))

try:
    import sitecustomize  # Ensure virtual subpackage aliases are active
except Exception:
    pass

try:
    from .hvf_media_orchestrator import HVFMediaOrchestrator
except ImportError:
    from hvf_media_orchestrator import HVFMediaOrchestrator

__all__ = ["HVFMediaOrchestrator"]


def __getattr__(name: str):
    candidates = [name]
    if name.startswith("chronos_"):
        candidates.append(name[len("chronos_"):])
    else:
        candidates.append(f"chronos_{name}")
    for cand in candidates:
        if (_C2_DIR / f"{cand}.py").exists():
            mod = importlib.import_module(cand)
            sys.modules[f"{__name__}.{name}"] = mod
            globals()[name] = mod
            return mod
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
