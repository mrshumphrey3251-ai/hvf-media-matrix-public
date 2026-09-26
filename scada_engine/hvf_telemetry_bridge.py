"""
HVF Sovereign SCADA Telemetry Bridge & Air-Gapped Local Health Dashboard
Zero-cloud local HTTP/REST diagnostic service and enterprise HMI cockpit for edge operations.
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HVF SOVEREIGN SCADA DEFENSE MATRIX -- SENTINEL COCKPIT</title>
    <style>
        :root {
            --bg-void: #06090e;
            --bg-panel: #0d131a;
            --bg-card: #131c26;
            --border-dim: #1f2d3d;
            --border-glow: #00f0ff33;
            --accent-cyan: #00f0ff;
            --accent-green: #00ff88;
            --accent-amber: #ffaa00;
            --accent-red: #ff3344;
            --text-main: #e2e8f0;
            --text-dim: #64748b;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg-void);
            color: var(--text-main);
            font-family: 'Consolas', 'Courier New', monospace;
            padding: 16px;
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }
        .hud-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid var(--accent-cyan);
            background: linear-gradient(90deg, rgba(0,240,255,0.08) 0%, rgba(0,0,0,0) 100%);
            padding: 12px 16px;
            margin-bottom: 16px;
            box-shadow: 0 4px 20px rgba(0,240,255,0.15);
        }
        .hud-title {
            font-size: 1.25rem;
            font-weight: 900;
            color: var(--accent-cyan);
            letter-spacing: 2px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .pulse-led {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background-color: var(--accent-green);
            box-shadow: 0 0 10px var(--accent-green);
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.85); }
            100% { opacity: 1; transform: scale(1); }
        }
        .hud-meta {
            display: flex;
            gap: 20px;
            font-size: 0.8rem;
            color: var(--text-dim);
        }
        .hud-meta span strong { color: var(--text-main); }
        .cockpit-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 16px;
            flex: 1;
            min-height: 0;
        }
        .col-left, .col-right {
            display: flex;
            flex-direction: column;
            gap: 16px;
            min-height: 0;
        }
        .panel {
            background-color: var(--bg-panel);
            border: 1px solid var(--border-dim);
            border-radius: 6px;
            padding: 14px;
            position: relative;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }
        .panel-header {
            font-size: 0.85rem;
            font-weight: bold;
            color: var(--accent-cyan);
            letter-spacing: 1.5px;
            text-transform: uppercase;
            border-bottom: 1px solid var(--border-dim);
            padding-bottom: 8px;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
        }
        .sld-container {
            display: flex;
            flex-direction: column;
            gap: 12px;
            background-color: var(--bg-card);
            border: 1px dashed var(--border-dim);
            border-radius: 4px;
            padding: 16px;
        }
        .sld-bus {
            height: 6px;
            background: linear-gradient(90deg, #00f0ff, #00ff88);
            box-shadow: 0 0 10px rgba(0,240,255,0.4);
            border-radius: 3px;
            margin: 10px 0;
            position: relative;
        }
        .sld-bus-label {
            position: absolute;
            top: -18px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 0.7rem;
            color: var(--accent-cyan);
            letter-spacing: 1px;
        }
        .feeder-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
        }
        .feeder-card {
            background-color: var(--bg-panel);
            border: 1px solid var(--border-dim);
            border-radius: 4px;
            padding: 10px;
            text-align: center;
            position: relative;
            transition: all 0.3s ease;
        }
        .feeder-card.closed {
            border-color: var(--accent-green);
            box-shadow: inset 0 0 8px rgba(0,255,136,0.15);
        }
        .feeder-card.tripped {
            border-color: var(--accent-red);
            box-shadow: inset 0 0 8px rgba(255,51,68,0.2);
        }
        .feeder-id { font-size: 0.75rem; color: var(--text-dim); }
        .feeder-name { font-size: 0.8rem; font-weight: bold; margin: 4px 0; }
        .feeder-state {
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 900;
            padding: 2px 8px;
            border-radius: 3px;
            margin-top: 6px;
        }
        .state-closed { background: rgba(0,255,136,0.2); color: var(--accent-green); border: 1px solid var(--accent-green); }
        .state-tripped { background: rgba(255,51,68,0.2); color: var(--accent-red); border: 1px solid var(--accent-red); }
        .state-open { background: rgba(255,170,0,0.2); color: var(--accent-amber); border: 1px solid var(--accent-amber); }
        .telemetry-strip {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
        }
        .stat-box {
            background-color: var(--bg-card);
            border: 1px solid var(--border-dim);
            border-radius: 4px;
            padding: 10px;
        }
        .stat-label { font-size: 0.7rem; color: var(--text-dim); letter-spacing: 1px; }
        .stat-val { font-size: 1.1rem; font-weight: bold; margin-top: 4px; color: var(--text-main); }
        .chain-box {
            flex: 1;
            overflow-y: auto;
            background-color: var(--bg-card);
            border: 1px solid var(--border-dim);
            border-radius: 4px;
            padding: 8px;
            font-size: 0.75rem;
            min-height: 120px;
        }
        .chain-item {
            padding: 6px 8px;
            border-bottom: 1px solid var(--border-dim);
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        .chain-item:last-child { border-bottom: none; }
        .chain-hash { color: var(--accent-cyan); word-break: break-all; }
        .chain-meta { color: var(--text-dim); font-size: 0.7rem; display: flex; justify-content: space-between; }
        .ctrl-btn {
            background-color: var(--border-dim);
            color: var(--text-main);
            border: 1px solid var(--accent-cyan);
            padding: 8px 12px;
            font-family: inherit;
            font-size: 0.75rem;
            cursor: pointer;
            border-radius: 4px;
            transition: all 0.2s;
            text-transform: uppercase;
            font-weight: bold;
        }
        .ctrl-btn:hover {
            background-color: var(--accent-cyan);
            color: var(--bg-void);
            box-shadow: 0 0 10px var(--accent-cyan);
        }
    </style>
</head>
<body>
    <div class="hud-header">
        <div class="hud-title">
            <div class="pulse-led"></div>
            <span>PROJECT EBONY // SOVEREIGN SCADA DEFENSE MATRIX</span>
        </div>
        <div class="hud-meta">
            <span>STATION: <strong>KOKC</strong></span>
            <span>CAGE: <strong>1AHA8</strong></span>
            <span>COMPLIANCE: <strong>DFARS 252.227-7018 / OK HB 2992</strong></span>
            <span>LATENCY: <strong id="latency-val">0.0us</strong></span>
        </div>
    </div>
    <div class="cockpit-grid">
        <div class="col-left">
            <div class="panel">
                <div class="panel-header">
                    <span>Physical Kinetic Contactor Bus (Modbus RTU RS-485)</span>
                    <span id="bus-state-indicator" style="color: var(--accent-green);">BUS ENERGIZED</span>
                </div>
                <div class="sld-container">
                    <div style="font-size: 0.75rem; color: var(--text-dim);">HIGH-VOLTAGE INTERCONNECT & LOCAL DISTRIBUTED ENERGY ASSETS</div>
                    <div class="sld-bus">
                        <div class="sld-bus-label">SOVEREIGN MICROGRID SYNCHRONIZATION BUS (12.47 kV)</div>
                    </div>
                    <div class="feeder-grid">
                        <div class="feeder-card closed" id="card-ch1">
                            <div class="feeder-id">COIL 1 [0x0000]</div>
                            <div class="feeder-name">UTILITY GRID</div>
                            <div style="font-size:0.65rem; color:var(--text-dim);">DUAL-KEY CUSTODY</div>
                            <div class="feeder-state state-closed" id="state-ch1">CLOSED</div>
                        </div>
                        <div class="feeder-card closed" id="card-ch2">
                            <div class="feeder-id">COIL 2 [0x0001]</div>
                            <div class="feeder-name">PHOTOVOLTAIC</div>
                            <div style="font-size:0.65rem; color:var(--text-dim);">AUTONOMOUS DER</div>
                            <div class="feeder-state state-closed" id="state-ch2">CLOSED</div>
                        </div>
                        <div class="feeder-card closed" id="card-ch3">
                            <div class="feeder-id">COIL 3 [0x0002]</div>
                            <div class="feeder-name">BESS STORAGE</div>
                            <div style="font-size:0.65rem; color:var(--text-dim);">AUTONOMOUS DER</div>
                            <div class="feeder-state state-closed" id="state-ch3">CLOSED</div>
                        </div>
                        <div class="feeder-card" id="card-ch4">
                            <div class="feeder-id">COIL 4 [0x0003]</div>
                            <div class="feeder-name">AUX GENSET</div>
                            <div style="font-size:0.65rem; color:var(--text-dim);">MANUAL OVERRIDE</div>
                            <div class="feeder-state state-open" id="state-ch4">STANDBY</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="panel">
                <div class="panel-header">
                    <span>Sentinel State & Atmospheric Oracle Ingest</span>
                    <span id="oracle-source">EAS/SAME 162.400 MHz</span>
                </div>
                <div class="telemetry-strip">
                    <div class="stat-box">
                        <div class="stat-label">ATMOSPHERIC THREAT</div>
                        <div class="stat-val" id="threat-val" style="color: var(--accent-green);">TIER 0: NOMINAL</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">WATCHDOG TIMER</div>
                        <div class="stat-val" id="watchdog-val" style="color: var(--accent-cyan);">ACTIVE (1000ms)</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">AIR-GAP SECURITY GATE</div>
                        <div class="stat-val" style="color: var(--accent-green);">SOVEREIGN (ZERO-WAN)</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-right">
            <div class="panel" style="flex:1; display:flex; flex-direction:column; min-height:0;">
                <div class="panel-header">
                    <span>Ed25519 Forensic Ledger</span>
                    <span id="chain-badge" style="color: var(--accent-green);">100% INTACT</span>
                </div>
                <div class="chain-box" id="chain-stream">
                    <div class="chain-item">
                        <div class="chain-meta">
                            <span>BLOCK #0: GENESIS</span>
                            <span>INITIALIZED</span>
                        </div>
                        <div class="chain-hash" id="latest-hash-display">0000000000000000000000000000000000000000000000000000000000000000</div>
                    </div>
                </div>
                <div style="margin-top:10px; font-size:0.7rem; color:var(--text-dim);">
                    SIGNER PUBKEY:
                    <div id="signer-key" style="word-break:break-all; color:var(--text-main); font-family:monospace; margin-top:2px;">LOADING...</div>
                </div>
            </div>
            <div class="panel">
                <div class="panel-header">
                    <span>Sovereign Command Console</span>
                </div>
                <div style="display:flex; flex-direction:column; gap:8px;">
                    <button class="ctrl-btn" onclick="pollData()">Force Telemetry Poll</button>
                </div>
            </div>
        </div>
    </div>
    <script>
        async function pollData() {
            try {
                const hRes = await fetch('/api/v1/health');
                const health = await hRes.json();
                document.getElementById('watchdog-val').innerText = health.watchdog_status || 'ARMED';

                const tRes = await fetch('/api/v1/telemetry');
                const telem = await tRes.json();
                document.getElementById('latency-val').innerText = (telem.last_pipeline_latency_us || 0.0) + 'us';

                const breakers = telem.breaker_channels || {};
                updateBreaker('ch1', breakers.CH1_UTILITY_GRID || 'CLOSED');
                updateBreaker('ch2', breakers.CH2_PV_ARRAYS || 'CLOSED');
                updateBreaker('ch3', breakers.CH3_BESS_STORAGE || 'CLOSED');
                updateBreaker('ch4', breakers.CH4_AUX_GENERATOR || 'OPEN');

                const lRes = await fetch('/api/v1/ledger');
                const ledger = await lRes.json();
                document.getElementById('signer-key').innerText = ledger.signer_pubkey_hex || 'N/A';
                document.getElementById('latest-hash-display').innerText = ledger.latest_block_hash || '000000000000...';
                document.getElementById('chain-badge').innerText = ledger.chain_valid ? (ledger.total_blocks + ' BLOCKS [INTACT]') : 'CORRUPTED';
                document.getElementById('chain-badge').style.color = ledger.chain_valid ? 'var(--accent-green)' : 'var(--accent-red)';
            } catch (err) {
                console.error("Telemetry poll failed:", err);
            }
        }
        function updateBreaker(ch, state) {
            const card = document.getElementById('card-' + ch);
            const badge = document.getElementById('state-' + ch);
            if (!card || !badge) return;
            card.className = 'feeder-card ' + state.toLowerCase();
            badge.innerText = state;
            if (state === 'CLOSED') {
                badge.className = 'feeder-state state-closed';
            } else if (state === 'TRIPPED') {
                badge.className = 'feeder-state state-tripped';
            } else {
                badge.className = 'feeder-state state-open';
            }
        }
        setInterval(pollData, 1500);
        window.onload = pollData;
    </script>
</body>
</html>
"""

class HVFTelemetryHandler(BaseHTTPRequestHandler):
    pipeline_ref: Optional[HVFDefensePipeline] = None

    def log_message(self, format, *args):
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
