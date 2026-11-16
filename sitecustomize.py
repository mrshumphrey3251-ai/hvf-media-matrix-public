"""
HVF Sovereign Runtime Path-Shield (CAGE: 1AHA8)
Ensures canonical production modules in c2_cockpit/ always take precedence over
archival snapshots in sandbox_staging/ across all current and future scripts.
"""
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_CANONICAL_DIRS = [
    str(_ROOT),
    str(_ROOT / "c2_cockpit"),
    str(_ROOT / "scada_engine"),
    str(_ROOT / "level5_extensions"),
    str(_ROOT / "proposals"),
    str(_ROOT / "src"),
]

# Strip any sandbox_staging path entries so historical snapshots never shadow live code
sys.path[:] = [p for p in sys.path if "sandbox_staging" not in p.replace("\\", "/")]

# Pin canonical directories at the front of sys.path in deterministic order
for _d in reversed(_CANONICAL_DIRS):
    if Path(_d).exists():
        if _d in sys.path:
            sys.path.remove(_d)
        sys.path.insert(0, _d)