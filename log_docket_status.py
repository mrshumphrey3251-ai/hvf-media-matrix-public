import json
from pathlib import Path
from datetime import datetime, timezone

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\governance\architecture\DOCKET_REGISTRY.json"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\governance\architecture\DOCKET_REGISTRY.json")
]

docket_entry = {
    "docket_id": "9-26-3703",
    "title": "Project Ebony: Sovereign Tri-Brain Bare-Metal Edge Architecture & Sub-Microsecond Kinetic Isolation",
    "external_portal_status": "Compliant/Queued for Assessment",
    "previous_status": "Queued for Next Cycle",
    "verified_at": datetime.now(timezone.utc).isoformat(),
    "compliance_flags": ["NIST_SP_800_82_REV2", "OK_HB_2992", "KINETIC_ISOLATION_VERIFIED"]
}

for p in targets:
    p.parent.mkdir(parents=True, exist_ok=True)
    dockets = []
    if p.exists():
        try:
            with open(p, "r", encoding="utf-8") as f:
                dockets = json.load(f)
        except Exception:
            dockets = []
    
    # Update or insert
    updated = False
    for d in dockets:
        if d.get("docket_id") == "9-26-3703":
            d.update(docket_entry)
            updated = True
            break
    if not updated:
        dockets.insert(0, docket_entry)
        
    with open(p, "w", encoding="utf-8") as f:
        json.dump(dockets, f, indent=2)
    print(f"[+] Synced Docket 9-26-3703 status into: {p}")
