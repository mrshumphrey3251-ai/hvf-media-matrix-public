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
    """Recursively index every readable file across all repositories into SQLite with zero truncation."""
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

def build_omni_repo_context(user_prompt: str, max_deep_chars: int = 15500) -> str:
    """
    Deterministic multi-repository context builder:
    - Reports exact file counts for EVERY repository (zero undisclosed counts).
    - Lists EVERY blueprint specification directory under blueprints/.
    - Injects full, untruncated trackers and query-matched files within safe payload bounds.
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
        f"Total Indexed Repositories: {repo_count} | Total Readable Files: {file_count}",
        "DIRECTIVE: Speak with absolute certainty. Never hedge or say 'technically'. Verify all facts directly below."
    ]

    for rname in sorted(by_repo.keys()):
        paths = by_repo[rname]
        bp_files = [p for p in paths if p.startswith("blueprints/")]
        if bp_files:
            bp_list = ", ".join(p.split("/", 1)[1] for p in bp_files)
            header.append(f"* {rname}: {len(paths)} files | blueprints ({len(bp_files)}): {bp_list}")
        else:
            root_sample = ", ".join([p for p in paths if "/" not in p][:5])
            header.append(f"* {rname}: {len(paths)} files | root: {root_sample}")

    manifest_block = "\n".join(header)

    tokens = {
        t.lower() for t in re.findall(r"[A-Za-z0-9_\-]{3,}", user_prompt)
        if t.lower() not in {"the", "and", "for", "with", "that", "this", "what", "are", "all", "every", "file", "files", "verify", "across", "how", "many", "out"}
    }

    scored = []
    for rname, rpath, clen, content in rows:
        low_key = f"{rname}/{rpath}".lower()
        score = 0
        if "phase3" in low_key and "tracker" in low_key:
            score += 170
        elif "phase2" in low_key and "tracker" in low_key:
            score += 160
        elif "phase1" in low_key and "tracker" in low_key:
            score += 155
        elif rpath == "MASTER_STATE_INDEX.json":
            score += 110
        elif "merkle_audit_ledger.json" in low_key or rpath.lower() == "readme.md":
            score += 65
        for tok in tokens:
            if tok in low_key:
                score += 50
        if rname.endswith("-public") and rname.replace("-public", "-private") in by_repo:
            if rpath in by_repo[rname.replace("-public", "-private")]:
                score -= 90
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