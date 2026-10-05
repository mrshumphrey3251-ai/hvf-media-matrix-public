import json
from pathlib import Path

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public")
]

search_files = [
    "FEEDBACK_RECORDS.json",
    "SUBMISSIONS.json",
    "PORTAL_STATE.json",
    "AUDIT_LEDGER.json",
    "MERKLE_CHRONUS_LOG.json"
]

print("[*] Auditing submission status tags across repositories...")

for repo in targets:
    print(f"\n--- Checking: {repo.name} ---")
    for f in repo.rglob("*.json"):
        if any(term in f.name for term in ["SUBMISSION", "FEEDBACK", "PORTAL", "QUEUE"]):
            try:
                with open(f, "r", encoding="utf-8", errors="replace") as jf:
                    data = json.load(jf)
                    raw_str = json.dumps(data)
                    if "9-26-3703" in raw_str or "Compliant" in raw_str or "Queued" in raw_str:
                        print(f"[+] Match found in: {f.relative_to(repo)}")
                        if isinstance(data, list):
                            for item in data:
                                if isinstance(item, dict) and ("9-26-3703" in str(item) or "Compliant" in str(item)):
                                    print(f"    Record ID / Title: {item.get('id', item.get('title', item.get('submission', 'N/A')))}")
                                    print(f"    Current Status:    {item.get('status', 'N/A')}")
                                    print(f"    History / Cycles:  {item.get('history', item.get('cycle', 'No prior cycle field'))}")
            except Exception:
                pass
