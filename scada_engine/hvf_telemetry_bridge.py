"""
Project Ebony: Air-Gapped Telemetry Bridge & Sentinel HMI Cockpit
Tri-Brain Architecture: Brain 1 (Kinetic), Brain 2 (Tactical), Brain 3 (Apex C2).
Codified under 100% Absolute Controlling Authority of Jeffery Humphrey.
DFARS 252.227-7018 Compliant Architecture.
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
    <title>Project Ebony // Sentinel HMI Cockpit</title>
    <style>
        :root {
            --bg-color: #0a0f1d;
            --panel-bg: rgba(16, 24, 48, 0.75);
            --border-color: rgba(56, 189, 248, 0.2);
            --border-glow: #38bdf8;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --accent-red: #ef4444;
            --accent-cyan: #06b6d4;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
            padding: 24px;
            background-image: radial-gradient(circle at 50% 0%, rgba(14, 165, 233, 0.1) 0%, transparent 60%);
            min-height: 100vh;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 16px;
            margin-bottom: 24px;
        }
        .header h1 { font-size: 20px; letter-spacing: 2px; text-transform: uppercase; color: var(--accent-cyan); }
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
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }
        .full-width { grid-column: 1 / -1; }
        .card {
            background: var(--panel-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
            backdrop-filter: blur(10px);
        }
        .card-header {
            font-size: 13px;
            color: var(--accent-cyan);
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .sld-bus {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin-top: 10px;
        }
        .breaker-card {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 12px;
            text-align: center;
        }
        .breaker-id { font-size: 12px; color: var(--text-muted); margin-bottom: 6px; }
        .breaker-state { font-size: 15px; font-weight: bold; }
        .state-closed { color: var(--accent-emerald); }
        .state-open { color: var(--accent-red); }
        .c2-terminal {
            background: rgba(5, 10, 20, 0.9);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            height: 280px;
            overflow-y: auto;
            padding: 14px;
            font-family: monospace;
            font-size: 13px;
            margin-bottom: 12px;
            line-height: 1.5;
        }
        .c2-msg { margin-bottom: 10px; }
        .c2-user { color: var(--accent-cyan); }
        .c2-ebony { color: #38bdf8; }
        .c2-meta { color: var(--text-muted); font-size: 11px; margin-top: 2px; }
        .c2-input-row {
            display: flex;
            gap: 10px;
        }
        .c2-input {
            flex: 1;
            background: rgba(0, 0, 0, 0.4);
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
            margin-top: 20px;
            border-top: 1px solid rgba(255,255,255,0.05);
            padding-top: 14px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>Project Ebony // Sentinel Cockpit</h1>
            <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">
                CAGE: 1AHA8 | OK HB 2992 | DFARS 252.227-7018 | Sovereign Tri-Brain Matrix
            </div>
        </div>
        <div class="badge" id="system-badge">TRI-BRAIN ACTIVE</div>
    </div>

    <div class="grid-layout">
        <!-- Single-Line Diagram -->
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

        <!-- Brain 3 Interactive Apex C2 Console -->
        <div class="card full-width">
            <div class="card-header">
                <span>Brain 3 // Sovereign Apex C2 Executive Dialogue (CEO 100% Sole Authority)</span>
                <span class="badge" style="border-color: var(--accent-cyan); color: var(--accent-cyan);">GUARDRAILS ARMED</span>
            </div>
            <div class="c2-terminal" id="c2-terminal">
                <div class="c2-msg">
                    <span class="c2-ebony">[EBONY CORE]</span> Sovereign Apex C2 initialized. Reporting exclusively to CEO Jeffery Humphrey under 100% Absolute Controlling Authority. Brain 1 Kinetic Safety Kernel active (13.0us). How may I serve the mission, Sir?
                </div>
            </div>
            <div class="c2-input-row">
                <input type="text" id="c2-input" class="c2-input" placeholder="Transmit directive or status query to Ebony..." autocomplete="off">
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

            const terminal = document.getElementById("c2-terminal");
            terminal.innerHTML += `<div class="c2-msg"><span class="c2-user">[CEO DIRECTIVE]</span> ${escapeHtml(text)}</div>`;
            input.value = "";
            terminal.scrollTop = terminal.scrollHeight;

            try {
                const res = await fetch("/api/v1/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ prompt: text })
                });
                const data = await res.json();
                terminal.innerHTML += `
                    <div class="c2-msg">
                        <span class="c2-ebony">[EBONY C2]</span> ${escapeHtml(data.reply)}
                        <div class="c2-meta">Engine: ${data.engine} &bull; Signature: ${data.signature}</div>
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
            telemetry = {}
            if self.server.pipeline:
                telemetry = {
                    "station_id": getattr(self.server.pipeline, "station_id", "HVF-SUBSTATION-01"),
                    "authority": "JEFFERY_HUMPHREY_100_PERCENT",
                    "status": "ONLINE"
                }
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
                if self.server.brain3:
                    resp_data = self.server.brain3.dispatch_query(prompt)
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
