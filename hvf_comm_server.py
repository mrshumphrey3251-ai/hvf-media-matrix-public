import os
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
import google.generativeai as genai

# HVF Media Matrix - Dedicated Comm Server (Private)
# Engineered for live read/write cognitive routing (Universal Model Hotfix)

env_path = os.path.join(os.path.dirname(__file__), ".env")
api_key = None
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                api_key = line.strip().split("=", 1)[1]
                break

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

class HVFCommHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            user_message = data.get('message', '')
            
            response_text = "ERROR: Cognitive Core Offline."
            if model:
                try:
                    prompt = f"You are Ebony, the highly intelligent Executive AI assistant for the CEO of Humphrey Virtual Farm. The CEO says: '{user_message}'. Respond directly, professionally, and concisely as an elite AI subordinate. Do not use markdown formatting."
                    response = model.generate_content(prompt)
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
