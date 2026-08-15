import os
import json
import time
import datetime
import urllib.request
from http.server import SimpleHTTPRequestHandler, HTTPServer
from google import genai

# HVF Media Matrix - Dedicated Comm Server
# Engineered with Knowledge Vault Ingestion & Verified Active Model Cascade

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
    aggregated_context = ""
    if os.path.exists(vault_path):
        for filename in os.listdir(vault_path):
            if filename.endswith(".txt") or filename.endswith(".md"):
                file_full_path = os.path.join(vault_path, filename)
                try:
                    with open(file_full_path, "r", encoding="utf-8") as vf:
                        aggregated_context += f"\n[DOCUMENT: {filename}]\n" + vf.read() + "\n"
                except Exception as ex:
                    aggregated_context += f"\n[ERROR READING {filename}: {str(ex)}]\n"
    return aggregated_context if aggregated_context else "Knowledge Vault contains no active documents."

def get_nws_telemetry(lat, lon):
    if not lat or not lon:
        return "Location data pending user hardware authorization or hardware unavailable."
    try:
        safe_lat = round(float(lat), 2)
        safe_lon = round(float(lon), 2)
        
        headers = {'User-Agent': '(HVF-Media-Matrix-Industrial-Node, ceo@humphreyvirtualfarm.com)'}
        points_url = f"https://api.weather.gov/points/{safe_lat},{safe_lon}"
        req1 = urllib.request.Request(points_url, headers=headers)
        with urllib.request.urlopen(req1, timeout=10) as r1:
            grid_data = json.loads(r1.read().decode('utf-8'))
            
        forecast_url = grid_data['properties']['forecast']
        req2 = urllib.request.Request(forecast_url, headers=headers)
        with urllib.request.urlopen(req2, timeout=10) as r2:
            forecast_data = json.loads(r2.read().decode('utf-8'))
            
        current_weather = forecast_data['properties']['periods'][0]['detailedForecast']
        return f"Federal NWS Telemetry (Lat: {safe_lat}, Lon: {safe_lon}). Current Conditions: {current_weather}"
    except Exception as e:
        return f"Federal NWS Telemetry unavailable. Diagnostics: {str(e)}"

def generate_with_shield(prompt):
    # Models strictly verified from the diagnostic list
    models_to_try = [
        'gemini-flash-latest',
        'gemini-3.5-flash',
        'gemini-3.7-flash',
        'gemini-pro-latest'
    ]
    last_error = ""
    for model_name in models_to_try:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return response.text.strip()
            except Exception as e:
                err_str = str(e)
                last_error = f"[{model_name}] {err_str}"
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    time.sleep(2)
                    continue
                else:
                    break
    return f"Transmission Error: {last_error}"

class HVFCommHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            user_message = data.get('message', '')
            lat = data.get('lat')
            lon = data.get('lon')
            
            response_text = "ERROR: Cognitive Core Offline."
            if client:
                current_time = datetime.datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
                environment = get_nws_telemetry(lat, lon)
                vault_data = load_knowledge_vault()
                
                prompt = (
                    f"System Context: The current local time is {current_time}. {environment}.\n"
                    f"--- PROPRIETARY KNOWLEDGE VAULT DATA ---\n{vault_data}\n----------------------------------------\n"
                    f"You are Ebony, the highly intelligent Executive AI assistant for the CEO of Humphrey Virtual Farm. "
                    f"You have full access to the Knowledge Vault data above. The CEO says: '{user_message}'. "
                    f"Respond directly, professionally, and concisely as an elite AI subordinate, utilizing the Vault data when relevant. "
                    f"Do not use markdown formatting."
                )
                response_text = generate_with_shield(prompt)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'reply': response_text}).encode('utf-8'))
        else:
            self.send_error(404)

if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(__file__), "ebony_dashboard"))
    server = HTTPServer(('localhost', 8000), HVFCommHandler)
    print("Ebony Knowledge Server Live on port 8000... Awaiting Directives.")
    server.serve_forever()
