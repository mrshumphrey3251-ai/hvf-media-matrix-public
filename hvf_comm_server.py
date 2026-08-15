import os
import json
import re
import datetime
import urllib.request
from http.server import SimpleHTTPRequestHandler, HTTPServer
from google import genai

# HVF Media Matrix - Dedicated Comm Server
# Engineered with Knowledge Vault Ingestion, Federal NWS Telemetry, & Autonomous Local Core Fallback

env_path = os.path.join(os.path.dirname(__file__), ".env")
api_key = None
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                api_key = line.strip().split("=", 1)[1]
                break

client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Neural Client Init Error: {e}")

def load_knowledge_vault():
    vault_path = os.path.join(os.path.dirname(__file__), "knowledge_vault")
    aggregated_context = {}
    if os.path.exists(vault_path):
        for filename in os.listdir(vault_path):
            if filename.endswith(".txt") or filename.endswith(".md"):
                file_full_path = os.path.join(vault_path, filename)
                try:
                    with open(file_full_path, "r", encoding="utf-8") as vf:
                        aggregated_context[filename] = vf.read()
                except Exception as ex:
                    aggregated_context[filename] = f"Error reading file: {str(ex)}"
    return aggregated_context

def autonomous_local_engine(user_message, vault_data, current_time, environment):
    # Fully autonomous on-premise fallback response engine
    msg_lower = user_message.lower()
    vault_summary = ""
    for doc_name, content in vault_data.items():
        vault_summary += f"\n--- {doc_name} ---\n{content}\n"
    
    # Check for direct Knowledge Vault queries
    if any(k in msg_lower for k in ["directive", "objective", "phase", "mission", "vault", "knowledge"]):
        extracted_info = []
        for line in vault_summary.splitlines():
            if ":" in line and not line.startswith("---"):
                extracted_info.append(line.strip())
        
        details = " ".join(extracted_info) if extracted_info else vault_summary.strip()
        return (
            f"[AUTONOMOUS CORE] Executive Report as of {current_time}. "
            f"Knowledge Vault Telemetry: {details}. "
            f"Environmental Status: {environment}. Standing by for operational execution."
        )
    
    if any(k in msg_lower for k in ["time", "date", "status"]):
        return (
            f"[AUTONOMOUS CORE] Systems operational as of {current_time}. "
            f"{environment}. Vault Status: {len(vault_data)} documents indexed and ready."
        )

    return (
        f"[AUTONOMOUS CORE] Directive received: '{user_message}'. "
        f"Processed locally against {len(vault_data)} Knowledge Vault documents at {current_time}."
    )

def get_nws_telemetry(lat, lon):
    if not lat or not lon:
        return "Location telemetry pending hardware link"
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
            
            # Attempt Cloud Engine first if client initialized
            if client:
                prompt = (
                    f"System Context: The current local time is {current_time}. {environment}.\n"
                    f"--- PROPRIETARY KNOWLEDGE VAULT DATA ---\n{vault_formatted}\n----------------------------------------\n"
                    f"You are Ebony, Executive AI assistant for the CEO of Humphrey Virtual Farm. "
                    f"Answer the CEO: '{user_message}' using the Vault data concisely. Do not use markdown."
                )
                try:
                    res = client.models.generate_content(model='gemini-flash-latest', contents=prompt)
                    response_text = res.text.strip()
                except Exception:
                    # Cloud throttled or rate-limited: seamless failover to Autonomous Local Core
                    response_text = autonomous_local_engine(user_message, vault_dict, current_time, environment)
            else:
                response_text = autonomous_local_engine(user_message, vault_dict, current_time, environment)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'reply': response_text}).encode('utf-8'))
        else:
            self.send_error(404)

if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(__file__), "ebony_dashboard"))
    server = HTTPServer(('localhost', 8000), HVFCommHandler)
    print("Ebony Autonomous Server Live on port 8000... Awaiting Directives.")
    server.serve_forever()
