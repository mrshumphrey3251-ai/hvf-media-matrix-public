import os
import re
import sqlite3
from collections import defaultdict
from pathlib import Path

REPOS_ROOT = Path(r"C:\hvf_c2\repos")
VAULT_DB = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit\omni_repo_vault.db")
PRIMARY_LOCAL_REPOS = [
    Path(r"C:\hvf_c2\hvf-media-matrix-private"),
    Path(r"C:\hvf_c2\hvf-media-matrix-public"),
]

ALLOWED_EXTS = {
    ".py", ".md", ".json", ".yaml", ".yml", ".txt", ".toml", ".sh", ".ps1", ".sql", ".cfg", ".ini"
}
SKIP_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv", "venv", ".archive_tools", "historical_archive", "sandbox_staging"
}

def discover_repositories() -> list[Path]:
    repo_dirs = []
    # Prioritize live working directories first so latest local commits always win
    for p in PRIMARY_LOCAL_REPOS:
        if p.exists():
            repo_dirs.append(p)
    if REPOS_ROOT.exists():
        for entry in sorted(REPOS_ROOT.iterdir()):
            if entry.is_dir() and (entry / ".git").exists():
                if entry.name not in {r.name for r in repo_dirs}:
                    repo_dirs.append(entry)
    return repo_dirs

def refresh_repo_vault() -> tuple[int, int]:
    """Recursively index every readable file across all 15+ repositories into SQLite with zero truncation."""
    conn = sqlite3.connect(str(VAULT_DB))
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS repo_files (
            repo_name TEXT,
            rel_path TEXT,
            char_len INTEGER,
            content TEXT,
            PRIMARY KEY (repo_name, rel_path)
        )
    """)
    cur.execute("DELETE FROM repo_files")

    seen = set()
    repos = discover_repositories()
    total_files = 0
    for repo in repos:
        rname = repo.name
        for root, dirs, files in os.walk(repo):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
            for fname in sorted(files):
                fpath = Path(root) / fname
                if fpath.suffix.lower() not in ALLOWED_EXTS:
                    continue
                rel_str = fpath.relative_to(repo).as_posix()
                if (rname, rel_str) in seen:
                    continue
                seen.add((rname, rel_str))
                try:
                    txt = fpath.read_text(encoding="utf-8", errors="replace")
                    cur.execute(
                        "INSERT INTO repo_files (repo_name, rel_path, char_len, content) VALUES (?, ?, ?, ?)",
                        (rname, rel_str, len(txt), txt)
                    )
                    total_files += 1
                except Exception:
                    continue
    conn.commit()
    conn.close()
    return len(repos), total_files

def build_omni_repo_context(user_prompt: str, max_deep_chars: int = 14500) -> str:
    """
    Zero-overflow multi-repository context builder across all 15 repositories:
    - Lists all 15 repositories, root files, and all blueprints/ subdirectories.
    - Injects full, untruncated contents of Phase1_Supplier_Tracker.md,
      Phase2_Integration_Tracker.md, and top query-matched files across all repos.
    """
    repo_count, file_count = refresh_repo_vault()
    conn = sqlite3.connect(str(VAULT_DB))
    cur = conn.cursor()
    cur.execute("SELECT repo_name, rel_path, char_len, content FROM repo_files ORDER BY repo_name, rel_path")
    rows = cur.fetchall()
    conn.close()

    by_repo = defaultdict(list)
    for rname, rpath, clen, _ in rows:
        by_repo[rname].append(rpath)

    header = [
        "=== E.B.O.N.Y. OMNI-REPOSITORY FULL-READ VAULT ===",
        f"Indexed Repositories ({repo_count}): {', '.join(sorted(by_repo.keys()))}",
        f"Total Untruncated Files Indexed: {file_count}",
        "DIRECTIVE: Verify all facts against the untruncated repository files below."
    ]

    for rname in sorted(by_repo.keys()):
        paths = by_repo[rname]
        root_files = [p for p in paths if "/" not in p]
        bp_files = [p for p in paths if p.startswith("blueprints/")]
        preview_list = root_files[:10]
        if bp_files:
            preview_list.append(f"blueprints/ ({len(bp_files)} specs: {', '.join(p.split('/')[1] for p in bp_files)})")
        elif len(paths) > len(root_files):
            sub_sample = [p for p in paths if "/" in p][:6]
            preview_list.extend(sub_sample)
        header.append(f"- {rname} ({len(paths)} files): {', '.join(preview_list)}")

    manifest_block = "\n".join(header)
    if len(manifest_block) > 4800:
        manifest_block = manifest_block[:4800] + "\n... [Manifest condensed]"

    tokens = {
        t.lower() for t in re.findall(r"[A-Za-z0-9_\-]{3,}", user_prompt)
        if t.lower() not in {"the", "and", "for", "with", "that", "this", "what", "are", "all", "every", "file", "files", "verify", "across", "how", "many", "out"}
    }

    scored = []
    for rname, rpath, clen, content in rows:
        low_key = f"{rname}/{rpath}".lower()
        score = 0
        if rpath in {"Phase1_Supplier_Tracker.md", "Phase1_Supplier_Sourcing_Tracker.md", "Phase2_Integration_Tracker.md"}:
            score += 150
        elif rpath == "MASTER_STATE_INDEX.json":
            score += 110
        elif "merkle_audit_ledger.json" in low_key or rpath.lower() == "readme.md":
            score += 65
        for tok in tokens:
            if tok in low_key:
                score += 45
        # Deduplicate public mirror when identical private repo exists
        if rname.endswith("-public") and rname.replace("-public", "-private") in by_repo:
            if rpath in by_repo[rname.replace("-public", "-private")]:
                score -= 80
        if score > 0:
            scored.append((score, rname, rpath, content))

    scored.sort(key=lambda x: (-x[0], x[1], x[2]))

    deep_blocks = ["\n--- UNTRUNCATED REPOSITORY FILES ---"]
    used = 0
    for score, rname, rpath, content in scored:
        entry = f"\n>>> [{rname}] {rpath} (FULL, {len(content)} chars) <<<\n{content}\n>>> END {rpath} <<<\n"
        if used + len(entry) > max_deep_chars:
            continue
        deep_blocks.append(entry)
        used += len(entry)

    return manifest_block + "\n" + "\n".join(deep_blocks)