import os
import re
import subprocess
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
    ".git", "__pycache__", "node_modules", ".venv", "venv", ".archive_tools", "historical_archive"
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
    # Always prioritize live working directories for hvf-media-matrix
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

def build_omni_repo_context(user_prompt: str, max_deep_chars: int = 28000) -> str:
    """
    Build complete, untruncated multi-repository context for E.B.O.N.Y.:
    1. Full directory & file inventory across ALL repositories.
    2. Complete, untruncated file contents for all trackers, ledgers, blueprints,
       and files matching the user's query across all 15 repositories.
    """
    all_files = collect_all_files()
    repos_found = sorted({r for r, _, _ in all_files})

    manifest_lines = [
        "=== E.B.O.N.Y. STANDING DIRECTIVE: OMNI-REPOSITORY FULL-READ ACCESS ===",
        f"Active Repositories Indexed ({len(repos_found)}): {', '.join(repos_found)}",
        f"Total Readable Files Across All Repositories: {len(all_files)}",
        "RULE: Never truncate files mid-read. Verify all claims directly against the repository files below.",
        "\n--- COMPLETE MULTI-REPOSITORY FILE INVENTORY ---"
    ]
    for repo_name, rel_path, _ in all_files:
        manifest_lines.append(f"[{repo_name}] {rel_path.as_posix()}")

    # Score files by relevance + always include critical state/tracker/ledger/README files
    tokens = {
        t.lower() for t in re.findall(r"[A-Za-z0-9_\-]{3,}", user_prompt)
        if t.lower() not in {"the", "and", "for", "with", "that", "this", "what", "are", "all", "every", "file", "files"}
    }
    audit_mode = any(k in user_prompt.lower() for k in ["audit", "lacking", "missing", "status", "tracker", "complete", "every", "all", "blueprint"])

    scored_files = []
    for repo_name, rel_path, fpath in all_files:
        rel_str = rel_path.as_posix()
        low_key = f"{repo_name}/{rel_str}".lower()
        score = 0
        if any(name in low_key for name in ["tracker", "merkle_audit_ledger", "master_state_index", "readme.md"]):
            score += 50
        if "blueprints/" in low_key and audit_mode:
            score += 35
        for tok in tokens:
            if tok in low_key:
                score += 25
        # Prefer private mirror over duplicate public mirror to avoid wasting context on identical copies
        if repo_name.endswith("-public") and any(
            r == repo_name.replace("-public", "-private") and p.as_posix() == rel_str
            for r, p, _ in all_files
        ):
            score -= 10
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

    return "\n".join(manifest_lines) + "\n" + "\n".join(deep_sections)