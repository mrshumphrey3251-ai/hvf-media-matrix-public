import ssl
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
        <button id="switchBtn" onclick="switchCamera()" style="background:#ff9900; color:#000; padding:15px; border:none; font-weight:bold; cursor:pointer; margin-left:10px;">[ SWITCH LENS ]</button>
        <div id="status" style="margin-top: 10px; font-size: 12px; color: #aaa;">AWAITING SIGNAL</div>
        <div class="video-container">
            <video id="localVideo" autoplay muted playsinline></video>
            <video id="remoteVideo" autoplay playsinline></video>
        </div>
        <script>
        const ws = new WebSocket('wss://' + location.host);
        let peerConnection;
        let localStream;
        let currentFacingMode = 'user';

        ws.onmessage = async (message) => {
            const data = JSON.parse(message.data);
            if (data.offer) {
                document.getElementById('status').innerText = 'STATUS: SECURE LINK ESTABLISHED (RECEIVER)';
                await setupPeerConnection();
                await peerConnection.setRemoteDescription(new RTCSessionDescription(data.offer));
                const answer = await peerConnection.createAnswer();
                await peerConnection.setLocalDescription(answer);
                ws.send(JSON.stringify({ answer: answer }));
            } else if (data.answer) {
                await peerConnection.setRemoteDescription(new RTCSessionDescription(data.answer));
            } else if (data.iceCandidate) {
                await peerConnection.addIceCandidate(new RTCIceCandidate(data.iceCandidate));
            }
        };

        async function initiateCall() {
            if (peerConnection) return; // Prevent double-clicks from mirroring video
            document.getElementById('status').innerText = 'STATUS: ACQUIRING HARDWARE...';
            
            try {
                // The exact 3:33 state: ask for both video and audio to keep Android happy
                localStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: currentFacingMode }, audio: true });
            } catch (err) {
                console.warn("[HVF] Audio missing (Desktop). Autonomous fallback engaged.", err);
                try {
                    // Fallback for the desktop tower
                    localStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: currentFacingMode }, audio: false });
                } catch (err2) {
                    console.error("[HVF] Hardware lock absolute.", err2);
                    document.getElementById('status').innerText = 'STATUS: HARDWARE ACCESS DENIED';
                    return;
                }
            }
            
            document.getElementById('localVideo').srcObject = localStream;
            document.getElementById('status').innerText = 'STATUS: SECURE LINK ESTABLISHED (CALLER)';
            
            await setupPeerConnection();
            const offer = await peerConnection.createOffer();
            await peerConnection.setLocalDescription(offer);
            ws.send(JSON.stringify({ offer: offer }));
        }

        async function switchCamera() {
            if (!localStream) {
                alert("[HVF] Matrix offline. Initiate secure link first.");
                return;
            }
            currentFacingMode = (currentFacingMode === 'user') ? 'environment' : 'user';
            try {
                let newStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: currentFacingMode }, audio: false });
                let newTrack = newStream.getVideoTracks()[0];
                let sender = peerConnection.getSenders().find(s => s.track.kind === 'video');
                if (sender) sender.replaceTrack(newTrack);
                
                localStream.removeTrack(localStream.getVideoTracks()[0]);
                localStream.addTrack(newTrack);
                document.getElementById('localVideo').srcObject = localStream;
            } catch (err) {
                console.error("[HVF] Lens toggle failed", err);
            }
        }

        async function setupPeerConnection() {
            peerConnection = new RTCPeerConnection({ iceServers: [{ urls: 'stun:stun.l.google.com:19302' }] });
            peerConnection.onicecandidate = (event) => {
                if (event.candidate) ws.send(JSON.stringify({ iceCandidate: event.candidate }));
            };
            peerConnection.ontrack = (event) => {
                document.getElementById('remoteVideo').srcObject = event.streams[0];
            };
            if (localStream) {
                localStream.getTracks().forEach(track => peerConnection.addTrack(track, localStream));
            }
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
