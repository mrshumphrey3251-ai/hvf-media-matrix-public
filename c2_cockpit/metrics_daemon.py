"""
/// PRIVATE METRICS DAEMON (V1: MASTER ORCHESTRATOR) ///
Sector: metrics
Purpose: Continuously automates telemetry extraction, threshold evaluation, and ledger logging.
"""
import os
import sys
import time
import logging

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from hvf_compliance_guard import simulation_firewall
from telemetry_matrix import execute_performance_sweep
from alert_protocol import evaluate_threshold
from performance_logger import write_to_ledger

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])

def run_daemon_loop():
    logging.info("/// MASTER METRICS DAEMON ONLINE ///")
    
    # Simulating a single automated cycle for structural testing
    logging.info("[DAEMON]: Extracting live telemetry...")
    current_cpu = 48.5
    current_mem = 62.1
    
    logging.info("[DAEMON]: Evaluating thresholds...")
    is_stable = evaluate_threshold(cpu_load=current_cpu, memory_load=current_mem)
    
    status = "OPTIMAL" if is_stable else "CRITICAL"
    
    logging.info("[DAEMON]: Committing to historical ledger...")
    write_to_ledger(cpu_load=current_cpu, memory_load=current_mem, status=status)
    
    logging.info("/// DAEMON CYCLE COMPLETE ///")

if __name__ == "__main__":
    simulation_firewall(authorized_user="Ebony")
    run_daemon_loop()
