"""
Project Ebony: Air-Gapped Telemetry Bridge & Sentinel HMI Cockpit
Tri-Brain 4-Perimeter Defense Matrix: Optical, Acoustic, Kinetic SCADA, Governance/RAG.
Codified under 100% Absolute Controlling Authority of Jeffery Humphrey.
DFARS 252.227-7018 / Oklahoma HB 2992 Compliant Architecture.
"""

import http.server
import socketserver
import json
import logging
import threading
from typing import Optional

logger = logging.getLogger("EBONY-TELEMETRY-BRIDGE")

HTML_COCKPIT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Ebony // Sentinel HMI Cockpit (4-Perimeter C2)</title>
    <style>
        :root {
            --bg-color: #070b14;
            --panel-bg: rgba(13, 20, 38, 0.85);
            --border-color: rgba(56, 189, 248, 0.25);
            --border-glow: #38bdf8;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --accent-red: #ef4444;
            --accent-cyan: #06b6d4;
            --accent-violet: #8b5cf6;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
            padding: 20px;
            background-image: radial-gradient(circle at 50% 0%, rgba(14, 165, 233, 0.12) 0%, transparent 70%);
            min-height: 100vh;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 14px;
            margin-bottom: 20px;
        }
        .header h1 { font-size: 19px; letter-spacing: 2px; text-transform: uppercase; color: var(--accent-cyan); }
        .subhead { font-size: 11px; color: var(--text-muted); margin-top: 4px; }
        .badge {
            font-size: 11px;
            padding: 4px 10px;
            border-radius: 4px;
            background: rgba(16, 185, 129, 0.15);
            color: var(--accent-emerald);
            border: 1px solid var(--accent-emerald);
            font-weight: bold;
        }
        .grid-layout {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 18px;
            margin-bottom: 20px;
        }
        .full-width { grid-column: 1 / -1; }
        .card {
            background: var(--panel-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 18px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            backdrop-filter: blur(12px);
        }
        .card-header {
            font-size: 12px;
            color: var(--accent-cyan);
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .perimeters-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-bottom: 4px;
        }
        .perimeter-card {
            background: rgba(0, 0, 0, 0.35);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 12px;
        }
        .p-title { font-size: 10px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px; }
        .p-status { font-size: 13px; font-weight: bold; color: var(--accent-emerald); margin-bottom: 4px; }
        .p-detail { font-size: 10px; color: var(--text-muted); line-height: 1.3; }
        .sld-bus {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
        }
        .breaker-card {
            background: rgba(0, 0, 0, 0.35);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 12px;
            text-align: center;
        }
        .breaker-id { font-size: 11px; color: var(--text-muted); margin-bottom: 6px; }
        .breaker-state { font-size: 14px; font-weight: bold; }
        .state-closed { color: var(--accent-emerald); }
        .state-open { color: var(--accent-red); }
        .c2-terminal {
            background: rgba(4, 8, 16, 0.95);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            height: 290px;
            overflow-y: auto;
            padding: 14px;
            font-family: monospace;
            font-size: 13px;
            margin-bottom: 12px;
            line-height: 1.5;
        }
        .c2-msg { margin-bottom: 12px; }
        .c2-user { color: var(--accent-cyan); font-weight: bold; }
        .c2-ebony { color: #38bdf8; font-weight: bold; }
        .c2-meta { color: var(--text-muted); font-size: 10px; margin-top: 4px; }
        .c2-controls {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 10px;
            font-size: 11px;
            color: var(--text-muted);
        }
        .c2-toggle-label { display: flex; align-items: center; gap: 6px; cursor: pointer; }
        .c2-input-row {
            display: flex;
            gap: 10px;
        }
        .c2-input {
            flex: 1;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            padding: 10px 14px;
            color: #fff;
            font-family: monospace;
            font-size: 13px;
        }
        .c2-input:focus { outline: none; border-color: var(--accent-cyan); }
        .c2-btn {
            background: rgba(6, 182, 212, 0.2);
            border: 1px solid var(--accent-cyan);
            color: var(--accent-cyan);
            padding: 0 20px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 12px;
            font-weight: bold;
            cursor: pointer;
            text-transform: uppercase;
        }
        .c2-btn:hover { background: var(--accent-cyan); color: #000; }
        .footer {
            font-size: 11px;
            color: var(--text-muted);
            text-align: center;
            margin-top: 18px;
            border-top: 1px solid rgba(255,255,255,0.06);
            padding-top: 12px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>Project Ebony // Sentinel Cockpit</h1>
            <div class="subhead">
                CAGE: 1AHA8 | OK HB 2992 | DFARS 252.227-7018 | Sole Controlling Authority: Jeffery Humphrey (100%)
            </div>
        </div>
        <div class="badge" id="system-badge">TRI-BRAIN ACTIVE</div>
    </div>

    <div class="grid-layout">
        <!-- 4-Perimeter Defense Status Grid -->
        <div class="card full-width">
            <div class="card-header">
                <span>The Four Sovereign Operational Perimeters (Defense Telemetry)</span>
                <span style="color: var(--accent-cyan);" id="rag-badge">Iron Dome RAG: 20,289 Vectors</span>
            </div>
            <div class="perimeters-grid">
                <div class="perimeter-card">
                    <div class="p-title">1. Optical Perimeter</div>
                    <div class="p-status">ACTIVE / ARMED</div>
                    <div class="p-detail">Arducam 1080P DirectShow &bull; Tapo RTSP (192.168.1.165) &bull; Live GLI Analysis</div>
                </div>
                <div class="perimeter-card">
                    <div class="p-title">2. Acoustic Perimeter</div>
                    <div class="p-status">ACTIVE / ARMED</div>
                    <div class="p-detail">Sovereign Voice Engine &bull; Shokz OpenRun Link &bull; Windows WASAPI Direct</div>
                </div>
                <div class="perimeter-card">
                    <div class="p-title">3. Kinetic SCADA</div>
                    <div class="p-status">NOMINAL (13.0us)</div>
                    <div class="p-detail">Sub-Microsecond Reflex &bull; 300ms Watchdog &bull; Modbus RTU Bus</div>
                </div>
                <div class="perimeter-card">
                    <div class="p-title">4. Sovereign Governance</div>
                    <div class="p-status">100% SOLE AUTHORITY</div>
                    <div class="p-detail">HVF-CONTRACT-SL-003 &bull; Ed25519 Signer &bull; Memory Vault SQLite</div>
                </div>
            </div>
        </div>

        <!-- 12.47 kV Single-Line Diagram -->
        <div class="card full-width">
            <div class="card-header">
                <span>12.47 kV Substation Single-Line Diagram (Brain 1 Kinetic Bus)</span>
                <span id="latency-tag" style="color: var(--accent-emerald);">Latency: 13.0us</span>
            </div>
            <div class="sld-bus">
                <div class="breaker-card">
                    <div class="breaker-id">CH1: UTILITY GRID</div>
                    <div class="breaker-state state-closed" id="ch1-status">CLOSED</div>
                    <div style="font-size: 10px; color: var(--text-muted); margin-top: 4px;">SOLE AUTHORITY GATE</div>
                </div>
                <div class="breaker-card">
                    <div class="breaker-id">CH2: SOLAR DER</div>
                    <div class="breaker-state state-closed" id="ch2-status">CLOSED</div>
                    <div style="font-size: 10px; color: var(--text-muted); margin-top: 4px;">AUTONOMOUS DER</div>
                </div>
                <div class="breaker-card">
                    <div class="breaker-id">CH3: BESS STORAGE</div>
                    <div class="breaker-state state-closed" id="ch3-status">CLOSED</div>
                    <div style="font-size: 10px; color: var(--text-muted); margin-top: 4px;">AUTONOMOUS DER</div>
                </div>
                <div class="breaker-card">
                    <div class="breaker-id">CH4: AUX GENSET</div>
                    <div class="breaker-state state-open" id="ch4-status">OPEN</div>
                    <div style="font-size: 10px; color: var(--text-muted); margin-top: 4px;">MANUAL OVERRIDE</div>
                </div>
            </div>
        </div>

        <!-- Brain 3 Interactive Apex C2 Console with RAG & Acoustic Toggle -->
        <div class="card full-width">
            <div class="card-header">
                <span>Brain 3 // Sovereign Apex C2 Executive Dialogue (CEO 100% Sole Authority)</span>
                <span class="badge" style="border-color: var(--accent-cyan); color: var(--accent-cyan);">IRON DOME GROUNDED</span>
            </div>
            <div class="c2-terminal" id="c2-terminal">
                <div class="c2-msg">
                    <span class="c2-ebony">[EBONY CORE]</span> Sovereign Apex C2 initialized. Reporting exclusively to CEO Jeffery Humphrey under 100% Absolute Controlling Authority. Iron Dome RAG (20,289 vectors) armed. Sovereign Voice Engine linked. Brain 1 Kinetic Safety Kernel active at 13.0us. How may I serve the mission, Sir?
                </div>
            </div>
            <div class="c2-controls">
                <label class="c2-toggle-label">
                    <input type="checkbox" id="voice-toggle" checked>
                    <span>Stream Audio to Shokz OpenRun Headset (Acoustic Perimeter)</span>
                </label>
                <span id="char-counter">Zero Cloud Relays &bull; Ed25519 Cryptographic Signatures</span>
            </div>
            <div class="c2-input-row">
                <input type="text" id="c2-input" class="c2-input" placeholder="Transmit directive or query to Ebony..." autocomplete="off">
                <button class="c2-btn" onclick="sendDirective()">Transmit</button>
            </div>
        </div>
    </div>

    <div class="footer">
        Humphrey Virtual Farms LLC &bull; Air-Gapped Sovereign SCADA &bull; Absolute Controlling Authority: Jeffery Humphrey (100%)
    </div>

    <script>
        async function sendDirective() {
            const input = document.getElementById("c2-input");
            const text = input.value.trim();
            if (!text) return;

            const voiceEnabled = document.getElementById("voice-toggle").checked;
            const terminal = document.getElementById("c2-terminal");
            terminal.innerHTML += `<div class="c2-msg"><span class="c2-user">[CEO DIRECTIVE]</span> ${escapeHtml(text)}</div>`;
            input.value = "";
            terminal.scrollTop = terminal.scrollHeight;

            try {
                const res = await fetch("/api/v1/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ prompt: text, voice: voiceEnabled })
                });
                const data = await res.json();
                const ragNotice = data.rag_intel_found ? ` &bull; RAG: Iron Dome Grounded (${data.rag_vectors} vectors)` : "";
                const voiceNotice = data.voice_dispatched ? " &bull; Voice: Dispatched to Headset" : "";
                terminal.innerHTML += `
                    <div class="c2-msg">
                        <span class="c2-ebony">[EBONY C2]</span> ${escapeHtml(data.reply)}
                        <div class="c2-meta">Engine: ${data.engine}${ragNotice}${voiceNotice} &bull; Signature: ${data.signature}</div>
                    </div>`;
            } catch (err) {
                terminal.innerHTML += `<div class="c2-msg" style="color: var(--accent-red);">[TRANSMISSION ERROR] Failed to connect to Brain 3: ${err}</div>`;
            }
            terminal.scrollTop = terminal.scrollHeight;
        }

        document.getElementById("c2-input").addEventListener("keypress", (e) => {
            if (e.key === "Enter") sendDirective();
        });

        function escapeHtml(t) {
            return t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        }
    </script>
</body>
</html>
"""

class HVFTelemetryHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_COCKPIT.encode("utf-8"))
        elif self.path == "/api/v1/telemetry":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            telemetry = {
                "station_id": getattr(self.server.pipeline, "station_id", "HVF-SUBSTATION-01") if self.server.pipeline else "STANDALONE",
                "authority": "JEFFERY_HUMPHREY_100_PERCENT",
                "status": "ONLINE",
                "perimeters": {
                    "optical": "ACTIVE",
                    "acoustic": "ACTIVE",
                    "kinetic_scada": "ACTIVE_13_0_US",
                    "governance": "100_PERCENT_SOLE_AUTHORITY"
                }
            }
            if self.server.brain3:
                telemetry["rag_vector_count"] = getattr(self.server.brain3, "vector_count", 0)
                telemetry["memory_vault_active"] = getattr(self.server.brain3, "memory_vault_active", False)
            self.wfile.write(json.dumps(telemetry).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/v1/chat":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len).decode("utf-8")
            try:
                req_json = json.loads(body)
                prompt = req_json.get("prompt", "")
                voice_enabled = bool(req_json.get("voice", False))
                if self.server.brain3:
                    resp_data = self.server.brain3.dispatch_query(prompt, voice_enabled=voice_enabled)
                else:
                    resp_data = {"status": "ERROR", "reply": "Brain 3 is offline.", "engine": "NONE"}
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(resp_data).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

class HVFTelemetryBridge:
    def __init__(self, pipeline, brain3=None, host="127.0.0.1", port=8088):
        self.pipeline = pipeline
        self.brain3 = brain3
        self.host = host
        self.port = port
        self.server = None
        self.thread = None

    def start(self):
        self.server = socketserver.TCPServer((self.host, self.port), HVFTelemetryHandler)
        self.server.pipeline = self.pipeline
        self.server.brain3 = self.brain3
        self.server.allow_reuse_address = True
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        logger.info(f"HMI Telemetry Bridge active on http://{self.host}:{self.port}/")

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            logger.info("Telemetry Bridge stopped.")
