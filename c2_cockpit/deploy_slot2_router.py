import os

router_code = """import asyncio
import cv2
import time
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaRelay
from av import VideoFrame

class PhysicalCameraTrack(VideoStreamTrack):
    kind = "video"
    def __init__(self):
        super().__init__()
        # CEO OVERRIDE: FORCE PHYSICAL SLOT 2 with DSHOW
        self.cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)

    async def recv(self):
        pts, time_base = await self.next_timestamp()
        ret, frame = self.cap.read()
        
        if not ret:
            # If camera 2 drops, render a black frame so the pipeline doesn't crash
            import numpy as np
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "SLOT 2: WAITING FOR PHYSICAL SIGNAL", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
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
    <head><title>HVF SCADA FEED</title></head>
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
    print("[*] PHYSICAL PIPELINE ALPHA IGNITED ON SLOT 2: 0.0.0.0:8889")
    web.run_app(app, host="0.0.0.0", port=8889)
"""

with open("hvf_media_router.py", "w", encoding="utf-8") as f:
    f.write(router_code)
print("[SUCCESS] Physical hardware mapped to Slot 2 (CAP_DSHOW). Router ready.")