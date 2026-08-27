"""
/// PRIVATE API CONTRACT FORGE ///
Sector: infrastructure
Purpose: Generates the master api_contracts.json consumed by downstream services.
"""
import json
import pathlib
import sys
import logging

if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])

def generate_contracts():
    logging.info("/// FORGING MASTER API CONTRACTS ///")
    contracts = [
        {
            "service": "MediaIngest",
            "base_url": "https://ingest.hvf.io/v1",
            "auth": "oauth2_client_credentials",
            "rate_limit": 1200
        }
    ]
    
    file_path = pathlib.Path(__file__).parent / 'api_contracts.json'
    file_path.write_text(json.dumps(contracts, indent=2))
    logging.info(f"✅ api_contracts.json created at -> {file_path}")

if __name__ == "__main__":
    generate_contracts()
