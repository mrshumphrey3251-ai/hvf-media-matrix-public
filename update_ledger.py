import json
from pathlib import Path
from datetime import datetime, timezone

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\governance\architecture\EXTERNAL_ENGAGEMENTS.json"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\governance\architecture\EXTERNAL_ENGAGEMENTS.json")
]

today_iso = datetime.now(timezone.utc).isoformat()

for p in targets:
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        data["current_status"] = "NDA Dispatched via Email (Awaiting Signature)"
        data["history"].append({
            "timestamp": today_iso,
            "event": "Formal Mutual NDA PDF dispatched via secure transmission to rickyvanderpool15@gmail.com"
        })
        
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"[+] Updated engagement ledger: {p}")

