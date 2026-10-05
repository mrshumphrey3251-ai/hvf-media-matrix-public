import json
from pathlib import Path

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\governance\architecture\SIDEBAR_MODULES.json"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\governance\architecture\SIDEBAR_MODULES.json")
]

for reg_path in targets:
    reg_path.parent.mkdir(parents=True, exist_ok=True)
    data = []
    if reg_path.exists():
        try:
            with open(reg_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []

    # Ensure action_desk is present
    if not any(item.get("filename") == "action_desk.py" for item in data):
        data.append({"filename": "action_desk.py", "title": "⚡ Action Desk"})

    with open(reg_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[+] Registered Action Desk in: {reg_path}")
