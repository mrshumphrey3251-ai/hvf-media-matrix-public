import os
import json
import secrets
import traceback
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
    except Exception as e:
        print(f"[!] Neural Client Init Error: {e}")

APP_HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HVF Ebony - Sovereign Dashboard</title>
    <style>
        body { margin: 0; background: #0a0e17; color: #f9fafb; font-family: sans-serif; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        #auth-modal { position: fixed; inset: 0; background: #06090f; display: flex; align-items: center; justify-content: center; z-index: 99999; }
        .auth-card { background: #111827; border: 1px solid #1f2937; padding: 36px; border-radius: 12px; width: 400px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.9); }
        h2 { color: #10b981; margin-top: 0; }
        p { color: #9ca3af; font-size: 13px; margin-bottom: 24px; line-height: 1.4; }
        .stealth-input { -webkit-text-security: disc; width: 100%; padding: 14px; border-radius: 6px; border: 1px solid #1f2937; background: #040711; color: #fff; font-size: 15px; margin-bottom: 16px; text-align: center; outline: none; }
        .stealth-input:focus { border-color: #10b981; }
        .auth-btn { width: 100%; padding: 14px; border-radius: 6px; background: #10b981; border: none; color: #000; font-weight: bold; font-size: 15px; cursor: pointer; }
        #main-container { display: none; flex: 1; flex-direction: column; height: 100vh; }
        header { padding: 16px 24px; background: #111827; border-bottom: 1px solid #1f2937; display: flex; justify-content: space-between; align-items: center; }
        .badge { background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 4px 10px; border-radius: 20px; font-size: 12px; border: 1px solid #10b981; }
        #chat-window { flex: 1; padding: 24px; overflow-y: auto; display: flex; flex-direction: column; gap: 16px; }
        .message { max-width: 75%; padding: 14px 18px; border-radius: 8px; line-height: 1.5; font-size: 14px; white-space: pre-wrap; }
        .msg-ceo { align-self: flex-end; background: #1e293b; border-left: 3px solid #3b82f6; }
        .msg-ebony { align-self: flex-start; background: #111827; border-left: 3px solid #10b981; }
        #input-panel { padding: 16px 24px; background: #111827; border-top: 1px solid #1f2937; display: flex; gap: 12px; }
        .chat-input { flex: 1; padding: 12px 16px; border-radius: 6px; background: #040711; border: 1px solid #1f2937; color: #fff; font-size: 14px; outline: none; }
        .chat-btn { padding: 12px 24px; border-radius: 6px; background: #10b981; border: none; color: #000; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div id="auth-modal">
        <div class="auth-card">
            <h2>HVF Security Gateway</h2>
            <p>Stealth Authentication Active.<br>Enter Passphrase to unlock Ebony.</p>
            <input type="text" id="passphrase-input" class="stealth-input" placeholder="Enter passphrase..." autocomplete="off" spellcheck="false" />
            <button class="auth-btn" id="unlock-btn" onclick="executeUnlock()">Unlock Node</button>
            <div id="auth-err" style="color: #ef4444; font-size: 13px; margin-top: 14px; min-height: 18px; font-weight: bold;"></div>
        </div>
    </div>
    <div id="main-container">
        <header>
            <div><strong style="font-size: 16px;">Humphrey Virtual Farm</strong> | Ebony Chief of Staff</div>
            <div class="badge">OPSEC Gated - Sovereign Node Active</div>
        </header>
        <div id="chat-window">
            <div class="message msg-ebony">Sovereign Node Authenticated. Knowledge Vault memory ready. Standing by.</div>
        </div>
        <div id="input-panel">
            <input type="text" id="user-msg" class="chat-input" placeholder="Transmit directive to Ebony..." onkeydown="if(event.key==='Enter') sendDirective()" />
            <button class="chat-btn" onclick="sendDirective()">Transmit</button>
        </div>
    </div>
    <script>
        let sessionToken = sessionStorage.getItem("hvf_stealth_token");
        const passInput = document.getElementById("passphrase-input");
        const errDiv = document.getElementById("auth-err");

        if (sessionToken) { unlockDashboard(); }
        else { passInput.focus(); }

        passInput.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); executeUnlock(); } });

        function unlockDashboard() {
            document.getElementById("auth-modal").style.display = "none";
            document.getElementById("main-container").style.display = "flex";
            document.getElementById("user-msg").focus();
        }

        async function executeUnlock() {
            const pass = passInput.value.trim();
            if (!pass) return;
            errDiv.innerText = "Verifying...";
            
            try {
                const res = await fetch("/api/auth", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ passphrase: pass })
                });
                
                const text = await res.text();
                let data = {};
                try { data = JSON.parse(text); } catch(e) {}
                
                if (res.ok && data.token) {
                    sessionToken = data.token;
                    sessionStorage.setItem("hvf_stealth_token", sessionToken);
                    unlockDashboard();
                } else {
                    errDiv.innerText = "Access Denied: Invalid Passphrase";
                    passInput.value = "";
                    passInput.focus();
                }
            } catch (err) {
                errDiv.innerText = "Gateway Error: Server unreachable.";
            }
        }

        async function sendDirective() {
            const input = document.getElementById("user-msg");
            const msg = input.value.trim();
            if (!msg || !sessionToken) return;
            
            const chat = document.getElementById("chat-window");
            chat.innerHTML += <div class="message msg-ceo"> + msg + </div>;
            input.value = "";
            chat.scrollTop = chat.scrollHeight;
            
            try {
                const res = await fetch("/api/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json", "Authorization": "Bearer " + sessionToken },
                    body: JSON.stringify({ message: msg })
                });
                
                const text = await res.text();
                try {
                    const data = JSON.parse(text);
                    chat.innerHTML += <div class="message msg-ebony"> + (data.reply || data.error || "No response generated.") + </div>;
                } catch(e) {
                    chat.innerHTML += <div class="message msg-ebony" style="color:#ef4444;">System Error: Received non-JSON output.</div>;
                }
                chat.scrollTop = chat.scrollHeight;
            } catch (err) {
                chat.innerHTML += <div class="message msg-ebony" style="color:#ef4444;">Network Error:  + err.message + </div>;
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
    def send_json_error(self, code, msg):
        try:
            self.send_response(code)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': msg}).encode('utf-8'))
        except: pass

    def do_GET(self):
        try:
            if self.path == '/' or self.path.startswith('/?'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
                self.end_headers()
                self.wfile.write(APP_HTML.encode('utf-8'))
            else:
                self.send_json_error(404, 'Not Found')
        except: pass

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try: payload = json.loads(post_data.decode('utf-8'))
            except: payload = {}

            if self.path == '/api/auth':
                passphrase = payload.get('passphrase', '').strip()
                print(f"[*] Gateway Auth Attempt Logged")
                
                if passphrase == MASTER_PASSPHRASE:
                    token = secrets.token_hex(24)
                    active_tokens.add(token)
                    print("[+] MATCH: Node Unlocked.")
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'SUCCESS', 'token': token}).encode('utf-8'))
                else:
                    print("[!] MISMATCH: Access Denied.")
                    self.send_json_error(401, 'Invalid Passphrase')
                return

            if self.path == '/api/chat':
                auth_header = self.headers.get('Authorization', '')
                if not auth_header.startswith("Bearer ") or auth_header.split(" ", 1)[1].strip() not in active_tokens:
                    self.send_json_error(403, 'ACCESS DENIED')
                    return

                user_message = payload.get('message', '')
                response_text = ""
                
                if client:
                    try:
                        vault_dict = load_knowledge_vault()
                        vault_formatted = "\n".join([f"DOC: {k}\n{v}" for k, v in vault_dict.items()])
                        prompt = f"Knowledge Base:\n{vault_formatted}\n\nRole: You are Ebony, authentic AI Chief of Staff. Speak naturally.\nCEO: {user_message}\nEbony:"
                        res = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
                        response_text = res.text.strip()
                    except Exception as mod_err:
                        response_text = f"Local Node Active. (API Warning: {str(mod_err)})"
                else:
                    response_text = "Local Node Active. Knowledge Vault standing by."
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'reply': response_text}).encode('utf-8'))
                return

            self.send_json_error(404, 'Endpoint Not Found')

        except Exception as e:
            print(f"[!] INTERNAL ERROR: {str(e)}")
            self.send_json_error(500, f'Backend Exception: {str(e)}')

if __name__ == "__main__":
    try:
        server = ThreadingHTTPServer(('127.0.0.1', 8085), HVFCommHandler)
        print("=====================================================")
        print(" EBONY STEALTH SERVER LIVE ON PORT 8085")
        print("=====================================================")
        server.serve_forever()
    except Exception as e:
        print("\n[!] CRITICAL ERROR: SERVER FAILED TO START")
        print(f"Details: {e}")
        traceback.print_exc()
