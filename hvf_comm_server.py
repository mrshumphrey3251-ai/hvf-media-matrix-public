import os
import json
import re
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
            if line.startswith("GEMINI_API_KEY="):
                api_key = line.strip().split("=", 1)[1]
            elif line.startswith("OUTBOUND_WEBHOOK_URL="):
                webhook_url = line.strip().split("=", 1)[1]

client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Neural Client Init Error: {e}")

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

def autonomous_local_engine(user_message, vault_data, current_time, environment):
    msg_lower = user_message.lower().strip()
    
    # 1. Social Media / Dispatch Generation
    if any(k in msg_lower for k in ["linkedin", "post", "social", "dispatch", "broadcast"]):
        return (
            f"[AUTONOMOUS DISPATCH ENGINE] Executive Release ({current_time}):\n\n"
            f"Humphrey Virtual Farm is advancing digital media matrix automation. "
            f"Current milestone: Complete integration of proprietary RAG memory cores, OPSEC-shielded geofencing, "
            f"and real-time federal environmental telemetry.\n\n"
            f"Architecture Blueprint: {GITHUB_PUBLIC_VAULT}\n\n"
            f"#HumphreyVirtualFarm #DigitalTransformation #AgTech #AI #AutonomousSystems"
            f"{REPO_SIGNATURE}"
        )
    
    # 2. Block-Aware Semantic Search Across All Vault Documents
    query_words = set([w for w in re.findall(r'\w+', msg_lower) if len(w) >= 3 and w not in ["what", "are", "our", "the", "and", "ebony", "with", "for", "powering", "regarding"]])
    
    matched_blocks = []
    for doc_name, content in vault_data.items():
        # Split document by major blocks/sections
        blocks = [b.strip() for b in content.split("\n\n") if b.strip() and not b.startswith("===") and not b.startswith("CLASSIFICATION")]
        for block in blocks:
            block_words = set(re.findall(r'\w+', block.lower()))
            overlap = query_words.intersection(block_words)
            if len(overlap) > 0:
                matched_blocks.append((len(overlap), block))
                
    if matched_blocks:
        matched_blocks.sort(key=lambda x: x[0], reverse=True)
        top_blocks = [item[1] for item in matched_blocks[:2]]
        return (
            f"Executive Technical & Knowledge Briefing ({current_time}):\n\n" +
            "\n\n".join(top_blocks) +
            f"{REPO_SIGNATURE}"
        )

    # 3. Status Check Fallback
    if any(k in msg_lower for k in ["status", "system", "weather", "telemetry", "diagnostics"]):
        return (
            f"Executive Telemetry Report as of {current_time}:\n"
            f"- Atmospheric State: {environment}\n"
            f"- Knowledge Vault: {len(vault_data)} Active Strategic Files\n"
            f"- Media Matrix Node 1: Armed & Ready\n"
            f"- OPSEC Geofence: 2-Decimal Active Shield"
            f"{REPO_SIGNATURE}"
        )

    # 4. General Conversational Fallback
    return (
        f"Directive received: '{user_message}'. All core nodes are operational under current protocols. "
        f"Standing by for specific operational commands."
        f"{REPO_SIGNATURE}"
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
            vault_formatted = "\n".join([f"[{k}]: {v}" for k, v in vault_dict.items()])
            
            response_text = ""
            if client:
                prompt = (
                    f"System Context: The current local time is {current_time}. {environment}.\n"
                    f"--- PROPRIETARY KNOWLEDGE VAULT DATA ---\n{vault_formatted}\n----------------------------------------\n"
                    f"You are Ebony, Executive AI assistant for the CEO of Humphrey Virtual Farm. "
                    f"Answer the CEO: '{user_message}' thoroughly using the Knowledge Vault files. Do not use markdown.\n"
                    f"MANDATORY REQUIREMENT: Always append this exact signature at the end of your response:\n"
                    f"{REPO_SIGNATURE}"
                )
                try:
                    res = client.models.generate_content(model='gemini-flash-latest', contents=prompt)
                    response_text = res.text.strip()
                except Exception:
                    response_text = autonomous_local_engine(user_message, vault_dict, current_time, environment)
            else:
                response_text = autonomous_local_engine(user_message, vault_dict, current_time, environment)
            
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
                
            webhook_status = "Local Ledger Only (No external webhook configured)"
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
                    webhook_status = f"Webhook relay notice: {str(wh_err)}"
                
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
    print("Ebony Block-Aware Semantic Server Live on port 8000... Awaiting Directives.")
    server.serve_forever()
