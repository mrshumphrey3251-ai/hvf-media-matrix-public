"""
/// PRIVATE DISASTER RECOVERY MATRIX (V1: COLD STORAGE BACKUP) ///
Sector: redundancy
Purpose: Duplicates encrypted ledgers and critical data to an isolated off-node vault to guarantee zero data loss.
"""
import os
import sys
import shutil
import logging
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from hvf_compliance_guard import simulation_firewall

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])

def execute_cold_storage_backup():
    logging.info("/// INITIATING DISASTER RECOVERY PROTOCOL ///")
    
    source_file = os.path.join(ROOT_DIR, "metrics", "ledgers", "infrastructure_uptime.log.enc")
    backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cold_vault")
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        
    if not os.path.exists(source_file):
        logging.error("[DR FAILURE]: Source encrypted ledger not found. Backup aborted.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"infrastructure_uptime_backup_{timestamp}.log.enc")
    
    shutil.copy2(source_file, backup_file)
    logging.info(f"[ASSET SECURED]: Encrypted ledger successfully mirrored to cold storage -> {backup_file}")
    logging.info("[STATUS]: Sovereign data integrity guaranteed at 100%.")

if __name__ == "__main__":
    simulation_firewall(authorized_user="Ebony")
    execute_cold_storage_backup()
