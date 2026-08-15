import os
import json
import datetime
from http.server import SimpleHTTPRequestHandler, HTTPServer
from google import genai

# HVF Media Matrix - Dedicated Comm Server
# Engineered for Next-Gen Google GenAI SDK & Live Temporal Awareness

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

class HVFCommHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            user_message = data.get('message', '')
            
            response_text = "ERROR: Cognitive Core Offline."
            if client:
                try:
                    current_time = datetime.datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
                    prompt = f"System Context: The current local time is {current_time}. You are Ebony, the highly intelligent Executive AI assistant for the CEO of Humphrey Virtual Farm. The CEO says: '{user_message}'. Respond directly, professionally, and concisely as an elite AI subordinate. Do not use markdown formatting."
                    response = client.models.generate_content(
                        model='gemini-flash-latest',
                        contents=prompt
                    )
                    response_text = response.text.strip()
                except Exception as e:
                    response_text = f"Transmission Error: {str(e)}"
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'reply': response_text}).encode('utf-8'))
        else:
            self.send_error(404)

if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(__file__), "ebony_dashboard"))
    server = HTTPServer(('localhost', 8000), HVFCommHandler)
    print("Ebony Cognitive Comm Server Live on port 8000... Awaiting Executive Directives.")
    server.serve_forever()
