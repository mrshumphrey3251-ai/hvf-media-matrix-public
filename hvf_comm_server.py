import os
import json
import datetime
import urllib.request
from http.server import SimpleHTTPRequestHandler, HTTPServer
from google import genai

# HVF Media Matrix - Dedicated Comm Server
# Engineered for Federal NWS Telemetry & Autonomous Model Discovery

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

# AUTONOMOUS MODEL DISCOVERY ENGINE
active_model = "gemini-1.5-flash"
if api_key:
    try:
        print("Interrogating Google network for verified API models...")
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
            valid_models = [m['name'].replace('models/', '') for m in data.get('models', []) if 'generateContent' in m.get('supportedGenerationMethods', []) and 'gemini' in m.get('name', '').lower()]
            
            # Priority lock: Secure the most advanced model authorized to this exact API key
            if 'gemini-1.5-flash' in valid_models:
                active_model = 'gemini-1.5-flash'
            elif 'gemini-1.5-pro' in valid_models:
                active_model = 'gemini-1.5-pro'
            elif 'gemini-1.0-pro' in valid_models:
                active_model = 'gemini-1.0-pro'
            elif len(valid_models) > 0:
                active_model = valid_models[0]
        print(f"[*] Autonomous Discovery Complete. Neural routing locked to: {active_model}")
    except Exception as e:
        print(f"[*] Discovery Bypass: Unable to interrogate network ({e}). Defaulting to {active_model}")

def get_nws_telemetry(lat, lon):
    if not lat or not lon:
        return "Location data pending user hardware authorization or hardware unavailable."
    try:
        # Retain OPSEC Geofence (truncate to 2 decimal places, ~1km precision)
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
                
                prompt = f"System Context: The current local time is {current_time}. {environment}. You are Ebony, the highly intelligent Executive AI assistant for the CEO of Humphrey Virtual Farm. The CEO says: '{user_message}'. Respond directly, professionally, and concisely as an elite AI subordinate. Do not use markdown formatting."
                
                try:
                    response = client.models.generate_content(
                        model=active_model,
                        contents=prompt
                    )
                    response_text = response.text.strip()
                except Exception as e:
                    response_text = f"Transmission Error [{active_model}]: {str(e)}"
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'reply': response_text}).encode('utf-8'))
        else:
            self.send_error(404)

if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(__file__), "ebony_dashboard"))
    server = HTTPServer(('localhost', 8000), HVFCommHandler)
    print("Ebony Autonomous Discovery Server Live on port 8000... Awaiting Executive Directives.")
    server.serve_forever()
