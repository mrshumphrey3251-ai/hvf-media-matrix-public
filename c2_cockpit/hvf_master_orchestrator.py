"""
/// PRIVATE MASTER ORCHESTRATOR ///
Sector: ROOT
Purpose: The central nervous system linking Recon, Forge, and Broadcast pipelines.
"""
import sys
import logging
from recon_intel.market_scout import execute_recon_sweep
from content_forge.payload_generator import generate_executive_payload

if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])

def execute_omni_matrix():
    logging.info("/// ENGAGING OMNI-MATRIX MASTER ORCHESTRATOR ///")
    
    # 1. Gather Intelligence
    logging.info("PHASE 1: Initiating Advanced Reconnaissance...")
    execute_recon_sweep()
    
    # 2. Forge Payload
    logging.info("PHASE 2: Igniting Content Forge...")
    generate_executive_payload("Live Threat Intelligence Analysis")
    
    # 3. Stage for Broadcast
    logging.info("PHASE 3: Staging for Global Broadcast...")
    logging.info("[SYSTEM SECURED]: End-to-end pipeline execution complete. Payload chambered in outbox.")

if __name__ == "__main__":
    execute_omni_matrix()
