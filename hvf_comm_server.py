import os
import json
import datetime
import urllib.request
from http.server import SimpleHTTPRequestHandler, HTTPServer
from google import genai

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_DIR = os.path.join(BASE_DIR, "knowledge_vault")
DATA_DIR = os.path.join(BASE_DIR, "ebony_dashboard", "data")
LOG_FILE = os.path.join(DATA_DIR, "dispatch_transmission_ledger.log")
ENV_PATH = os.path.join(BASE_DIR, ".env")

GITHUB_PUBLIC_VAULT = "https://github.com/mrshumphrey3251-ai/hvf-media-matrix-public"
REPO_SIGNATURE = f"\n\n[HVF INFRASTRUCTURE BROADCAST]\nOfficial Architecture Repository: {GITHUB_PUBLIC_VAULT}\nOperational Security: Geofenced & Vault-Verified"

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
        print("[+] Google GenAI Client Initialized Successfully.")
    except Exception as e:
        print(f"[!] Neural Client Init Error: {e}")
else:
    print("[!] WARNING: GEMINI_API_KEY not found in .env.")

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
        current_weather = forecast_data['properties']['periods'][0]['detailedForecast']
        return f"Federal NWS (Lat: {safe_lat}, Lon: {safe_lon}): {current_weather}"
    except Exception:
        return "Federal NWS telemetry standby"

class HVFCommHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
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
                    f"System Context:\n"
                    f"- Current Local Time: {current_time}\n"
                    f"- Live Environmental Telemetry: {environment}\n\n"
                    f"PROPRIETARY KNOWLEDGE VAULT MEMORY:\n{vault_formatted}\n\n"
                    f"Role: You are Ebony, the authentic, highly intelligent, executive AI Chief of Staff to the CEO of Humphrey Virtual Farm. "
                    f"Converse naturally, fluidly, and directly to the CEO. Address all inquiries with clarity and depth. Use your Knowledge Vault for historical and technical recall.\n\n"
                    f"CEO Directive: {user_message}\n\n"
                    f"Ebony Response:"
                )
                
                # Model chain using official verified names
                target_models = ['gemini-3.7-flash', 'gemini-3.5-flash', 'gemini-flash-latest']
                success = False
                last_error_msg = ""
                
                for mod in target_models:
                    try:
                        print(f"[*] Attempting neural generation with model: {mod}...")
                        res = client.models.generate_content(
                            model=mod,
                            contents=prompt
                        )
                        if res and res.text:
                            response_text = res.text.strip() + REPO_SIGNATURE
                            print(f"[+] Generation successful via [{mod}].")
                            success = True
                            break
                    except Exception as err:
                        last_error_msg = str(err)
                        print(f"[!] Generation error on [{mod}]: {last_error_msg}")
                
                if not success:
                    response_text = f"[NEURAL LINK ERROR] Detailed Diagnostic: {last_error_msg}{REPO_SIGNATURE}"
            else:
                response_text = f"[NEURAL LINK STANDBY] Key missing in .env.{REPO_SIGNATURE}"
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'reply': response_text}).encode('utf-8'))

        elif self.path == '/api/publish':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            payload = json.loads(post_data.decode('utf-8'))
            dispatch_id = payload.get('id')
            
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] DISPATCH TRANSMITTED: ID {dispatch_id} | Platform: {payload.get('platform')} | Topic: {payload.get('topic')}\n"
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(LOG_FILE, "a", encoding="utf-8") as lf:
                lf.write(log_entry)
                
            webhook_status = "Local Ledger Only"
            if webhook_url:
                try:
                    req_payload = json.dumps({
                        "event": "DISPATCH_PUBLISHED",
                        "timestamp": timestamp,
                        "dispatch": payload,
                        "repository": GITHUB_PUBLIC_VAULT
                    }).encode('utf-8')
                    req = urllib.request.Request(webhook_url, data=req_payload, headers={'Content-Type': 'application/json'})
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        webhook_status = f"Relayed to external webhook (HTTP {resp.status})"
                except Exception as wh_err:
                    webhook_status = f"Webhook notice: {str(wh_err)}"
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'status': 'SUCCESS',
                'message': f'Dispatch {dispatch_id} recorded in ledger. {webhook_status}'
            }).encode('utf-8'))
        else:
            self.send_error(404)

if __name__ == "__main__":
    os.chdir(os.path.join(BASE_DIR, "ebony_dashboard"))
    server = HTTPServer(('localhost', 8000), HVFCommHandler)
    print("Ebony Communication Server Live on port 8000... Awaiting Directives.")
    server.serve_forever()
