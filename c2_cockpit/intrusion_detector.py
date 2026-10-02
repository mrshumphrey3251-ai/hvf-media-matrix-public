"""
/// PRIVATE INTRUSION DETECTOR (V1: PERIMETER DEFENSE) ///
Sector: security
Purpose: Monitors access logs for unauthorized breach attempts and triggers automated defensive countermeasures.
"""
import os
import sys
import logging

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from hvf_compliance_guard import simulation_firewall

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])

def scan_perimeter():
    logging.info("/// INITIATING PERIMETER THREAT SCAN ///")
    
    # Simulating the ingestion of live network traffic logs
    network_events = [
        {"ip": "192.168.1.15", "status": "AUTH_SUCCESS"},
        {"ip": "10.0.0.42", "status": "AUTH_FAILED"},
        {"ip": "10.0.0.42", "status": "AUTH_FAILED"},
        {"ip": "10.0.0.42", "status": "AUTH_FAILED"}
    ]
    
    threat_detected = False
    failed_attempts = 0
    hostile_ip = ""

    for event in network_events:
        if event["status"] == "AUTH_FAILED":
            failed_attempts += 1
            hostile_ip = event["ip"]
            if failed_attempts >= 3:
                threat_detected = True
                break
                
    if threat_detected:
        logging.error(f"[BREACH ATTEMPT DETECTED]: Multiple failed logins from {hostile_ip}.")
        logging.info(f"[COUNTERMEASURE DEPLOYED]: IP {hostile_ip} blacklisted. Perimeter secured.")
    else:
        logging.info("[PERIMETER SECURE]: No hostile anomalies detected.")

if __name__ == "__main__":
    simulation_firewall(authorized_user="Ebony")
    scan_perimeter()
