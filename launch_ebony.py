"""
Project Ebony: Sovereign SCADA Defense Matrix -- Operational Live Launcher
Initializes the bare-metal defense pipeline, spins up the air-gapped HMI cockpit,
and binds the local HTTP telemetry daemon on production port 8088.
DFARS 252.227-7018 Compliant Architecture.
"""

import os
import sys
import time
import logging
import webbrowser
from datetime import datetime, timezone

# Add repository root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from scada_engine.hvf_defense_pipeline import HVFDefensePipeline
from scada_engine.hvf_telemetry_bridge import HVFTelemetryBridge

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [EBONY-CORE] %(message)s"
)

def launch():
    print("=" * 64)
    print("  PROJECT EBONY // SOVEREIGN SCADA DEFENSE MATRIX")
    print("  Contractor: Humphrey Virtual Farms LLC | CAGE: 1AHA8")
    print("  Compliance: DFARS 252.227-7018 / Oklahoma HB 2992")
    print("  Classification: Commercial Technical Data Rights (Private Expense)")
    print("=" * 64)

    logging.info("Initializing bare-metal defense pipeline engine...")
    db_file = os.path.join(os.path.dirname(__file__), "cinematic_vault", "database", "ebony_active_state.db")
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    
    pipeline = HVFDefensePipeline(db_path=db_file)
    logging.info(f"Pipeline armed. Station ID: {pipeline.station_id} | Watchdog: {pipeline.watchdog.status}")
    logging.info(f"Contactor Matrix: {list(pipeline.relay.channels.keys())}")
    logging.info(f"Ed25519 Forensic Signer: {pipeline.crypto_ledger.pubkey_bytes.hex()[:16]}... [ACTIVE]")

    host = "127.0.0.1"
    port = 8088
    logging.info(f"Binding air-gapped Telemetry Bridge & HMI Cockpit to http://{host}:{port}/")
    bridge = HVFTelemetryBridge(pipeline, host=host, port=port)
    bridge.start()

    cockpit_url = f"http://{host}:{port}/"
    logging.info(f"Sentinel Cockpit online at {cockpit_url}")
    print("\n" + "=" * 64)
    print(f"  >>> HMI COCKPIT ACTIVE AT: {cockpit_url}")
    print("  >>> Press Ctrl+C in this terminal to safely disarm and shutdown.")
    print("=" * 64 + "\n")

    # Automatically launch browser to the live cockpit
    try:
        webbrowser.open(cockpit_url)
    except Exception as e:
        logging.warning(f"Could not open browser automatically: {e}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n")
        logging.info("Shutdown signal received. Halting Telemetry Bridge cleanly...")
        bridge.stop()
        logging.info("Project Ebony safely disarmed. Session closed.")

if __name__ == "__main__":
    launch()
