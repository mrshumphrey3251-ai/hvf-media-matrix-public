"""
/// PRIVATE ADVANCED RECONNAISSANCE NODE (STEALTH UPGRADE) ///
Sector: recon_intel
Purpose: Autonomously extracts live tactical intelligence using WAF-bypass headers.
"""
import os
import sys
import logging
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTEL_DIR = os.path.join(BASE_DIR, "..", "content_vault", "intel_drops")
os.makedirs(INTEL_DIR, exist_ok=True)

def execute_recon_sweep(target_url="https://feeds.feedburner.com/TheHackersNews"):
    logging.info("/// DEPLOYING STEALTH RECON SCOUT ///")
    logging.info(f"Targeting Intelligence Endpoint: {target_url}")
    
    try:
        # Stealth Matrix: Bypasses standard WAF bot-defenses by mimicking a live executive workstation.
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }
        
        response = requests.get(target_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            logging.info("[UPLINK SECURED]: Live intelligence stream intercepted.")
            root = ET.fromstring(response.content)
            
            intel_data = []
            # Parse standard RSS items universally
            for item in root.findall(".//item")[:3]:
                title = item.find("title").text if item.find("title") is not None else "Unknown Threat"
                pubDate = item.find("pubDate").text if item.find("pubDate") is not None else "Unknown Date"
                intel_data.append(f"- {title} ({pubDate})")
            
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(INTEL_DIR, f"tactical_intel_{timestamp}.txt")
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("/// LIVE MARKET & THREAT INTELLIGENCE ///\n\n")
                f.write("\n".join(intel_data))
            
            logging.info(f"[INTEL ACQUIRED]: Extracted 3 high-level intelligence vectors.")
            logging.info(f"[VAULTED]: Intelligence dropped at -> {filepath}")
        else:
            logging.error(f"[RECON FAILED]: Endpoint returned status code {response.status_code}")
            
    except Exception as e:
        logging.error(f"[SYSTEM MISFIRE]: Recon scout encountered an error: {e}")

if __name__ == "__main__":
    execute_recon_sweep()
