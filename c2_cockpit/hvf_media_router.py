import json, cv2, numpy as np
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from av import VideoFrame

class DroneFlightTrack(VideoStreamTrack):
    kind = "video"
    
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            self.cap = None

    async def recv(self):
        pts, time_base = await self.next_timestamp()
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                video_frame = VideoFrame.from_ndarray(frame, format="bgr24")
                video_frame.pts = pts
                video_frame.time_base = time_base
                return video_frame
        
        # Fallback Swarm Standby Frame
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(img, "HVF SWARM: WAITING FOR SIGNAL", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        video_frame = VideoFrame.from_ndarray(img, format="bgr24")
        video_frame.pts = pts
        video_frame.time_base = time_base
        return video_frame

async def stream_page(request):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head><style>body { margin: 0; background-color: #000; color: #0f0; font-family: monospace; overflow: hidden; }</style></head>
    <body>
        <div style="position: absolute; top: 10px; left: 10px; z-index: 999; background: rgba(0,0,0,0.7); padding: 5px;">
            🔴 LIVE // HVF SCADA SWARM FEED
        </div>
        <video id="video" autoplay playsinline style="width: 100vw; height: 100vh; object-fit: cover;"></video>
        <script>
            var pc = new RTCPeerConnection();
            pc.addEventListener('track', function(evt) {
                document.getElementById('video').srcObject = evt.streams[0];
            });
            pc.addTransceiver('video', {direction: 'recvonly'});
            pc.createOffer().then(function(offer) {
                return pc.setLocalDescription(offer);
            }).then(function() {
                return fetch('/offer', {
                    body: JSON.stringify({ sdp: pc.localDescription.sdp, type: pc.localDescription.type }),
                    headers: {'Content-Type': 'application/json'},
                    method: 'POST'
                });
            }).then(function(response) {
                return response.json();
            }).then(function(answer) {
                return pc.setRemoteDescription(answer);
            });
        </script>
    </body>
    </html>
    """
    return web.Response(content_type='text/html', text=html_content)

async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
    pc = RTCPeerConnection()
    pc.addTrack(DroneFlightTrack())
    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    return web.Response(content_type='application/json', text=json.dumps({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}))

app = web.Application()
app.router.add_get('/live/stream', stream_page)
app.router.add_post('/offer', offer)

if __name__ == '__main__':
    print("[*] SOVEREIGN WEBRTC MEDIA ROUTER IGNITED: 0.0.0.0:8889", flush=True)
    web.run_app(app, port=8889)