import json
from pathlib import Path
from datetime import datetime, timezone

base_dir = Path(r"C:\HVF_Repos")
cache_targets = [
    base_dir / "hvf-media-matrix-private" / "c2_cockpit" / "SOVEREIGN_CORPUS.json",
    base_dir / "hvf-media-matrix-public" / "c2_cockpit" / "SOVEREIGN_CORPUS.json"
]

corpus = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "repos_indexed": [],
    "ultimate_law_axioms": [],
    "all_files": []
}

print("[*] Building consolidated Sovereign Corpus from local repositories...")

for repo_dir in sorted(base_dir.iterdir()):
    if not repo_dir.is_dir() or repo_dir.name.startswith("."):
        continue
    
    corpus["repos_indexed"].append(repo_dir.name)
    print(f" -> Indexing: {repo_dir.name}")
    
    for file_path in repo_dir.rglob("*.*"):
        if any(skip in file_path.parts for skip in [".git", "venv", ".venv", "__pycache__", "node_modules"]):
            continue
            
        if file_path.suffix.lower() in [".md", ".txt", ".json"]:
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    text = f.read()
                
                lower = text.lower()
                is_law = (
                    "ultimate-law" in repo_dir.name.lower() or 
                    "ultimate law" in lower or 
                    "book of adam" in lower or
                    "22 book" in lower
                )
                
                doc = {
                    "repo": repo_dir.name,
                    "rel_path": str(file_path.relative_to(repo_dir)),
                    "size_bytes": len(text),
                    "is_law_axiom": is_law,
                    "content": text  # Ingest complete text
                }
                
                if is_law:
                    corpus["ultimate_law_axioms"].append(doc)
                    print(f"    [!] Captured Sovereign Law Axiom: {repo_dir.name}/{doc['rel_path']}")
                
                corpus["all_files"].append({
                    "repo": repo_dir.name,
                    "rel_path": str(file_path.relative_to(repo_dir)),
                    "is_law_axiom": is_law
                })
            except Exception:
                pass

print(f"\n[+] Total Repositories Indexed: {len(corpus['repos_indexed'])}")
print(f"[+] Total Sovereign Law Axioms Loaded: {len(corpus['ultimate_law_axioms'])}")

for ct in cache_targets:
    ct.parent.mkdir(parents=True, exist_ok=True)
    with open(ct, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2)
    print(f"[+] Corpus index written to: {ct}")
