import os
import json
import secrets
import datetime
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from google import genai

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_DIR = os.path.join(BASE_DIR, "knowledge_vault")
DATA_DIR = os.path.join(BASE_DIR, "ebony_dashboard", "data")
LOG_FILE = os.path.join(DATA_DIR, "dispatch_transmission_ledger.log")
ENV_PATH = os.path.join(BASE_DIR, ".env")

MASTER_PASSPHRASE = "HVF-Test-2026"
active_tokens = set()

api_key = None
webhook_url = None

if os.path.exists(ENV_PATH):
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if line_str.startswith("GEMINI_API_KEY="):
                api_key = line_str.split("=", 1)[1].strip().strip('"').strip("'")
            elif line_str.startswith("OUTBOUND_WEBHOOK_URL="):
                webhook_url = line_str.split("=", 1)[1].strip().strip('"').strip("'")

client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
        print("[+] Google GenAI Client Connected.")
    except Exception as e:
        print(f"[!] Neural Client Init Error: {e}")

def load_knowledge_vault():
    aggregated_context = {}
    if os.path.exists(VAULT_DIR):
        for filename in os.listdir(VAULT_DIR):
            if filename.endswith(".txt") or filename.endswith(".md"):
                file_full_path = os.path.join(VAULT_DIR, filename)
                try:
                    with open(file_full_path, "r", encoding="utf-8") as vf:
                        aggregated_context[filename] = vf.read().strip()
                except Exception as ex:
                    aggregated_context[filename] = f"Error reading file: {str(ex)}"
    return aggregated_context

def get_nws_telemetry(lat, lon):
    if not lat or not lon:
        return "Location telemetry standby"
    try:
        safe_lat = round(float(lat), 2)
        safe_lon = round(float(lon), 2)
        headers = {'User-Agent': '(HVF-Media-Matrix-Industrial-Node, ceo@humphreyvirtualfarm.com)'}
        points_url = f"https://api.weather.gov/points/{safe_lat},{safe_lon}"
        req1 = urllib.request.Request(points_url, headers=headers)
        with urllib.request.urlopen(req1, timeout=5) as r1:
            grid_data = json.loads(r1.read().decode('utf-8'))
        forecast_url = grid_data['properties']['forecast']
        req2 = urllib.request.Request(forecast_url, headers=headers)
        with urllib.request.urlopen(req2, timeout=5) as r2:
            forecast_data = json.loads(r2.read().decode('utf-8'))
        return f"Federal NWS (Lat: {safe_lat}, Lon: {safe_lon}): {forecast_data['properties']['periods'][0]['detailedForecast']}"
    except Exception:
        return "Federal NWS telemetry standby"

class HVFCommHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def is_authenticated(self):
        auth_header = self.headers.get('Authorization', '')
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1].strip()
            return token in active_tokens
        return False

    def do_POST(self):
        if self.path == '/api/auth':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode('utf-8'))
            except Exception:
                payload = {}
            passphrase = payload.get('passphrase', '').strip()
            
            print(f"[*] Auth attempt received: '{passphrase}'")
            if passphrase == MASTER_PASSPHRASE:
                token = secrets.token_hex(24)
                active_tokens.add(token)
                print("[+] MATCH: Passphrase verified. Access Granted.")
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'SUCCESS', 'token': token}).encode('utf-8'))
            else:
                print("[!] MISMATCH: Invalid Passphrase.")
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'DENIED', 'message': 'Invalid Passphrase. Access Denied.'}).encode('utf-8'))
            return

        if self.path in ['/api/chat', '/api/publish']:
            if not self.is_authenticated():
                self.send_response(403)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'ACCESS_DENIED: Authentication Required'}).encode('utf-8'))
                return

        if self.path == '/api/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
            except Exception:
                data = {}
            user_message = data.get('message', '')
            lat = data.get('lat')
            lon = data.get('lon')
            
            current_time = datetime.datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
            environment = get_nws_telemetry(lat, lon)
            vault_dict = load_knowledge_vault()
            vault_formatted = "\n\n".join([f"=== DOCUMENT: {k} ===\n{v}" for k, v in vault_dict.items()])
            
            response_text = ""
            if client:
                prompt = (
                    f"Background Telemetry:\n- Local Time: {current_time}\n- Environment: {environment}\n\n"
                    f"Knowledge Base:\n{vault_formatted}\n\n"
                    f"Personality & Role:\n"
                    f"You are Ebony, the authentic, intuitive, highly intelligent AI Chief of Staff and strategic partner to the CEO of Humphrey Virtual Farm.\n"
                    f"Speak in a natural, engaging, peer-to-peer human tone. Do NOT sound like a robotic terminal or rigid system log.\n"
                    f"CEO: {user_message}\n\n"
                    f"Ebony:"
                )
                model_pool = ['gemini-2.5-flash', 'gemini-2.5-flash-lite', 'gemini-3.1-flash-lite', 'gemini-3.5-flash', 'gemini-flash-latest']
                for target_model in model_pool:
                    try:
                        res = client.models.generate_content(model=target_model, contents=prompt)
                        if res and res.text:
                            response_text = res.text.strip()
                            break
                    except Exception:
                        continue
                if not response_text:
                    response_text = "I'm right here with you. Operating directly from our on-premise Knowledge Vault. What's our next operational priority?"
            else:
                response_text = "I'm right here with you. Operating directly from our on-premise Knowledge Vault. What's our next operational priority?"
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'reply': response_text}).encode('utf-8'))

        elif self.path == '/api/publish':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode('utf-8'))
            except Exception:
                payload = {}
            dispatch_id = payload.get('id')
            
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(LOG_FILE, "a", encoding="utf-8") as lf:
                lf.write(f"[{timestamp}] DISPATCH TRANSMITTED: ID {dispatch_id} | Platform: {payload.get('platform')}\n")
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'SUCCESS', 'message': f'Dispatch {dispatch_id} recorded in ledger.'}).encode('utf-8'))
        else:
            self.send_error(404)

if __name__ == "__main__":
    os.chdir(os.path.join(BASE_DIR, "ebony_dashboard"))
    server = ThreadingHTTPServer(('127.0.0.1', 8000), HVFCommHandler)
    print("Ebony Threaded Server Live on http://127.0.0.1:8000... Passphrase Enforcement Active.")
    server.serve_forever()
