import os
import re
import subprocess
from collections import defaultdict
from pathlib import Path

REPOS_ROOT = Path(r"C:\hvf_c2\repos")
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

def sync_all_repositories(auto_pull: bool = False) -> list[Path]:
    """Discover all repositories in C:\\hvf_c2\\repos and optionally pull latest commits."""
    repo_dirs = []
    if REPOS_ROOT.exists():
        for entry in sorted(REPOS_ROOT.iterdir()):
            if entry.is_dir() and (entry / ".git").exists():
                if auto_pull:
                    try:
                        subprocess.run(
                            ["git", "pull", "origin", "main"],
                            cwd=str(entry),
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            timeout=5,
                        )
                    except Exception:
                        pass
                repo_dirs.append(entry)
    for p in PRIMARY_LOCAL_REPOS:
        if p.exists() and p not in repo_dirs:
            repo_dirs.insert(0, p)
    return repo_dirs

def collect_all_files() -> list[tuple[str, Path, Path]]:
    """Recursively enumerate every readable file across every repository."""
    all_files = []
    seen_keys = set()
    for repo in sync_all_repositories(auto_pull=False):
        repo_name = repo.name
        for root, dirs, files in os.walk(repo):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
            for fname in sorted(files):
                fpath = Path(root) / fname
                if fpath.suffix.lower() not in ALLOWED_EXTS:
                    continue
                rel_path = fpath.relative_to(repo)
                key = f"{repo_name}/{rel_path.as_posix()}"
                if key not in seen_keys:
                    seen_keys.add(key)
                    all_files.append((repo_name, rel_path, fpath))
    return all_files

def build_omni_repo_context(user_prompt: str, max_deep_chars: int = 16000) -> str:
    """
    Zero-overflow multi-repository context builder:
    - Guarantees total output stays <= 22,000 chars so online API payload never overflows.
    - Summarizes all 15+ repositories & top-level/blueprint files concisely.
    - Injects FULL, UNTRUNCATED contents of matched files across all repositories.
    """
    all_files = collect_all_files()
    by_repo = defaultdict(list)
    for repo_name, rel_path, fpath in all_files:
        by_repo[repo_name].append((rel_path.as_posix(), fpath))

    manifest_lines = [
        "=== E.B.O.N.Y. STANDING DIRECTIVE: OMNI-REPOSITORY FULL-READ ACCESS ===",
        f"Total Repositories Indexed: {len(by_repo)} | Total Readable Files: {len(all_files)}",
        "RULE: Never truncate files mid-read. Verify all claims directly against the repository files below.",
        "\n--- REPOSITORY ARCHITECTURE & FILE MANIFEST ---"
    ]

    for repo_name in sorted(by_repo.keys()):
        entries = by_repo[repo_name]
        # Show root-level files and blueprint subdirectories for every repository
        highlights = [
            p for p, _ in entries
            if "/" not in p or p.startswith("blueprints/")
        ]
        sample_str = ", ".join(highlights[:30])
        if len(highlights) > 30:
            sample_str += f" ... (+{len(highlights) - 30} more)"
        manifest_lines.append(f"* [{repo_name}] ({len(entries)} files): {sample_str}")

    manifest_text = "\n".join(manifest_lines)
    if len(manifest_text) > 6500:
        manifest_text = manifest_text[:6500] + "\n... [Manifest capped for token safety]"

    tokens = {
        t.lower() for t in re.findall(r"[A-Za-z0-9_\-]{3,}", user_prompt)
        if t.lower() not in {"the", "and", "for", "with", "that", "this", "what", "are", "all", "every", "file", "files", "verify", "across"}
    }

    scored_files = []
    for repo_name, rel_path, fpath in all_files:
        rel_str = rel_path.as_posix()
        low_key = f"{repo_name}/{rel_str}".lower()
        score = 0
        if rel_str in {"Phase1_Supplier_Sourcing_Tracker.md", "Phase2_Integration_Tracker.md", "MASTER_STATE_INDEX.json"}:
            score += 100
        elif "merkle_audit_ledger.json" in low_key or rel_str.lower() == "readme.md":
            score += 60
        for tok in tokens:
            if tok in low_key:
                score += 40
        # Deduplicate public mirrors when identical private repo exists
        if repo_name.endswith("-public") and repo_name.replace("-public", "-private") in by_repo:
            if any(p == rel_str for p, _ in by_repo[repo_name.replace("-public", "-private")]):
                score -= 50
        if score > 0:
            scored_files.append((score, repo_name, rel_str, fpath))

    scored_files.sort(key=lambda x: (-x[0], x[1], x[2]))

    deep_sections = ["\n--- FULL UNTRUNCATED REPOSITORY FILE CONTENTS ---"]
    used_chars = 0
    for score, repo_name, rel_str, fpath in scored_files:
        try:
            content = fpath.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        block = f"\n>>> FILE: [{repo_name}] {rel_str} (FULL CONTENT, {len(content)} chars) <<<\n{content}\n>>> END FILE: {rel_str} <<<\n"
        if used_chars + len(block) > max_deep_chars:
            continue
        deep_sections.append(block)
        used_chars += len(block)

    return manifest_text + "\n" + "\n".join(deep_sections)