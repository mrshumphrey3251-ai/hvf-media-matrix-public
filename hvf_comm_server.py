import os
import json
import datetime
import urllib.request
from http.server import SimpleHTTPRequestHandler, HTTPServer
from google import genai

# HVF Media Matrix - Dedicated Comm Server
# Multi-Document Knowledge Ingestion, Federal NWS Telemetry, & Matrix Dispatch Engine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_DIR = os.path.join(BASE_DIR, "knowledge_vault")
ENV_PATH = os.path.join(BASE_DIR, ".env")

api_key = None
if os.path.exists(ENV_PATH):
    with open(ENV_PATH, "r", encoding="utf-8") as f:
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
    msg_lower = user_message.lower()
    
    # Check for Social Media / Dispatch Generation directive
    if any(k in msg_lower for k in ["linkedin", "post", "social", "dispatch", "media matrix", "broadcast"]):
        directive_doc = vault_data.get("hvf_master_directive.txt", "")
        ops_doc = vault_data.get("hvf_operations_manual.txt", "")
        
        return (
            f"[AUTONOMOUS DISPATCH ENGINE] Executive Media Release Draft ({current_time}):\n\n"
            f"Headline: Autonomous Infrastructure in Precision Agriculture & Digital Systems\n\n"
            f"Operational Update: Humphrey Virtual Farm (HVF) is actively advancing digital media matrix automation. "
            f"Current milestone: Complete integration of proprietary RAG memory cores, OPSEC-shielded geofencing, "
            f"and real-time federal environmental telemetry.\n\n"
            f"Key Focus: Total infrastructure dominance through zero-latency automated pipelines.\n\n"
            f"#HumphreyVirtualFarm #DigitalTransformation #AgTech #AI #AutonomousSystems #ExecutiveLeadership"
        )
    
    matching_lines = []
    for doc_name, content in vault_data.items():
        doc_lines = [l.strip() for l in content.splitlines() if l.strip() and not l.startswith("===")]
        if any(term in msg_lower for term in ["node", "operation", "security", "manual"]) and "operations" in doc_name:
            matching_lines.extend(doc_lines)
        elif any(term in msg_lower for term in ["directive", "mission", "objective", "phase"]) and "directive" in doc_name:
            matching_lines.extend(doc_lines)
            
    if not matching_lines:
        for content in vault_data.values():
            matching_lines.extend([l.strip() for l in content.splitlines() if l.strip()])
            
    vault_summary = " | ".join(matching_lines) if matching_lines else "No active directives found."
    
    return (
        f"[AUTONOMOUS CORE] Executive Briefing as of {current_time}. "
        f"Vault Directives: {vault_summary}. "
        f"Environmental Status: {environment}. Ready for next directive."
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
                    f"Answer the CEO: '{user_message}' using the Vault data concisely. Do not use markdown."
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
        else:
            self.send_error(404)

if __name__ == "__main__":
    os.chdir(os.path.join(BASE_DIR, "ebony_dashboard"))
    server = HTTPServer(('localhost', 8000), HVFCommHandler)
    print("Ebony Matrix Dispatch Server Live on port 8000... Awaiting Directives.")
    server.serve_forever()
