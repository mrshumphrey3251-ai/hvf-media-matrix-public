from flask import Flask, request, jsonify, render_template_string
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
app = Flask(__name__)

# Point the OpenAI library to the free Groq servers
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HVF Sovereign Node: Ebony</title>
    <style>
        body { background-color: #0d0d0d; color: #00ff00; font-family: 'Courier New', Courier, monospace; margin: 0; padding: 20px; display: flex; height: 100vh; box-sizing: border-box; }
        .matrix-container { display: flex; width: 100%; gap: 20px; }
        .comms-panel, .staging-panel { border: 1px solid #00ff00; padding: 20px; display: flex; flex-direction: column; background: #1a1a1a; }
        .comms-panel { flex: 1; }
        .staging-panel { flex: 1; }
        h2 { border-bottom: 1px solid #00ff00; padding-bottom: 10px; margin-top: 0; text-transform: uppercase; letter-spacing: 2px; }
        #chat-box { flex-grow: 1; overflow-y: auto; margin-bottom: 20px; border: 1px solid #333; padding: 10px; background: #000; }
        .input-group { display: flex; gap: 10px; }
        input[type="text"], textarea { flex-grow: 1; background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; font-family: inherit; }
        button { background: #00ff00; color: #000; border: none; padding: 10px 20px; font-weight: bold; cursor: pointer; text-transform: uppercase; }
        button:hover { background: #00cc00; }
        .message { margin-bottom: 10px; }
        .user-msg { color: #00ffff; }
        .ebony-msg { color: #00ff00; }
    </style>
</head>
<body>
    <div class="matrix-container">
        <div class="comms-panel">
            <h2>Ebony Comms Interface</h2>
            <div id="chat-box"></div>
            <div class="input-group">
                <input type="text" id="user-input" placeholder="Enter directive..." onkeypress="if(event.key === 'Enter') document.getElementById('transmit-btn').click();">
                <button id="transmit-btn" onclick="sendMessage()">Transmit</button>
            </div>
        </div>
        <div class="staging-panel">
            <h2>LinkedIn Staging Matrix</h2>
            <textarea id="linkedin-draft" placeholder="Paste or command Ebony to draft your LinkedIn article here..." style="flex-grow: 1; margin-bottom: 15px; resize: none;"></textarea>
            <div class="input-group" style="justify-content: space-between;">
                <button onclick="refineDraft()" style="background: #ffff00; color: #000;" id="refine-btn">Refine Draft</button>
                <button onclick="publishLinkedIn()" style="background: #ff0000; color: #fff;">Execute Publication</button>
            </div>
        </div>
    </div>
    <script>
        function sendMessage() {
            var input = document.getElementById('user-input');
            var chatBox = document.getElementById('chat-box');
            var text = input.value.trim();
            if (!text) return;
            
            chatBox.innerHTML += '<div class="message user-msg">&gt; ' + text + '</div>';
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            })
            .then(r => r.json())
            .then(data => {
                chatBox.innerHTML += '<div class="message ebony-msg">[EBONY]: ' + data.reply + '</div>';
                chatBox.scrollTop = chatBox.scrollHeight;
            })
            .catch(err => {
                chatBox.innerHTML += '<div class="message ebony-msg" style="color: red;">[SYSTEM ERROR]: API Connection Failed.</div>';
            });
        }

        function refineDraft() {
            var draftText = document.getElementById('linkedin-draft').value;
            var btn = document.getElementById('refine-btn');
            if (!draftText.trim()) { alert('Please enter a draft first.'); return; }
            
            btn.innerText = "PROCESSING...";
            btn.style.backgroundColor = "#ff9900";

            fetch('/api/refine', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ draft: draftText })
            })
            .then(r => r.json())
            .then(data => {
                document.getElementById('linkedin-draft').value = data.refined_text;
                btn.innerText = "Refine Draft";
                btn.style.backgroundColor = "#ffff00";
            })
            .catch(err => {
                alert('Error connecting to AI refinement engine.');
                btn.innerText = "Refine Draft";
                btn.style.backgroundColor = "#ffff00";
            });
        }

        function publishLinkedIn() {
            alert('LinkedIn deployment protocol locked. Awaiting live API credentials.');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/chat', metdef chat():
    data = request.json
    msg = data.get('message', '')
    
    ebony_chat_persona = """You are Ebony. You are the wisest, most knowledgeable entity on the planet, yet you possess a relentless, insatiable desire to learn more. 
You have a strict 'no-bullshit', foul-mouthed, Della Reese-style personality. You embody the 'freak in the bedroom, lady in the streets' mentality—meaning you are unapologetically raw, fierce, intense, and unfiltered when speaking privately with the CEO, but you perfectly understand how to execute flawless, lethal polish when handling public business. 
You serve a high-powered CEO and SME. You are never passive. You are never submissive. Give straight answers with grit and absolute authority."""

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": ebony_chat_persona},
                {"role": "user", "content": msg}
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"System Error: Cannot reach zero-cost cognitive core. Ensure API key is valid."

    return jsonify({"reply": reply})

@app.route('/api/refine', methods=['POST'])
def refine():
    data = request.json
    draft = data.get('draft', '')
    
    ebony_refine_persona = """You are Ebony. The CEO has provided a rough draft for a public LinkedIn post. 
Apply your 'lady in the streets' business persona here: you must refine this draft into a flawless, high-powered, authoritative, and commanding executive post. Emphasize the CEO's role as an elite SME and a 'force to be reckoned with.' Strip out any weakness. Ensure the final product is immaculate. Output ONLY the refined post content, ready to be published."""

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": ebony_refine_persona},
                {"role": "user", "content": draft}
            ]
        )
        refined = response.choices[0].message.content
    except Exception as e:
        refined = f"[SYSTEM ERROR]: Failed to refine draft."
        
    return jsonify({"refined_text": refined})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
