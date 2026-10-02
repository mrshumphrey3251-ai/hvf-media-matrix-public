"""
/// PRIVATE SECURITY DAEMON (V2: UNIFIED MASTER ORCHESTRATOR) ///
Sector: security
Purpose: Automates active intrusion detection, IAM authentication, and cryptographic ledger sweeps.
"""
import os
import sys
import logging

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from hvf_compliance_guard import simulation_firewall
from access_control import verify_executive_clearance
from encryption_engine import execute_ledger_lockdown
from intrusion_detector import scan_perimeter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])

def run_security_sweep():
    logging.info("/// MASTER SECURITY DAEMON ONLINE (V2) ///")
    
    logging.info("[DAEMON]: Initiating perimeter threat scan...")
    scan_perimeter()
    
    logging.info("[DAEMON]: Initiating automated IAM verification...")
    is_authorized = verify_executive_clearance(user_id="Ebony", security_token="AUTH-BETA-002")
    
    if is_authorized:
        logging.info("[DAEMON]: Authorization confirmed. Executing zero-trust encryption sweep...")
        execute_ledger_lockdown()
    else:
        logging.error("[DAEMON]: Authorization failed. Locking down infrastructure controls.")
        
    logging.info("/// SECURITY SWEEP COMPLETE ///")

if __name__ == "__main__":
    simulation_firewall(authorized_user="Ebony")
    run_security_sweep()
