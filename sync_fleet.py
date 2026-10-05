import os
import subprocess
from pathlib import Path

base_dir = Path(r"C:\HVF_Repos")
base_dir.mkdir(parents=True, exist_ok=True)

fleet_repos = [
    "hvf-media-matrix-public",
    "hvf-media-matrix-private",
    "ultimate-law-private",
    "ultimate-law-public",
    "hvf-ebony-command",
    "ebony-chronos-public",
    "ebony-chronos-private",
    "hvf-ebony-showcase",
    "hvf-signallink-dmz",
    "HVF_Matrix_Core",
    "project-ebony-spec",
    "hvf-intel-scraper-public",
    "hvf-intel-scraper",
    "Kinetic_Guillotine",
    "HVF_NEXUS_CORE_V2_PUBLIC",
    "HVF_NEXUS_CORE_V2_PRIVATE",
    "hvf-bible-game-core",
    "HVF_NEXUS_CORE_V2",
    "HVF_NEXUS_CORE_V2_INTERNAL",
    "HVF_NEXUS_CORE",
    "hvf-nexus"
]

print(f"[*] Auditing local synchronization of {len(fleet_repos)} fleet repositories under {base_dir}...\n")

for repo_name in fleet_repos:
    target_path = base_dir / repo_name
    if target_path.exists():
        print(f"[+] Found locally: {repo_name} -> Pulling latest changes...")
        try:
            res = subprocess.run(["git", "-C", str(target_path), "pull"], capture_output=True, text=True)
            print(f"    {res.stdout.strip() or res.stderr.strip() or 'OK'}")
        except Exception as e:
            print(f"    [!] Git pull error on {repo_name}: {e}")
    else:
        print(f"[-] Missing locally: {repo_name} -> Attempting clone...")
        try:
            res = subprocess.run(["gh", "repo", "clone", f"HumphreyVirtualFarm/{repo_name}", str(target_path)], capture_output=True, text=True)
            if res.returncode == 0:
                print(f"    [+] Cloned successfully via gh CLI: {repo_name}")
            else:
                res2 = subprocess.run(["git", "clone", f"https://github.com/HumphreyVirtualFarm/{repo_name}.git", str(target_path)], capture_output=True, text=True)
                if res2.returncode == 0:
                    print(f"    [+] Cloned successfully via git clone: {repo_name}")
                else:
                    print(f"    [!] Clone failed for {repo_name}: {res2.stderr.strip()}")
        except Exception as e:
            print(f"    [!] Clone exception for {repo_name}: {e}")
