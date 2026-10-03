import cv2

print("[*] COMMENCING SOVEREIGN HARDWARE OPTICAL SCAN...")
working_cameras = []

for index in range(5):
    for backend_name, backend_flag in [("DSHOW", cv2.CAP_DSHOW), ("MSMF", cv2.CAP_MSMF)]:
        cap = cv2.VideoCapture(index, backend_flag)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"[+] SUCCESS: Physical Camera secured at SLOT {index} using backend {backend_name}")
                working_cameras.append((index, backend_name))
            cap.release()

if not working_cameras:
    print("[FATAL] All slots failed. The camera is physically disconnected, blocked by Windows Privacy Settings, or completely locked by another hidden application.")
else:
    print(f"[*] SCAN COMPLETE. Active hardware mapped: {working_cameras}")