import os
import sys
import time
import threading
import socketserver
from http.server import HTTPServer, BaseHTTPRequestHandler
import cv2

PORT = 8502

class SovereignArducamBuffer:
    def __init__(self):
        self.frame = None
        self.lock = threading.Lock()
        self.running = True

    def capture_loop(self):
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)

        while self.running:
            ret, raw_frame = cap.read()
            if not ret or raw_frame is None:
                time.sleep(0.01)
                continue

            ts_str = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
            cv2.putText(raw_frame, f"HVF-C2 // ARDUCAM-1080P-HDR // {ts_str}", 
                        (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 255, 128), 2, cv2.LINE_AA)

            ret_enc, buffer = cv2.imencode(".jpg", raw_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            if ret_enc:
                with self.lock:
                    self.frame = buffer.tobytes()

            time.sleep(0.02)

        cap.release()

buffer_manager = SovereignArducamBuffer()

class StreamingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/video_feed":
            self.send_response(200)
            self.send_header("Age", "0")
            self.send_header("Cache-Control", "no-cache, private")
            self.send_header("Pragma", "no-cache")
            self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=FRAME")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.end_headers()
            try:
                while True:
                    with buffer_manager.lock:
                        if buffer_manager.frame is None:
                            time.sleep(0.01)
                            continue
                        current_bytes = buffer_manager.frame

                    self.wfile.write(b"--FRAME\r\n")
                    self.send_header("Content-Type", "image/jpeg")
                    self.send_header("Content-Length", str(len(current_bytes)))
                    self.end_headers()
                    self.wfile.write(current_bytes)
                    self.wfile.write(b"\r\n")
                    time.sleep(0.033)
            except Exception:
                pass
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def log_message(self, format, *args):
        return

class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

if __name__ == "__main__":
    cap_thread = threading.Thread(target=buffer_manager.capture_loop, daemon=True)
    cap_thread.start()
    time.sleep(1.0)
    server_address = ("0.0.0.0", PORT)
    httpd = ThreadedHTTPServer(server_address, StreamingHandler)
    print(f"[ONLINE] Sovereign Arducam daemon broadcasting on 0.0.0.0:{PORT}")
    httpd.serve_forever()
