import json
from pathlib import Path
from datetime import datetime, timezone

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\governance\architecture\EXTERNAL_ENGAGEMENTS.json"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\governance\architecture\EXTERNAL_ENGAGEMENTS.json")
]

engagement = {
    "entity_name": "Vanderpool Energy Design LLC",
    "jurisdiction": "Pennsylvania",
    "contact_person": "Richard Vanderpool",
    "contact_title": "Founder",
    "delivery_email": "rickyvanderpool15@gmail.com",
    "engagement_type": "Exploratory Infrastructure Alignment",
    "current_status": "NDA Staged for Transmission",
    "governing_law": "State of Oklahoma",
    "ip_safeguards": [
        "Pre-existing IP carve-out for Project Ebony, Protocol Lambda, Chronos SCADA",
        "Patent preclusion clause preventing inclusion into pending vault utility filings",
        "Zero joint-venture / no-partnership governance"
    ],
    "history": [
        {"timestamp": "2026-10-02T20:39:00Z", "event": "Inbound inquiry on LinkedIn regarding physical vault & Chronos SCADA intersection"},
        {"timestamp": "2026-10-02T21:04:00Z", "event": "HVF issued strict NDA-first protocol; rejected informal note-comparing"},
        {"timestamp": "2026-10-02T21:10:00Z", "event": "Counterparty formally consented to standard mutual NDA"},
        {"timestamp": "2026-10-02T21:27:00Z", "event": "Corporate entity details and transmission vector provided"},
        {"timestamp": datetime.now(timezone.utc).isoformat(), "event": "Binding Oklahoma Mutual NDA generated and staged"}
    ]
}

for p in targets:
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(engagement, f, indent=2)
    print(f"[+] Synced external engagement record to: {p}")
