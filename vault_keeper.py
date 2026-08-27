"""
/// LOCAL CREDENTIAL VAULT KEEPER ///
Purpose: Backs up .env credentials locally; restores them instantly if .env is missing or altered.
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
BACKUP_PATH = os.path.join(BASE_DIR, ".env.vault_backup")

def backup():
    if not os.path.exists(ENV_PATH):
        print("[VAULT]: No .env file found to backup.")
        return
    with open(ENV_PATH, "r", encoding="utf-8") as src, open(BACKUP_PATH, "w", encoding="utf-8") as dst:
        dst.write(src.read())
    print(f"[VAULT]: Local backup secured successfully -> {BACKUP_PATH}")

def restore():
    if not os.path.exists(BACKUP_PATH):
        print("[VAULT]: No backup file found to restore from.")
        return
    with open(BACKUP_PATH, "r", encoding="utf-8") as src, open(ENV_PATH, "w", encoding="utf-8") as dst:
        dst.write(src.read())
    print(f"[VAULT]: .env restored successfully from -> {BACKUP_PATH}")

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "backup"
    if action == "restore":
        restore()
    else:
        backup()
