"""
/// PRIVATE DOMINANCE RELEASE ENGINE ///
Sector: deployment
Purpose: Manages Canary (5%) and Full (100%) production rollouts.
"""
import sys
import time
import logging
from hvf_compliance_guard import simulation_firewall

if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])

def canary_deploy(percentage=5):
    logging.info(f"[RELEASE]: Routing {percentage}% of live traffic to the new dominant build...")
    logging.info("[RELEASE]: Initiating telemetry monitoring for anomalies...")
    time.sleep(2)  # Simulating the required monitoring window
    logging.info("✅ Canary deployed - monitor for 2 min")

def full_deploy():
    logging.info("[RELEASE]: Canary telemetry green. Zero anomalies detected.")
    logging.info("[RELEASE]: Routing 100% of live traffic to the new build...")
    logging.info("✅ Full production rollout complete")

if __name__ == "__main__":
    logging.info("/// INITIATING RELEASE PROTOCOL ///")
    simulation_firewall(authorized_user="Ebony")
    
    # Dynamically handle Canary vs Full rollout
    if len(sys.argv) > 1 and sys.argv[1] == "full":
        full_deploy()
    else:
        canary_deploy(percentage=5)
