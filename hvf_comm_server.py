import os
import json
import secrets
import datetime
import urllib.request
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from google import genai

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_DIR = os.path.join(BASE_DIR, "knowledge_vault")
DATA_DIR = os.path.join(BASE_DIR, "ebony_dashboard", "data")
LOG_FILE = os.path.join(DATA_DIR, "dispatch_transmission_ledger.log")
ENV_PATH = os.path.join(BASE_DIR, ".env")

MASTER_PASSPHRASE = "HVF-Test-2026"
active_tokens = set()

api_key = None
if os.path.exists(ENV_PATH):
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("GEMINI_API_KEY="):
                api_key = line.split("=", 1)[1].strip().strip('"').strip("'")

client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
        print("[+] Google GenAI Client Connected.")
    except Exception as e:
        print(f"[!] Neural Client Init Error: {e}")

LOGIN_HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HVF Security Gateway</title>
    <style>
        body { margin: 0; background: #0a0e17; color: #f9fafb; font-family: sans-serif; display: flex; height: 100vh; align-items: center; justify-content: center; }
        .auth-card { background: #111827; border: 1px solid #1f2937; padding: 36px; border-radius: 12px; width: 400px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.9); }
        h2 { color: #10b981; margin-top: 0; }
        p { color: #9ca3af; font-size: 13px; margin-bottom: 24px; }
        input { width: 100%; padding: 14px; border-radius: 6px; border: 1px solid #1f2937; background: #040711; color: #fff; font-size: 15px; margin-bottom: 16px; text-align: center; box-sizing: border-box; }
        button { width: 100%; padding: 14px; border-radius: 6px; background: #10b981; border: none; color: #000; font-weight: bold; font-size: 15px; cursor: pointer; }
        .err { color: #ef4444; font-size: 13px; margin-top: 14px; font-weight: bold; }
    </style>
</head>
<body>
    <form class="auth-card" method="POST" action="/login">
        <h2>HVF Security Gateway</h2>
        <p>Native Server-Side Authentication.<br>Enter your Secret Executive Passphrase to unlock Ebony.</p>
        <input type="password" name="passphrase" placeholder="Enter passphrase..." autofocus autocomplete="off" required />
        <button type="submit">Unlock Node</button>
        <div class="err">{{ERROR}}</div>
    </form>
</body>
</html>'''

DASHBOARD_HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HVF Ebony - Sovereign Dashboard</title>
    <style>
        body { margin: 0; background: #0a0e17; color: #f9fafb; font-family: sans-serif; display: flex; flex-direction: column; height: 100vh; }
        header { padding: 16px 24px; background: #111827; border-bottom: 1px solid #1f2937; display: flex; justify-content: space-between; align-items: center; }
        .badge { background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 4px 10px; border-radius: 20px; font-size: 12px; border: 1px solid #10b981; }
        #chat-window { flex: 1; padding: 24px; overflow-y: auto; display: flex; flex-direction: column; gap: 16px; }
        .message { max-width: 75%; padding: 14px 18px; border-radius: 8px; line-height: 1.5; font-size: 14px; white-space: pre-wrap; }
        .msg-ceo { align-self: flex-end; background: #1e293b; border-left: 3px solid #3b82f6; }
        .msg-ebony { align-self: flex-start; background: #111827; border-left: 3px solid #10b981; }
        #input-panel { padding: 16px 24px; background: #111827; border-top: 1px solid #1f2937; display: flex; gap: 12px; }
        input { flex: 1; padding: 12px 16px; border-radius: 6px; background: #040711; border: 1px solid #1f2937; color: #fff; font-size: 14px; }
        button { padding: 12px 24px; border-radius: 6px; background: #10b981; border: none; color: #000; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <header>
        <div><strong style="font-size: 16px;">Humphrey Virtual Farm</strong> | Ebony Chief of Staff</div>
        <div class="badge">OPSEC Gated - Sovereign Node Active</div>
    </header>
    <div id="chat-window">
        <div class="message msg-ebony">Sovereign Node Authenticated. Knowledge Vault memory ready. Standing by.</div>
    </div>
    <div id="input-panel">
        <input type="text" id="user-msg" placeholder="Transmit directive to Ebony..." onkeydown="if(event.key==='Enter') sendDirective()" />
        <button onclick="sendDirective()">Transmit</button>
    </div>
    <script>
        async function sendDirective() {
            const input = document.getElementById('user-msg');
            const msg = input.value.trim();
            if (!msg) return;
            const chat = document.getElementById('chat-window');
            chat.innerHTML += <div class="message msg-ceo"> + msg + </div>;
            input.value = '';
            chat.scrollTop = chat.scrollHeight;
            try {
                // The browser automatically sends the secure HTTP cookie with this request
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: msg })
                });
                const data = await res.json();
                chat.innerHTML += <div class="message msg-ebony"> + (data.reply || data.error) + </div>;
                chat.scrollTop = chat.scrollHeight;
            } catch (err) {
                chat.innerHTML += <div class="message msg-ebony" style="color:#ef4444;">Transmission failed</div>;
            }
        }
    </script>
</body>
</html>'''

def load_knowledge_vault():
    aggregated_context = {}
    if os.path.exists(VAULT_DIR):
        for filename in os.listdir(VAULT_DIR):
            if filename.endswith(".txt") or filename.endswith(".md"):
                try:
                    with open(os.path.join(VAULT_DIR, filename), "r", encoding="utf-8") as vf:
                        aggregated_context[filename] = vf.read().strip()
                except: pass
    return aggregated_context

class HVFCommHandler(BaseHTTPRequestHandler):
    def parse_cookies(self):
        cookie_header = self.headers.get('Cookie')
        cookies = {}
        if cookie_header:
            for item in cookie_header.split(';'):
                if '=' in item:
                    k, v = item.strip().split('=', 1)
                    cookies[k] = v
        return cookies

    def is_authenticated(self):
        cookies = self.parse_cookies()
        token = cookies.get('hvf_session')
        return token in active_tokens

    def do_GET(self):
        if self.path == '/' or self.path.startswith('/?'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # If the browser already has the valid cookie, show the dashboard immediately
            if self.is_authenticated():
                self.wfile.write(DASHBOARD_HTML.encode('utf-8'))
            else:
                # If no valid cookie, show the login form
                error_msg = "Invalid Passphrase." if "error=1" in self.path else ""
                self.wfile.write(LOGIN_HTML.replace("{{ERROR}}", error_msg).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        # 1. Native Form Submission Endpoint
        if self.path == '/login':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed = parse_qs(post_data)
            passphrase = parsed.get('passphrase', [''])[0].strip()
            
            print(f"[*] Native Form Auth attempt received")
            if passphrase == MASTER_PASSPHRASE:
                token = secrets.token_hex(24)
                active_tokens.add(token)
                print("[+] PASS MATCH: Session Cookie Issued!")
                # Issue secure cookie and physically redirect the browser to the root page
                self.send_response(303)
                self.send_header('Location', '/')
                self.send_header('Set-Cookie', f'hvf_session={token}; Path=/')
                self.end_headers()
            else:
                print("[!] PASS MISMATCH: Redirecting back to login")
                self.send_response(303)
                self.send_header('Location', '/?error=1')
                self.end_headers()
            return

        # 2. Chat API Endpoint
        if self.path == '/api/chat':
            if not self.is_authenticated():
                self.send_response(403)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"error": "ACCESS_DENIED: Invalid Cookie"}')
                return

            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try: data = json.loads(post_data.decode('utf-8'))
            except: data = {}
            user_message = data.get('message', '')
            
            response_text = ""
            if client:
                try:
                    vault_dict = load_knowledge_vault()
                    vault_formatted = "\n".join([f"DOC: {k}\n{v}" for k, v in vault_dict.items()])
                    prompt = f"Knowledge Base:\n{vault_formatted}\n\nRole: You are Ebony, authentic AI Chief of Staff. Speak naturally.\nCEO: {user_message}\nEbony:"
                    res = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
                    response_text = res.text.strip()
                except Exception as e:
                    response_text = f"Local Node Active. Knowledge Vault standing by."
            else:
                response_text = "Local Node Active. Knowledge Vault standing by."
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'reply': response_text}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server = ThreadingHTTPServer(('127.0.0.1', 8080), HVFCommHandler)
    print("=====================================================")
    print(" EBONY NATIVE FORM SERVER LIVE ON PORT 8080")
    print("=====================================================")
    server.serve_forever()
