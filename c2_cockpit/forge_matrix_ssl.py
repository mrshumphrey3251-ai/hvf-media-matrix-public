import os

# 1. Forge the Sovereign SSL Certificates
print("[*] Forging Sovereign SSL Certificates...")
try:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import hashes
    from cryptography.x509.oid import NameOID
    from cryptography import x509
    import datetime
except ImportError:
    print("[FATAL] Cryptography engine missing. Run 'pip install cryptography'.")
    exit()

key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Project Ebony Sovereign Matrix"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"100.87.162.117")
])
cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(datetime.datetime.utcnow()).not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365)).sign(key, hashes.SHA256())

with open("matrix_key.pem", "wb") as f:
    f.write(key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption()))
with open("matrix_cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))
print("[SUCCESS] matrix_cert.pem and matrix_key.pem locked in the vault.")

# 2. Upgrade the Master Media Router to HTTPS
print("[*] Upgrading SCADA Router to Military-Grade HTTPS...")
router_code = """import asyncio
import cv2
import time
import threading
import numpy as np
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaRelay
from av import VideoFrame
import ssl

class ThreadedCamera:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        self.ret, self.frame = self.cap.read()
        self.running = True
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()

    def update(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.ret = ret
                self.frame = frame

    def read(self):
        return self.ret, self.frame

class PhysicalCameraTrack(VideoStreamTrack):
    kind = "video"
    def __init__(self):
        super().__init__()
        self.camera = ThreadedCamera(0)

    async def recv(self):
        pts, time_base = await self.next_timestamp()
        ret, frame = self.camera.read()
        if not ret or frame is None:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "HARDWARE OFFLINE", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        video_frame = VideoFrame.from_ndarray(frame, format="bgr24")
        video_frame.pts = pts
        video_frame.time_base = time_base
        return video_frame

relay = MediaRelay()
cam_track = PhysicalCameraTrack()

async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
    pc = RTCPeerConnection()
    pc.addTrack(relay.subscribe(cam_track))
    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    return web.json_response({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type})

async def index(request):
    html_content = '''<!DOCTYPE html>
    <html>
    <head><title>HVF SECURE SCADA</title></head>
    <body style="background-color:black; color:green; text-align:center; margin:0; padding:0;">
        <video id="video" autoplay playsinline style="width:100%; height:100%; border:none; object-fit:cover;"></video>
        <script>
            const pc = new RTCPeerConnection();
            pc.addEventListener('track', function(evt) {
                if (evt.track.kind == 'video') { document.getElementById('video').srcObject = evt.streams[0]; }
            });
            pc.addTransceiver('video', {direction: 'recvonly'});
            pc.createOffer().then(offer => pc.setLocalDescription(offer))
            .then(() => fetch('/offer', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({sdp: pc.localDescription.sdp, type: pc.localDescription.type})
            }))
            .then(res => res.json())
            .then(answer => pc.setRemoteDescription(answer));
        </script>
    </body>
    </html>'''
    return web.Response(content_type="text/html", text=html_content)

app = web.Application()
app.router.add_get("/live/stream", index)
app.router.add_post("/offer", offer)

if __name__ == "__main__":
    print("[*] SECURE HTTPS PIPELINE IGNITED: 0.0.0.0:8889")
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain("matrix_cert.pem", "matrix_key.pem")
    web.run_app(app, host="0.0.0.0", port=8889, ssl_context=ssl_context)
"""
with open("hvf_media_router.py", "w", encoding="utf-8") as f:
    f.write(router_code)
print("[SUCCESS] Router secured with HTTPS.")

# 3. Upgrade the Streamlit UI Iframe to HTTPS
print("[*] Upgrading Comms Deck Iframe to HTTPS...")
file_path = "ebony_console_GREEN.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace('http://100.87.162.117:8889/live/stream', 'https://100.87.162.117:8889/live/stream')
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("[SUCCESS] Architecture fully migrated to HTTPS.")