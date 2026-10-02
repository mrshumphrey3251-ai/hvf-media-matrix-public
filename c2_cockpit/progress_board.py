import json
from pathlib import Path
from threading import Lock
from datetime import datetime

BASE = Path(__file__).parent
BOARD_FILE = BASE / "progress_board.json"
_lock = Lock()

def _load() -> dict:
    if BOARD_FILE.exists():
        return json.loads(BOARD_FILE.read_text())
    return {}

def save_phase(phase: str, status: str, notes: str = ""):
    """Update the status of a phase."""
    with _lock:
        data = _load()
        data[phase] = {
            "status": status,
            "notes": notes,
            "updated": datetime.utcnow().isoformat() + "Z"
        }
        BOARD_FILE.write_text(json.dumps(data, indent=2))
        print(f"✅ {phase} set to {status}")
        return f"✅ {phase} set to {status}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        exec(sys.argv[1])
