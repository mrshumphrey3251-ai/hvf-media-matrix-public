import json
import subprocess
from pathlib import Path

repos = [
    Path(r"C:\hvf_c2\hvf-media-matrix-private"),
    Path(r"C:\hvf_c2\hvf-media-matrix-public"),
]

skip_dirs = {".git", "__pycache__", ".venv", "venv", "node_modules"}
report = []

for repo in repos:
    if not repo.exists():
        continue
    renamed = []
    for path in list(repo.rglob("*")):
        if not path.is_file():
            continue
        if any(part in skip_dirs for part in path.parts):
            continue
        new_name = (
            path.name
            .replace("10-26-4046", "10-26-4046")
            .replace("10_26_4046", "10_26_4046")
            .replace("10-26-4046", "10-26-4046")
            .replace("10_26_4046", "10_26_4046")
        )
        if new_name != path.name:
            target = path.with_name(new_name)
            if target.exists():
                target.unlink()
            path.rename(target)
            renamed.append(f"{path.relative_to(repo)} -> {target.relative_to(repo)}")
    report.append({"repository": str(repo), "renamed_files": renamed})

print(json.dumps(report, indent=2))
