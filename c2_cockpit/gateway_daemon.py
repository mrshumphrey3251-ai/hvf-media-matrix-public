"""
/// PRIVATE GATEWAY DAEMON (V1: EDGE ORCHESTRATOR) ///
Sector: gateway
Purpose: Automates rate limiting and API client authentication at the network edge.
"""
import os
import sys
import logging

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from hvf_compliance_guard import simulation_firewall
from rate_limiter import enforce_quota
from api_gateway import process_client_request

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])

def run_gateway_loop(client_id, api_key, request_count):
    logging.info("/// MASTER GATEWAY DAEMON ONLINE ///")
    
    logging.info("[DAEMON]: Initiating edge rate limit check...")
    is_safe = enforce_quota(client_id=client_id, request_count=request_count)
    
    if is_safe:
        logging.info("[DAEMON]: Traffic optimal. Passing to authentication matrix...")
        process_client_request(client_id=client_id, api_key=api_key)
    else:
        logging.error("[DAEMON]: Edge defense engaged. Connection terminated before reaching core infrastructure.")
        
    logging.info("/// GATEWAY CYCLE COMPLETE ///")

if __name__ == "__main__":
    simulation_firewall(authorized_user="Ebony")
    # Simulating a legitimate, optimal request volume
    run_gateway_loop(client_id="CLIENT-OMEGA-99", api_key="HD-KEY-778899-SECURE", request_count=450)
