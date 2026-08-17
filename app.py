from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

# Load environment variables (security hashes, future API keys)
load_dotenv()

# Initialize the Sovereign Server
app = Flask(__name__)

# Route 1: Serve the Dual-Pane Dashboard
@app.route('/')
def home():
    return render_template('index.html')

# Route 2: The Ebony Communications Matrix
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    # Core logic placeholder: Currently set to acknowledge receipt of directive
    # Future integration: This block will route to the AI inference engine
    reply = f"Directive confirmed: '{user_message}'. Awaiting full cognitive integration."
    
    return jsonify({"reply": reply})

if __name__ == '__main__':
    # Ignite the server on local port 5000
    app.run(host='127.0.0.1', port=5000, debug=False)
