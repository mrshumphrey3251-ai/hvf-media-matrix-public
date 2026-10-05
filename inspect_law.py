from pathlib import Path

targets = [
    Path(r"C:\HVF_Repos\ultimate-law-private"),
    Path(r"C:\HVF_Repos\ultimate-law-public")
]

print("[*] Inspecting files inside Ultimate Law repositories...\n")

for repo in targets:
    if not repo.exists():
        print(f"[-] Missing: {repo}")
        continue
    print(f"=== REPOSITORY: {repo.name} ===")
    for p in repo.rglob("*.*"):
        if any(skip in p.parts for skip in [".git", "__pycache__", "venv"]):
            continue
        rel = p.relative_to(repo)
        size = p.stat().st_size
        print(f"  - {rel} ({size} bytes)")
        if p.suffix.lower() in [".md", ".txt"]:
            try:
                with open(p, "r", encoding="utf-8", errors="replace") as f:
                    preview = f.readline().strip()
                print(f"      Header preview: {preview[:80]}")
            except Exception:
                pass
    print()
