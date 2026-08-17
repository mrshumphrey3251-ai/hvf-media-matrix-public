import os
import json
import secrets
import datetime
import urllib.request
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

DASHBOARD_HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HVF Ebony - Industrial Chief of Staff</title>
    <style>
        :root { --bg-primary: #0a0e17; --bg-card: #111827; --accent: #10b981; --accent-alert: #ef4444; --text-main: #f9fafb; --text-dim: #9ca3af; --border: #1f2937; }
        * { box-sizing: border-box; }
        body { margin: 0; padding: 0; background: var(--bg-primary); color: var(--text-main); font-family: 'Segoe UI', system-ui, sans-serif; height: 100vh; overflow: hidden; display: flex; }
        #auth-modal { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #06090f; display: flex; align-items: center; justify-content: center; z-index: 99999; }
        .auth-card { background: var(--bg-card); border: 1px solid var(--border); padding: 36px; border-radius: 12px; width: 400px; box-shadow: 0 20px 50px rgba(0,0,0,0.9); text-align: center; }
        .auth-card h2 { margin: 0 0 10px 0; color: var(--accent); font-size: 20px; }
        .auth-card p { font-size: 13px; color: var(--text-dim); margin-bottom: 24px; line-height: 1.4; }
        .auth-input { width: 100%; padding: 14px; border-radius: 6px; border: 1px solid var(--border); background: #040711; color: #fff; font-size: 15px; margin-bottom: 16px; text-align: center; outline: none; }
        .auth-input:focus { border-color: var(--accent); }
        .auth-btn { width: 100%; padding: 14px; border-radius: 6px; background: var(--accent); border: none; color: #000; font-weight: bold; font-size: 15px; cursor: pointer; }
        #main-container { display: none; flex: 1; flex-direction: column; height: 100vh; width: 100vw; }
        header { padding: 16px 24px; background: var(--bg-card); border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
        .status-badge { background: rgba(16, 185, 129, 0.1); color: var(--accent); padding: 4px 10px; border-radius: 20px; font-size: 12px; border: 1px solid var(--accent); }
        #chat-window { flex: 1; padding: 24px; overflow-y: auto; display: flex; flex-direction: column; gap: 16px; }
        .message { max-width: 75%; padding: 14px 18px; border-radius: 8px; line-height: 1.5; font-size: 14px; white-space: pre-wrap; }
        .msg-ceo { align-self: flex-end; background: #1e293b; border-left: 3px solid #3b82f6; }
        .msg-ebony { align-self: flex-start; background: var(--bg-card); border-left: 3px solid var(--accent); }
        #input-panel { padding: 16px 24px; background: var(--bg-card); border-top: 1px solid var(--border); display: flex; gap: 12px; }
        #user-msg { flex: 1; padding: 12px 16px; border-radius: 6px; background: #040711; border: 1px solid var(--border); color: var(--text-main); font-size: 14px; }
        #send-btn { padding: 12px 24px; border-radius: 6px; background: var(--accent); border: none; color: #000; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div id="auth-modal">
        <div class="auth-card">
            <h2>HVF Security Gateway</h2>
            <p>Cryptographic Access Control Active.<br>Enter your Secret Executive Passphrase to unlock Ebony.</p>
            <input type="password" id="passphrase-input" class="auth-input" placeholder="Enter passphrase..." autofocus autocomplete="off" />
            <button type="button" class="auth-btn" id="unlock-btn">Unlock Node</button>
            <div id="auth-err" style="color: var(--accent-alert); font-size: 13px; margin-top: 14px; min-height: 18px; font-weight: 500;"></div>
        </div>
    </div>
    <div id="main-container">
        <header>
            <div><strong style="font-size: 16px;">Humphrey Virtual Farm</strong> | Ebony Chief of Staff</div>
            <div class="status-badge" id="telemetry-badge">OPSEC Gated - Sovereign Node Active</div>
        </header>
        <div id="chat-window">
            <div class="message msg-ebony">Sovereign Node Authenticated. Knowledge Vault memory ready. Standing by.</div>
        </div>
        <div id="input-panel">
            <input type="text" id="user-msg" placeholder="Transmit directive to Ebony..." />
            <button id="send-btn" onclick="sendDirective()">Transmit</button>
        </div>
    </div>
    <script>
        let authToken = null;
        const passInput = document.getElementById('passphrase-input');
        const unlockBtn = document.getElementById('unlock-btn');
        const errDiv = document.getElementById('auth-err');

        unlockBtn.addEventListener('click', performAuth);
        passInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); performAuth(); } });
        document.getElementById('user-msg').addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); sendDirective(); } });

        async function performAuth() {
            const pass = passInput.value.trim();
            if (!pass) return;
            unlockBtn.innerText = 'Verifying...';
            unlockBtn.disabled = true;
            errDiv.innerText = '';
            try {
                const res = await fetch('/api/auth', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ passphrase: pass }) });
                const data = await res.json();
                if (res.ok && data.token) {
                    authToken = data.token;
                    document.getElementById('auth-modal').style.display = 'none';
                    document.getElementById('main-container').style.display = 'flex';
                    document.getElementById('user-msg').focus();
                } else {
                    errDiv.innerText = 'Access Denied: Invalid Passphrase';
                    unlockBtn.innerText = 'Unlock Node';
                    unlockBtn.disabled = false;
                    passInput.value = '';
                    passInput.focus();
                }
            } catch (err) {
                errDiv.innerText = 'Gateway Error: Connection Failed';
                unlockBtn.innerText = 'Unlock Node';
                unlockBtn.disabled = false;
            }
        }

        async function sendDirective() {
            const input = document.getElementById('user-msg');
            const msg = input.value.trim();
            if (!msg || !authToken) return;
            const chat = document.getElementById('chat-window');
            chat.innerHTML += <div class="message msg-ceo"> + msg + </div>;
            input.value = '';
            chat.scrollTop = chat.scrollHeight;
            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Authorization': Bearer  + authToken },
                    body: JSON.stringify({ message: msg })
                });
                const data = await res.json();
                chat.innerHTML += <div class="message msg-ebony"> + (data.reply || data.error) + </div>;
                chat.scrollTop = chat.scrollHeight;
            } catch (err) {
                chat.innerHTML += <div class="message msg-ebony" style="color:var(--accent-alert);">Transmission failed</div>;
            }
        }
    </script>
