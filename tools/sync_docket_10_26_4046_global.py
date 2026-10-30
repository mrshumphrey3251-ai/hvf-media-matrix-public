#!/usr/bin/env python3
"""
HVF Project Ebony v8.0.0 — Global Docket 10-26-4046 Repository Synchronizer
Author: Jeffery Humphrey, Founder, President & CEO, Humphrey Virtual Farms LLC (CAGE: 1AHA8)
Purpose: Scans all .md, .py, .json, .txt, and .html files across Private and Public
         repositories to replace superseded docket numbers (10-26-3976 / 10-26-4014)
         with active TSM Docket 10-26-4046 and lock in the 04:24 (264.23s) SHA-256 hash.
Security & Extensibility: 100% Offline Loopback, Zero Cloud, Hook-Extensible Class Architecture.
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Any


class GlobalDocketSynchronizer:
    ACTIVE_DOCKET: str = "10-26-4046"
    ACTIVE_DOCKET_UNDERSCORE: str = "10_26_4046"
    MASTER_VIDEO_SHA256: str = "c597865785eae6fdad6fdf6803a2710aaa0fb5c2fa28fe512b6ed76ef8b7a7fd"
    MASTER_DURATION_SEC: str = "264.23"
    MASTER_DURATION_MMSS: str = "04:24"

    TARGET_EXTENSIONS = {".md", ".py", ".json", ".txt", ".html", ".yaml", ".yml"}
    SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules"}

    REPLACEMENTS = [
        ("10-26-4014", "10-26-4046"),
        ("10_26_4014", "10_26_4046"),
        ("10-26-3976", "10-26-4046"),
        ("10_26_3976", "10_26_4046"),
        ("605c6c3e77ddabb3d151e2c828ab7f69d779a1f7a4de73ba073386940f342d7b", "c597865785eae6fdad6fdf6803a2710aaa0fb5c2fa28fe512b6ed76ef8b7a7fd"),
        ("1c3804f4473fa3f2946e1711c592f421ffccca37ee5a04fe13642ec5f8864a19", "c597865785eae6fdad6fdf6803a2710aaa0fb5c2fa28fe512b6ed76ef8b7a7fd"),
        ("TSM REV V.10 RESUBMISSION (SUPERSEDING 9-26-3703)", "DOCKET 10-26-4046 (SUPERSEDING 9-26-3703 | TRL 4 -> TRL 6)"),
    ]

    def __init__(self, repo_paths: List[Path]) -> None:
        self.repo_paths = [p for p in repo_paths if p.exists()]

    def sync_repository(self, repo_root: Path) -> Dict[str, Any]:
        updated_files: List[str] = []
        total_scanned = 0

        for path in repo_root.rglob("*"):
            if not path.is_file():
                continue
            if any(part in self.SKIP_DIRS for part in path.parts):
                continue
            if path.name == "sync_docket_10_26_4046_global.py":
                continue
            if path.suffix.lower() not in self.TARGET_EXTENSIONS:
                continue

            total_scanned += 1
            try:
                original = path.read_text(encoding="utf-8")
            except Exception:
                continue

            modified = original
            for old_str, new_str in self.REPLACEMENTS:
                modified = modified.replace(old_str, new_str)

            if modified != original:
                path.write_text(modified, encoding="utf-8")
                updated_files.append(str(path.relative_to(repo_root)))

        # Ensure the docket-specific MP4 alias exists
        master_mp4 = repo_root / "c2_cockpit/proposals/EBONY_V8_CDAO_RUBRIC_VERIFICATION_20261028.mp4"
        docket_mp4 = repo_root / "c2_cockpit/proposals/PROJECT_EBONY_TRADEWINDS_RESUBMISSION_10_26_4046.mp4"
        old_docket_mp4 = repo_root / "c2_cockpit/proposals/PROJECT_EBONY_TRADEWINDS_RESUBMISSION_10_26_3976.mp4"
        if master_mp4.exists():
            shutil.copy2(master_mp4, docket_mp4)
            if old_docket_mp4.exists():
                try:
                    old_docket_mp4.unlink()
                except Exception:
                    pass

        return {
            "repository": str(repo_root),
            "files_scanned": total_scanned,
            "files_updated_count": len(updated_files),
            "files_updated": updated_files[:40],
        }

    def run_all(self) -> List[Dict[str, Any]]:
        results = []
        for repo in self.repo_paths:
            results.append(self.sync_repository(repo))
        return results


if __name__ == "__main__":
    priv = Path(r"C:\hvf_c2\hvf-media-matrix-private")
    pub = Path(r"C:\hvf_c2\hvf-media-matrix-public")
    syncer = GlobalDocketSynchronizer([priv, pub])
    report = syncer.run_all()
    print(json.dumps(report, indent=2))
