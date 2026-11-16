"""
================================================================================
PROPRIETARY AND CONFIDENTIAL -- HUMPHREY VIRTUAL FARMS LLC
PROTECTED UNDER 10 U.S.C. § 4022 OTHER TRANSACTION AGREEMENT
================================================================================
CONTRACTOR NAME: Humphrey Virtual Farms LLC
CONTRACTOR ADDRESS: Oklahoma, USA
CAGE CODE: 1AHA8 | UEI: S1M4ENLHTDH5
AGREEMENT / OTA IDENTIFIER: PROTOTYPE OTA 10 U.S.C. § 4022

RESTRICTIVE LEGEND -- COMMERCIAL COMPUTER SOFTWARE & PROPRIETARY TECHNICAL DATA:
The software, firmware, algorithms, architectural structures, and underlying
source code contained herein are proprietary commercial items developed entirely
at private expense by Humphrey Virtual Farms LLC.

The Government's rights to use, modify, reproduce, release, perform, display,
or disclose this computer software and technical data are restricted as set forth
in the governing 10 U.S.C. § 4022 Prototype Agreement. Any reproduction of this
software, in whole or in part, or disclosure to unauthorized third parties or
commercial competitors without the express written permission of Humphrey
Virtual Farms LLC is strictly prohibited.
================================================================================
"""
# hvf_core_server.py - HVF Media Matrix Sovereign Engine
# Engineered for absolute control. Pure native Python architecture + WORM Merkle Ledger.

from datetime import datetime
import http.server
import json
import socketserver

from hvf_master_orchestrator import MasterOrchestrator
from hvf_security_gateway import HVFSecurityGateway
from merkle_ingest_bridge import SovereignMerkleLedger

PORT = 3000
security_perimeter = HVFSecurityGateway()
orchestrator = MasterOrchestrator()
merkle_ledger = SovereignMerkleLedger()


class ThreadedHVFServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


class HVFCoreHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Primary Diagnostic Route - Verifies system health natively
        if self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            audit = merkle_ledger.audit_chain()
            response = {
                "status": "Secure & Online",
                "message": "HVF Media Matrix Sovereign Core is fully operational.",
                "timestamp": datetime.now().isoformat(),
                "dependency_level": "ZERO",
                "merkle_chain_valid": audit["valid"],
                "merkle_chain_height": audit["chain_height"],
                "merkle_head": audit["merkle_head"],
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        elif self.path == '/api/merkle':
            audit = merkle_ledger.audit_chain()
            self.send_response(200 if audit["valid"] else 500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(audit).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        # Primary Ingestion Route - Secures incoming data payloads & seals SHA-256 Merkle block
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

            # INTELLIGENCE ROUTING: Parse, forward to Master Orchestrator & seal WORM Merkle block
            try:
                payload_json = json.loads(post_data.decode('utf-8'))
                orchestrator.process_payload(payload_json)
            except Exception as e:
                payload_json = {"raw_bytes": content_length, "parse_note": str(e)}
                print(f"[SYSTEM ERROR] Payload parsing failed: {e}")

            source_node = self.headers.get('X-HVF-Node', 'API_PORT_3000')
            sealed_block = merkle_ledger.seal_payload(payload_json, source_node=source_node)

            # Payload Authorized & Cryptographically Sealed
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response = {
                "status": "Payload Received, Authorized & Orchestrated",
                "message": "HVF Media Matrix data ingestion pathway secured.",
                "data_size_bytes": content_length,
                "timestamp": datetime.now().isoformat(),
                "merkle_block_id": sealed_block["block_id"],
                "merkle_block_hash": sealed_block["block_hash"],
                "merkle_prev_hash": sealed_block["prev_hash"],
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()


def main():
    # Centralized execution block - Seizes the port and launches the threaded matrix
    with ThreadedHVFServer(("", PORT), HVFCoreHandler) as httpd:
        print(f"[SYSTEM START] HVF Sovereign Matrix executing on port {PORT}")
        print("[ARCHITECTURE STATUS] API Ingestion pathways online, fortified, and wired to WORM Merkle Ledger.")
        httpd.serve_forever()


if __name__ == "__main__":
    main()