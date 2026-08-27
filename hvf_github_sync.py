"""
/// DUAL-VAULT SYNC ENGINE ///
Sector: ROOT
Purpose: Autonomously stage, commit, and push private and public repositories to remote GitHub vaults.
"""
import os
import sys
import subprocess
import logging
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, f"github_sync_{datetime.utcnow():%Y%m%d}.log")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.FileHandler(log_file, encoding="utf-8"), logging.StreamHandler(sys.stdout)])

def run_git_command(command, repo_path):
    try:
        result = subprocess.run(command, cwd=repo_path, capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, result.stderr.strip()
    except Exception as e:
        return False, str(e)

def sync_repository(repo_path, repo_name):
    logging.info(f"=== INITIATING GITHUB SYNC: {repo_name} ===")
    
    if not os.path.exists(os.path.join(repo_path, ".git")):
        logging.error(f"[SYNC HALT]: Git is not initialized in {repo_path}")
        return

    # Stage all changes
    success, out = run_git_command("git add .", repo_path)
    if not success:
        logging.error(f"[{repo_name}] Failed to stage files: {out}")
        return

    # Check if there are changes to commit
    status_success, status_out = run_git_command("git status --porcelain", repo_path)
    if not status_out:
        logging.info(f"[{repo_name}] No new changes detected. Vault is already synchronized.")
        return

    # Commit changes
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    commit_msg = f"Omni-Matrix Update: Executive Architecture Deployment [{timestamp}]"
    success, out = run_git_command(f'git commit -m "{commit_msg}"', repo_path)
    if success:
        logging.info(f"[{repo_name}] Cryptographic commit secured: {commit_msg}")
    else:
        logging.error(f"[{repo_name}] Commit failed: {out}")
        return

    # Push to remote
    logging.info(f"[{repo_name}] Establishing secure uplink to remote GitHub vault...")
    success, out = run_git_command("git push", repo_path)
    if success:
        logging.info(f"[{repo_name}] [UPLINK SUCCESS]: Payload successfully delivered to remote repository.")
    else:
        logging.error(f"[{repo_name}] [UPLINK FAILED]: {out}")

def execute_dual_sync():
    logging.info("/// INITIATING DUAL-VAULT SYNC PROTOCOL ///")
    
    private_repo = BASE_DIR
    public_repo = os.path.abspath(os.path.join(BASE_DIR, "..", "hvf-media-matrix-public"))
    
    sync_repository(private_repo, "PRIVATE VAULT")
    sync_repository(public_repo, "PUBLIC BLUEPRINTS")
    
    logging.info("/// DUAL-VAULT SYNC PROTOCOL COMPLETE ///")

if __name__ == "__main__":
    execute_dual_sync()