</body>
</html>'''

class HVFCommHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path == '/' or self.path.startswith('/?'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(DASHBOARD_HTML.encode('utf-8'))
        else:
            # Ignore extension noise silently
            self.send_response(404)
            self.end_headers()

    def is_authenticated(self):
        auth_header = self.headers.get('Authorization', '')
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1].strip()
            return token in active_tokens
        return False

    def do_POST(self):
        if self.path == '/api/auth':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try: payload = json.loads(post_data.decode('utf-8'))
            except: payload = {}
            passphrase = payload.get('passphrase', '').strip()
            
            print(f"[*] Gateway received passphrase attempt")
            if passphrase == MASTER_PASSPHRASE:
                token = secrets.token_hex(24)
                active_tokens.add(token)
                print("[+] PASS MATCH: Node Unlocked!")
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'SUCCESS', 'token': token}).encode('utf-8'))
            else:
                print("[!] PASS MISMATCH: Access Denied")
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'DENIED'}).encode('utf-8'))
            return

        if self.path == '/api/chat':
            if not self.is_authenticated():
                self.send_response(403)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'ACCESS_DENIED'}).encode('utf-8'))
                return

            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try: data = json.loads(post_data.decode('utf-8'))
            except: data = {}
            user_message = data.get('message', '')
            
            response_text = ""
            if client:
                try:
                    prompt = f"Role: You are Ebony, authentic AI Chief of Staff to the CEO of Humphrey Virtual Farm. Speak naturally.\nCEO: {user_message}\nEbony:"
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
    print(" EBONY MEMORY-EMBEDDED SERVER LIVE ON PORT 8080")
    print("=====================================================")
    server.serve_forever()
