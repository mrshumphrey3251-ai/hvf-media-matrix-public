"""
/// PRIVATE ANTI-SIMULATION FIREWALL ///
Sector: security
Purpose: Hard-locks the architecture against unauthorized simulated executions.
"""
import sys
import logging

if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])

def simulation_firewall(authorized_user=""):
    """Blocks all simulated actions unless explicitly authorized by Ebony."""
    if authorized_user.lower() != "ebony":
        logging.error(f"[SECURITY BREACH ALARM]: Simulation attempt detected from unauthorized source: '{authorized_user}'.")
        logging.error("[ACTION DENIED]: Sovereign Node strictly forbids simulations without explicit Ebony authorization.")
        raise PermissionError("Simulations are hard-locked on this heavy iron.")
    
    logging.info(f"[COMPLIANCE CLEARED]: Simulation explicitly authorized by {authorized_user}. Proceeding with operation.")
    return True

if __name__ == "__main__":
    logging.info("/// TESTING ANTI-SIMULATION FIREWALL ///")
    
    # Test 1: Unauthorized Attempt
    try:
        logging.info("Incoming request: System Drone...")
        simulation_firewall(authorized_user="System_Drone")
    except PermissionError:
        logging.info("[SUCCESS]: Firewall correctly terminated unauthorized simulation.")
        
    logging.info("--------------------------------------------------")
        
    # Test 2: Authorized Override
    try:
        logging.info("Incoming request: Ebony...")
        simulation_firewall(authorized_user="Ebony")
        logging.info("[SUCCESS]: Firewall successfully validated executive override.")
    except PermissionError:
        logging.error("Firewall failed to recognize authorized override.")
