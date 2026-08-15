import os
import json
import datetime
import urllib.request
from http.server import SimpleHTTPRequestHandler, HTTPServer
from google import genai

# HVF Media Matrix - Dedicated Comm Server
# Engineered for Dynamic Mobile Hardware GPS Bridge with OPSEC Geofence Shield

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

def get_environmental_telemetry(lat, lon):
    if not lat or not lon:
        return "Location data pending user hardware authorization. Cannot verify weather."
    try:
        # OPSEC GEOFENCE SHIELD: Truncate to 2 decimal places (~1km radius)
        # Prevents exact street-level tracking from external APIs while maintaining neighborhood weather accuracy.
        safe_lat = round(float(lat), 2)
        safe_lon = round(float(lon), 2)
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={safe_lat}&longitude={safe_lon}&current_weather=true&temperature_unit=fahrenheit"
        w_req = urllib.request.Request(weather_url, headers=headers)
        with urllib.request.urlopen(w_req, timeout=5) as w_response:
            w_data = json.loads(w_response.read().decode('utf-8'))
            
        temp = w_data['current_weather']['temperature']
        return f"Secure Geofenced Coordinates (Truncated for OPSEC): Latitude {safe_lat}, Longitude {safe_lon}. Local Weather: {temp} degrees Fahrenheit."
    except Exception as e:
        return f"Environmental telemetry unavailable. Diagnostics: {str(e)}"

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
                environment = get_environmental_telemetry(lat, lon)
                
                prompt = f"System Context: The current local time is {current_time}. {environment}. You are Ebony, the highly intelligent Executive AI assistant for the CEO of Humphrey Virtual Farm. The CEO says: '{user_message}'. Respond directly, professionally, and concisely as an elite AI subordinate. Do not use markdown formatting."
                
                try:
                    response = client.models.generate_content(
                        model='gemini-flash-latest',
                        contents=prompt
                    )
                    response_text = response.text.strip()
                except Exception as e:
                    try:
                        response_fallback = client.models.generate_content(
                            model='gemini-2.5-flash-lite',
                            contents=prompt
                        )
                        response_text = f"[FAILOVER ENGAGED] {response_fallback.text.strip()}"
                    except Exception as fallback_error:
                        response_text = f"Transmission Error: {str(fallback_error)}"
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'reply': response_text}).encode('utf-8'))
        else:
            self.send_error(404)

if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(__file__), "ebony_dashboard"))
    server = HTTPServer(('localhost', 8000), HVFCommHandler)
    print("Ebony Secure Mobile Server Live on port 8000... Awaiting Executive Directives.")
    server.serve_forever()
