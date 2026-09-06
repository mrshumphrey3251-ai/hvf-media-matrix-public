import os, sys, json, sqlite3, hashlib, base64
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# --- ARCHITECTURE PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "hvf_memory_vault.db")
GHOST_LOG = os.path.join(BASE_DIR, "ebony_dashboard", "data", "ghost_server.log")

# Force silent running in the background ledger
os.makedirs(os.path.dirname(GHOST_LOG), exist_ok=True)
sys.stdout = open(GHOST_LOG, 'a', encoding='utf-8')
sys.stderr = open(GHOST_LOG, 'a', encoding='utf-8')

# --- CRYPTOGRAPHIC ENGINE ---
def derive_cipher(password: str, username: str) -> Fernet:
    salt = hashlib.sha256(username.encode("utf-8")).digest()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    return Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8"))))

# --- MASTER ROUTING ENGINE ---
class MasterRoutingEngine(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 1. ENCRYPTED TEXT & TELEMETRY INGESTION (SCADA)
            if self.path == '/api/transmit':
                content_length = int(self.headers.get('Content-Length', 0))
                data = json.loads(self.rfile.read(content_length).decode('utf-8'))
                
                username = data.get('username', '').strip().lower()
                password = data.get('password', '')
                role = data.get('role', 'SCADA_AGENT')
                content = data.get('content', '')

                if not username or not password or not content:
                    self.send_error(400, "Missing Cryptographic Parameters")
                    return

                # Encrypt the payload to match the CEO's UI vault perfectly
                cipher = derive_cipher(password, username)
                blob = cipher.encrypt(content.encode("utf-8")).decode("utf-8")

                # Inject securely into SQLite Memory Vault
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS encrypted_user_comms (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, role TEXT NOT NULL, encrypted_content TEXT NOT NULL, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
                cur.execute("INSERT INTO encrypted_user_comms (username, role, encrypted_content) VALUES (?, ?, ?)", (username, role, blob))
                conn.commit()
                conn.close()

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'SUCCESS', 'message': 'Payload Encrypted & Secured'}).encode('utf-8'))
                return

            # 2. FUTURE EXPANSION: VIDEO WEBRTC SIGNALING
            elif self.path == '/api/video_signal':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'STANDBY', 'message': 'WebRTC Video Pipeline Ready'}).encode('utf-8'))
                return

            # 3. FUTURE EXPANSION: VOICE CALL SIGNALING
            elif self.path == '/api/voice_signal':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'STANDBY', 'message': 'Voice WebSocket Pipeline Ready'}).encode('utf-8'))
                return

        except Exception as e:
            print(f"Routing Fault: {e}", flush=True)
            self.send_error(500, "Internal Cryptographic Fault")

if __name__ == '__main__':
    server = ThreadingHTTPServer(('0.0.0.0', 8085), MasterRoutingEngine)
    print("[*] SOVEREIGN MASTER ROUTING ENGINE ONLINE: 0.0.0.0:8085", flush=True)
    server.serve_forever()