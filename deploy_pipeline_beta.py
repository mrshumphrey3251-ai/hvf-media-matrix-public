import os

print("[*] Forging Sovereign Intercom Broker...")

broker_code = """import ssl
from aiohttp import web

websockets = set()

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    websockets.add(ws)
    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                # Instantly bounce cryptographic keys to all other connected peers
                for peer in websockets:
                    if peer != ws:
                        await peer.send_str(msg.data)
    except Exception:
        pass
    finally:
        websockets.discard(ws)
    return ws

async def intercom_page(request):
    html = '''<!DOCTYPE html>
    <html>
    <head>
        <title>Sovereign Intercom</title>
        <style>
            body { background: #000; color: #00ff00; font-family: monospace; margin: 0; padding: 10px; text-align: center; }
            .video-container { display: flex; justify-content: center; gap: 10px; margin-top: 10px; }
            video { width: 45%; max-width: 400px; border: 2px solid #00ff00; background: #111; border-radius: 8px; }
            button { background: #00ff00; color: #000; border: none; padding: 12px 24px; cursor: pointer; font-weight: bold; font-size: 14px; border-radius: 4px; transition: 0.3s; }
            button:hover { background: #fff; }
        </style>
    </head>
    <body>
        <button id="callBtn" onclick="startCall()">[ INITIATE SECURE COMM LINK ]</button>
        <div id="status" style="margin-top: 10px; font-size: 12px; color: #aaa;">AWAITING SIGNAL</div>
        <div class="video-container">
            <video id="localVideo" autoplay muted playsinline></video>
            <video id="remoteVideo" autoplay playsinline></video>
        </div>
        <script>
            const localVideo = document.getElementById('localVideo');
            const remoteVideo = document.getElementById('remoteVideo');
            const statusDiv = document.getElementById('status');
            let pc;
            let localStream;
            
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = protocol + '//' + window.location.host + '/ws';
            const ws = new WebSocket(wsUrl);

            ws.onopen = () => { statusDiv.innerText = "SIGNALING BROKER SECURED"; };
            ws.onclose = () => { statusDiv.innerText = "BROKER DISCONNECTED"; };

            const config = { iceServers: [{ urls: 'stun:stun.l.google.com:19302' }] };

            ws.onmessage = async (event) => {
                if (!pc) await initPeerConnection();
                const message = JSON.parse(event.data);
                if (message.sdp) {
                    await pc.setRemoteDescription(new RTCSessionDescription(message.sdp));
                    if (message.sdp.type === 'offer') {
                        const answer = await pc.createAnswer();
                        await pc.setLocalDescription(answer);
                        ws.send(JSON.stringify({ sdp: pc.localDescription }));
                        statusDiv.innerText = "SECURE LINK ESTABLISHED (RECEIVER)";
                    }
                } else if (message.candidate) {
                    await pc.addIceCandidate(new RTCIceCandidate(message.candidate));
                }
            };

            async function initPeerConnection() {
                pc = new RTCPeerConnection(config);
                pc.onicecandidate = (event) => {
                    if (event.candidate) ws.send(JSON.stringify({ candidate: event.candidate }));
                };
                pc.ontrack = (event) => {
                    remoteVideo.srcObject = event.streams[0];
                    statusDiv.innerText = "SECURE OPTICS INCOMING";
                };
                try {
                    localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
                    localVideo.srcObject = localStream;
                    localStream.getTracks().forEach(track => pc.addTrack(track, localStream));
                } catch (e) {
                    statusDiv.innerText = "HARDWARE ACCESS DENIED (Locked by OS or Browser)";
                }
            }

            async function startCall() {
                document.getElementById('callBtn').innerText = "[ NEGOTIATING LINK... ]";
                if (!pc) await initPeerConnection();
                const offer = await pc.createOffer();
                await pc.setLocalDescription(offer);
                ws.send(JSON.stringify({ sdp: pc.localDescription }));
                statusDiv.innerText = "SECURE LINK ESTABLISHED (CALLER)";
                document.getElementById('callBtn').innerText = "[ COMM LINK ACTIVE ]";
            }
        </script>
    </body>
    </html>'''
    return web.Response(text=html, content_type='text/html')

app = web.Application()
app.router.add_get('/intercom', intercom_page)
app.router.add_get('/ws', websocket_handler)

if __name__ == '__main__':
    print("[*] SOVEREIGN INTERCOM BROKER IGNITED ON PORT 8890")
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain("matrix_cert.pem", "matrix_key.pem")
    web.run_app(app, host='0.0.0.0', port=8890, ssl_context=ssl_context)
"""
with open("hvf_intercom_broker.py", "w", encoding="utf-8") as f:
    f.write(broker_code)
print("[SUCCESS] hvf_intercom_broker.py engineered.")

print("[*] Injecting Pipeline Beta into Comms Deck...")
file_path = "ebony_console_GREEN.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

marker = 'st.markdown("### 💬 Encrypted P2P Dispatch")'
if marker in content and "🎥 Sovereign P2P Video Link" not in content:
    injection = """st.markdown("### 🎥 Sovereign P2P Video Link")
    st.markdown(
        '<iframe src="https://100.87.162.117:8890/intercom" width="100%" height="450" style="border:1px solid #00ff00; border-radius: 8px;" allow="camera; microphone; autoplay; fullscreen"></iframe>',
        unsafe_allow_html=True
    )
    st.markdown("---")
    
    """ + marker
    content = content.replace(marker, injection)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[SUCCESS] Pipeline Beta surgically injected into Sovereign Comms Deck.")
else:
    print("[INFO] Target locked: Pipeline Beta is already present.")