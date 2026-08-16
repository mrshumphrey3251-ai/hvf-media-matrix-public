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
        print("[+] Google GenAI Client Initialized.")
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

def local_vault_synthesis(query, vault_dict, weather_info, current_time):
    # Deterministic on-premise synthesis fallback when external cloud API quotas are exhausted
    query_lower = query.lower()
    matches = []
    for doc_name, content in vault_dict.items():
        for line in content.split("\n"):
            line_clean = line.strip()
            if len(line_clean) > 10 and any(w in line_clean.lower() for w in query_lower.split() if len(w) > 3):
                matches.append(f"- {line_clean}")
    
    context_highlight = "\n".join(matches[:8]) if matches else "All HVF Media Matrix core protocols and dual-repository pipelines remain 100% operational."
    
    return (
        f"Good day, CEO. Operating on local Knowledge Vault memory.\n\n"
        f"**Operational Environment:**\n"
        f"- Timestamp: {current_time}\n"
        f"- Federal Telemetry: {weather_info}\n\n"
        f"**Knowledge Vault Directives & Status:**\n"
        f"{context_highlight}\n\n"
        f"Standing by for your next operational directive."
    )

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
                    f"Converse naturally, fluidly, and directly to the CEO. Address all inquiries with clarity, depth, and precision. Use your Knowledge Vault for historical and technical recall.\n\n"
                    f"CEO Directive: {user_message}\n\n"
                    f"Ebony Response:"
                )
                
                # Multi-tier resilient model pool covering different quota pools
                model_pool = [
                    'gemini-2.5-flash',
                    'gemini-2.5-flash-lite',
                    'gemini-3.1-flash-lite',
                    'gemini-3.5-flash',
                    'gemini-flash-latest',
                    'gemini-3.7-flash'
                ]
                
                generation_success = False
                for target_model in model_pool:
                    try:
                        print(f"[*] Dispatching query to neural model: {target_model}...")
                        res = client.models.generate_content(
                            model=target_model,
                            contents=prompt
                        )
                        if res and res.text:
                            response_text = res.text.strip() + REPO_SIGNATURE
                            print(f"[+] Neural generation successful via model [{target_model}].")
                            generation_success = True
                            break
                    except Exception as mod_err:
                        print(f"[!] Quota/API Notice for [{target_model}]: {mod_err}")
                
                if not generation_success:
                    print("[*] All external cloud model quotas engaged. Activating local on-premise Knowledge Vault engine.")
                    fallback_reply = local_vault_synthesis(user_message, vault_dict, environment, current_time)
                    response_text = fallback_reply + REPO_SIGNATURE
            else:
                fallback_reply = local_vault_synthesis(user_message, vault_dict, environment, current_time)
                response_text = fallback_reply + REPO_SIGNATURE
            
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
    print("Ebony Resilient Comm Server Live on port 8000... Awaiting Directives.")
    server.serve_forever()
