"""
/// PRIVATE BROADCAST ENGINE (LIVE-FIRE PUBLISHING NODE) ///
Sector: global_comms
Purpose: Sweep outbox, format JSON payloads, and force-publish to the external network.
"""
import os
import sys
import logging
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')

load_dotenv(override=True)
LINKEDIN_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_URN = os.getenv("LINKEDIN_AUTHOR_URN")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")
OUTBOX_DIR = os.path.join(BASE_DIR, "..", "content_vault", "outbox")
os.makedirs(OUTBOX_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, f"broadcast_engine_live_{datetime.utcnow():%Y%m%d}.log")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.FileHandler(log_file, encoding="utf-8"), logging.StreamHandler(sys.stdout)])

def stage_test_payload():
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(OUTBOX_DIR, f"outbound_test_{timestamp}.txt")
    payload = "Initiating live-fire test from sovereign edge node. Zero-Trust Omni-Matrix is fully operational. #SovereignCompute #ExecutiveAI"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(payload)
    logging.info(f"[AUTO-STAGE]: Fresh payload chambered -> {filepath}")
    return [f"outbound_test_{timestamp}.txt"]

def deploy_outbox():
    logging.info("Initiating sweep of local outbox for staged broadcasts...")
    staged_files = [f for f in os.listdir(OUTBOX_DIR) if f.endswith('.txt') and not f.endswith('.locked') and not f.endswith('.deployed')]
    
    if not staged_files:
        logging.warning("Outbox is empty. Chambering a fresh test payload...")
        staged_files = stage_test_payload()

    if not LINKEDIN_TOKEN or not LINKEDIN_URN:
        logging.warning("[SYSTEM HALT]: Live API key or URN missing from the vault.")
        return

    logging.info(f"Detected {len(staged_files)} staged payloads. Engaging deployment matrix...")
    headers = {
        "Authorization": f"Bearer {LINKEDIN_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }
    
    for file in staged_files:
        filepath = os.path.join(OUTBOX_DIR, file)
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        logging.info(f"Firing payload [{file}] to external LinkedIn Matrix...")
        
        post_data = {
            "author": LINKEDIN_URN,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": content},
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }

        try:
            url = "https://api.linkedin.com/v2/ugcPosts"
            response = requests.post(url, headers=headers, json=post_data, timeout=10)
            
            if response.status_code == 201:
                logging.info(f"[NETWORK SUCCESS]: Payload successfully published to timeline. Code 201.")
                os.rename(filepath, filepath + ".deployed")
            elif response.status_code == 403:
                logging.warning(f"[API SECURE DENIAL]: Token lacks publishing scope. Quarantining payload.")
                os.rename(filepath, filepath + ".locked")
            else:
                logging.error(f"[API ERROR]: Server returned Code {response.status_code}. Response: {response.text}")
                os.rename(filepath, filepath + ".locked")
        except Exception as e:
            logging.error(f"[NETWORK FAILURE]: {e}")

if __name__ == "__main__":
    deploy_outbox()
