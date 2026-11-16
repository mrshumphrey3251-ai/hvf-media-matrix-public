"""
HVF Sovereign Private-to-Public OPSEC Release Gatekeeper (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)
Validates AST syntax, enforces strict OPSEC redaction across public deliverables,
and mirrors approved modules/audit receipts from hvf-media-matrix-private to
hvf-media-matrix-public with zero secret leakage.
"""
import argparse
import ast
from pathlib import Path
import re
import sys
from typing import List, Tuple

PRIVATE_ROOT = Path(r"C:\hvf_c2\hvf-media-matrix-private")
PUBLIC_ROOT = Path(r"C:\hvf_c2\hvf-media-matrix-public")

# Mandatory OPSEC redaction rules applied to every text/code file synced to public
REDACTION_RULES: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"Humphrey J\. Miller"), "Jeffery Humphrey"),
    (re.compile(r"humphrey\.miller@hvf\.io", re.I), "humphreyvirtualfarm@gmail.com"),
    (re.compile(r"\$\d+M in seed & series-A funding", re.I), "sovereign, self-funded architecture"),
    (re.compile(r"\b100\.87\.162\.117\b"), "127.0.0.1"),
    (re.compile(r"EBONY_TIER_1_CEO[A-Z0-9_]*"), "EXECUTIVE_ADMIN_ROLE"),
    (re.compile(r"C:\\hvf_c2\\hvf-media-matrix-private", re.I), r"C:\hvf_c2\hvf-media-matrix-public"),
]

# Hard-block patterns that must NEVER appear in public repository files
FORBIDDEN_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("Legacy Identity Leak", re.compile(r"Humphrey J\. Miller")),
    ("Legacy Email Leak", re.compile(r"humphrey\.miller@hvf\.io", re.I)),
    ("Private Tailscale IP", re.compile(r"\b100\.87\.162\.117\b")),
    ("Internal Role Token", re.compile(r"EBONY_TIER_1_CEO")),
    ("Private API Key Prefix", re.compile(r"\b(gsk_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,})\b")),
    ("Fernet Key Material", re.compile(r"gAAAAAB[A-Za-z0-9_\-=]{30,}")),
]

# Allowlisted relative paths eligible for automated Private -> Public promotion
DEFAULT_SYNC_ALLOWLIST = [
    "sitecustomize.py",
    "c2_cockpit/vector_cache_gateway.py",
    "scripts/sync_sovereign_release.py",
]


def sanitize_and_validate(rel_path: str, raw_text: str) -> str:
    """Apply OPSEC redactions, verify zero forbidden leaks, and validate Python AST."""
    cleaned = raw_text
    for pattern, replacement in REDACTION_RULES:
        cleaned = pattern.sub(lambda _m, r=replacement: r, cleaned)

    for label, forbidden_rx in FORBIDDEN_PATTERNS:
        if forbidden_rx.search(cleaned):
            raise ValueError(f"[OPSEC BLOCK] {rel_path} failed '{label}' check after redaction!")

    if rel_path.endswith(".py"):
        try:
            ast.parse(cleaned)
        except SyntaxError as exc:
            raise ValueError(f"[AST BLOCK] {rel_path} failed Python AST check: {exc}") from exc

    return cleaned


def sync_files(rel_paths: List[str], dry_run: bool = False) -> int:
    """Sync allowlisted files from PRIVATE_ROOT to PUBLIC_ROOT with OPSEC & AST gates."""
    synced = 0
    for rel in rel_paths:
        src = PRIVATE_ROOT / rel
        if not src.exists():
            print(f"[SKIP] Missing in private repo: {rel}")
            continue
        raw = src.read_text(encoding="utf-8")
        cleaned = sanitize_and_validate(rel, raw)
        dst = PUBLIC_ROOT / rel
        if not dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(cleaned, encoding="utf-8", newline="\n")
        synced += 1
        mode = "DRY-RUN VERIFIED" if dry_run else "SYNCED & REDACTED"
        print(f"[PASS] {mode}: {rel}")
    return synced


def main() -> None:
    parser = argparse.ArgumentParser(description="HVF Sovereign Private-to-Public OPSEC Release Gatekeeper")
    parser.add_argument("--dry-run", action="store_true", help="Validate AST and OPSEC gates without writing files")
    parser.add_argument("files", nargs="*", help="Optional relative file paths to sync (defaults to core allowlist)")
    args = parser.parse_args()

    targets = args.files if args.files else DEFAULT_SYNC_ALLOWLIST
    count = sync_files(targets, dry_run=args.dry_run)
    print(f"[+] Gatekeeper Complete: {count}/{len(targets)} deliverables passed AST + OPSEC verification (0 leaks).")


if __name__ == "__main__":
    main()