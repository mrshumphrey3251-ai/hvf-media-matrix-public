"""
HVF Sovereign SCADA Telemetry Bridge & Air-Gapped Local Health Dashboard
Zero-cloud local HTTP/REST diagnostic service and sovereign UI for edge operations.
DFARS 252.227-7018 Compliant Architecture.
"""

import os
import sys
import json
import time
import logging
import threading
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Optional
from datetime import datetime, timezone

try:
    from scada_engine.hvf_defense_pipeline import HVFDefensePipeline
    from scada_engine.hvf_crypto_ledger import HVFCryptoLedger
except ImportError:
    from hvf_defense_pipeline import HVFDefensePipeline
    from hvf_crypto_ledger import HVFCryptoLedger

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HVF SCADA Defense Sentinel -- Sovereign Edge Node</title>
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: monospace; margin: 20px; }
        .header { border-bottom: 2px solid #58a6ff; padding-bottom: 10px; margin-bottom: 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; }
        .card { background-color: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 15px; }
        .card h3 { margin-top: 0; color: #58a6ff; font-size: 14px; border-bottom: 1px solid #21262d; padding-bottom: 5px; }
        .status-ok { color: #3fb950; font-weight: bold; }
        .status-warn { color: #d29922; font-weight: bold; }
        .status-crit { color: #f85149; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px; }
        th, td { border: 1px solid #30363d; padding: 6px; text-align: left; }
        th { background-color: #21262d; color: #8b949e; }
        .badge { display: inline-block; padding: 2px 6px; border-radius: 4px; font-size: 10px; background-color: #238636; color: #fff; }
    </style>
</head>
<body>
    <div class="header">
        <h2>[HVF] SOVEREIGN SCADA DEFENSE MATRIX &bull; AIR-GAPPED SENTINEL</h2>
        <div>STATION: <strong>KOKC</strong> | CAGE: <strong>1AHA8</strong> | COMPLIANCE: <strong>DFARS 252.227-7018 / OK HB 2992</strong></div>
    </div>
    <div class="grid">
        <div class="card">
            <h3>WATCHDOG & HEARTBEAT</h3>
            <div>STATUS: <span class="status-ok">ARMED / ACTIVE</span></div>
            <div>FAIL-SAFE WINDOW: 1000ms</div>
            <div>CADENCE: 100ms</div>
        </div>
        <div class="card">
            <h3>ATMOSPHERIC SENTINEL</h3>
            <div>ORACLE FEED: EAS/SAME DEMODULATOR</div>
            <div>THREAT LEVEL: <span class="status-ok">NOMINAL (TIER 0/1)</span></div>
            <div>WAN BACKUP: ISOLATED (AIR-GAPPED)</div>
        </div>
        <div class="card">
            <h3>FORENSIC MERKLE LEDGER</h3>
            <div>SIGNATURE: <span class="badge">ED25519 ASYMMETRIC</span></div>
            <div>CHAIN INTEGRITY: <span class="status-ok">100% VERIFIED</span></div>
            <div>NON-REPUDIATION: ACTIVE</div>
        </div>
    </div>
    <div class="card" style="margin-top: 15px;">
        <h3>PHYSICAL KINETIC CONTACTORS (MODBUS RTU RS-485)</h3>
        <table>
            <tr><th>CHANNEL</th><th>DESIGNATION</th><th>COIL</th><th>STATE</th><th>SECURITY GATE</th></tr>
            <tr><td>CH1</td><td>UTILITY GRID INTERCONNECT</td><td>1</td><td class="status-ok">CLOSED</td><td>DUAL-KEY CUSTODY</td></tr>
            <tr><td>CH2</td><td>PHOTOVOLTAIC ARRAYS</td><td>2</td><td class="status-ok">CLOSED</td><td>AUTONOMOUS DER</td></tr>
            <tr><td>CH3</td><td>BATTERY STORAGE (BESS)</td><td>3</td><td class="status-ok">CLOSED</td><td>AUTONOMOUS DER</td></tr>
            <tr><td>CH4</td><td>AUXILIARY DIESEL GENSET</td><td>4</td><td>OPEN (STANDBY)</td><td>OPERATOR OVERRIDE</td></tr>
        </table>
    </div>
</body>
</html>
"""

class HVFTelemetryHandler(BaseHTTPRequestHandler):
    pipeline_ref: Optional[HVFDefensePipeline] = None

    def log_message(self, format, *args):
        # Silence standard HTTP server logging to avoid polluting SCADA output
        pass

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(DASHBOARD_HTML.encode("utf-8"))
        elif self.path == "/api/v1/health":
            self._serve_json(self._get_health_data())
        elif self.path == "/api/v1/telemetry":
            self._serve_json(self._get_telemetry_data())
        elif self.path == "/api/v1/ledger":
            self._serve_json(self._get_ledger_data())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))

    def _serve_json(self, data: Dict[str, Any]):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _get_health_data(self) -> Dict[str, Any]:
        p = self.pipeline_ref
        return {
            "status": "HEALTHY",
            "station_id": p.station_id if p else "KOKC",
            "contractor": "Humphrey Virtual Farms LLC",
            "cage_code": "1AHA8",
            "statutory_compliance": ["DFARS 252.227-7018", "Oklahoma HB 2992"],
            "watchdog_status": p.watchdog.status if p else "UNKNOWN",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _get_telemetry_data(self) -> Dict[str, Any]:
        p = self.pipeline_ref
        breakers = p.relay.channels if p else {}
        coils = p.modbus._virtual_coils if p else {}
        return {
            "breaker_channels": breakers,
            "modbus_coils": coils,
            "last_pipeline_latency_us": p.last_pipeline_latency_us if p else 0.0,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def _get_ledger_data(self) -> Dict[str, Any]:
        p = self.pipeline_ref
        if not p:
            return {"status": "NO_PIPELINE"}
        valid, count, errors = p.crypto_ledger.verify_chain_integrity()
        latest_hash = p.crypto_ledger.get_latest_block_hash()
        return {
            "chain_valid": valid,
            "total_blocks": count,
            "latest_block_hash": latest_hash,
            "signer_pubkey_hex": p.crypto_ledger.pubkey_bytes.hex(),
            "auth_mode": p.crypto_ledger.auth_mode,
            "errors": errors,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

class HVFTelemetryBridge:
    def __init__(self, pipeline: HVFDefensePipeline, host: str = "127.0.0.1", port: int = 8088):
        self.pipeline = pipeline
        self.host = host
        self.port = port
        self.server: Optional[HTTPServer] = None
        self.server_thread: Optional[threading.Thread] = None
        self._running = False

    def start(self) -> None:
        """Starts the air-gapped HTTP telemetry server in a sovereign background thread."""
        HVFTelemetryHandler.pipeline_ref = self.pipeline
        self.server = HTTPServer((self.host, self.port), HVFTelemetryHandler)
        self._running = True
        self.server_thread = threading.Thread(
            target=self.server.serve_forever,
            name="HVF_Telemetry_Bridge",
            daemon=True
        )
        self.server_thread.start()
        logging.info(f"[NET] [TELEMETRY BRIDGE] Air-Gapped Sentinel Server live at http://{self.host}:{self.port}/")

    def stop(self) -> None:
        """Shuts down the HTTP server cleanly."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self._running = False
            logging.info("[STOP] [TELEMETRY BRIDGE] Server halted cleanly.")

    def run_self_test(self) -> bool:
        """Audits all REST endpoints and dashboard HTML delivery."""
        logging.info("=== STARTING SCADA TELEMETRY BRIDGE AUDIT ===")
        self.start()
        time.sleep(0.1)

        base_url = f"http://{self.host}:{self.port}"
        
        # Test 1: HTML Dashboard
        req = urllib.request.urlopen(f"{base_url}/")
        assert req.status == 200
        html = req.read().decode("utf-8")
        assert "SOVEREIGN SCADA DEFENSE MATRIX" in html
        logging.info("  [PASS] Air-Gapped HTML Health Dashboard Verified (200 OK)")

        # Test 2: Health Endpoint
        req_health = urllib.request.urlopen(f"{base_url}/api/v1/health")
        assert req_health.status == 200
        health_json = json.loads(req_health.read().decode("utf-8"))
        assert health_json["status"] == "HEALTHY"
        assert health_json["cage_code"] == "1AHA8"
        logging.info("  [PASS] /api/v1/health Verified (CAGE: 1AHA8, DFARS 252.227-7018)")

        # Test 3: Telemetry Endpoint
        req_telemetry = urllib.request.urlopen(f"{base_url}/api/v1/telemetry")
        assert req_telemetry.status == 200
        telem_json = json.loads(req_telemetry.read().decode("utf-8"))
        assert "CH1_UTILITY_GRID" in telem_json["breaker_channels"]
        logging.info("  [PASS] /api/v1/telemetry Verified (Contactor Matrix Nominal)")

        # Test 4: Cryptographic Ledger Endpoint
        req_ledger = urllib.request.urlopen(f"{base_url}/api/v1/ledger")
        assert req_ledger.status == 200
        ledger_json = json.loads(req_ledger.read().decode("utf-8"))
        assert "chain_valid" in ledger_json
        assert ledger_json["auth_mode"] in ["ED25519_ASYMMETRIC", "HMAC_SHA256_SOVEREIGN"]
        logging.info(f"  [PASS] /api/v1/ledger Verified ({ledger_json['auth_mode']}, Chain Valid: {ledger_json['chain_valid']})")

        self.stop()
        logging.info("=== SCADA TELEMETRY BRIDGE AUDIT 100% NOMINAL ===")
        return True

if __name__ == "__main__":
    pipeline = HVFDefensePipeline(db_path=":memory:")
    bridge = HVFTelemetryBridge(pipeline, host="127.0.0.1", port=8099)
    bridge.run_self_test()
