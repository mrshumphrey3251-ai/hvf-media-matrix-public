import json
from pathlib import Path
from datetime import datetime, timezone

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\governance\architecture\ACTION_ITEMS.json"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\governance\architecture\ACTION_ITEMS.json")
]

mission_104 = {
    "id": "ACT-104",
    "task": "Calibrate moisture-sensor nodes across HVF Omni-Industrial Matrix (Grain Silo, Energy, Cold-Chain)",
    "priority": "CRITICAL",
    "status": "IN_PROGRESS",
    "owner": "Maya 'Volt' Chen / Ebony SCADA",
    "timestamp": datetime.now(timezone.utc).isoformat()
}

for p in targets:
    p.parent.mkdir(parents=True, exist_ok=True)
    items = []
    if p.exists():
        try:
            with open(p, "r", encoding="utf-8") as f:
                items = json.load(f)
        except Exception:
            items = []

    # Insert ACT-104 at the top if not already present
    if not any(item.get("id") == "ACT-104" for item in items):
        items.insert(0, mission_104)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2)
        print(f"[+] ACT-104 committed to: {p}")
    else:
        print(f"[*] ACT-104 already present in: {p}")
