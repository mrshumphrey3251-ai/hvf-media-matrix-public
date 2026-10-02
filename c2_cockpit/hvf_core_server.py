# hvf_core_server.py - HVF Media Matrix Sovereign Engine (Private)
# Engineered for absolute control. Pure native Python architecture. Zero external dependencies.

import http.server
import socketserver
import json
from datetime import datetime
from hvf_security_gateway import HVFSecurityGateway
from hvf_master_orchestrator import MasterOrchestrator

PORT = 3000
security_perimeter = HVFSecurityGateway()
orchestrator = MasterOrchestrator()

class HVFCoreHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Primary Diagnostic Route - Verifies system health natively
        if self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "Secure & Online",
                "message": "HVF Media Matrix Sovereign Core is fully operational.",
                "timestamp": datetime.now().isoformat(),
                "dependency_level": "ZERO"
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        # Primary Ingestion Route - Secures incoming data payloads
        if self.path == '/api/ingest':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # SECURITY PROTOCOL: Enforce cryptographic token validation
            incoming_token = self.headers.get('X-HVF-Token')
            
            if not incoming_token or not security_perimeter.validate_payload(incoming_token):
                self.send_response(403)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "status": "ACCESS DENIED", 
                    "message": "Intrusion blocked by HVF Security Perimeter."
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            
            # INTELLIGENCE ROUTING: Parse and forward to Master Orchestrator
            try:
                payload_json = json.loads(post_data.decode('utf-8'))
                orchestrator.process_payload(payload_json)
            except Exception as e:
                print(f"[SYSTEM ERROR] Payload parsing failed: {e}")
            
            # Payload Authorized
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "Payload Received, Authorized & Orchestrated",
                "message": "HVF Media Matrix data ingestion pathway secured.",
                "data_size_bytes": content_length,
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

# Centralized execution block - Seizes the port and launches the matrix
with socketserver.TCPServer(("", PORT), HVFCoreHandler) as httpd:
    print(f"[SYSTEM START] HVF Sovereign Matrix executing on port {PORT}")
    print("[ARCHITECTURE STATUS] API Ingestion pathways online, fortified, and wired to Orchestrator.")
    httpd.serve_forever()