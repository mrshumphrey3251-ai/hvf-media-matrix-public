import cv2
import sys

print("[*] Initiating Bare-Metal Hardware Diagnostic...")

# Force hardware connection on Slot 0 using DirectShow
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("[FATAL] Windows OS refuses to release the camera on Slot 0. It is either unplugged, or held hostage by another app.")
    sys.exit()

print("[SUCCESS] Hardware lock acquired. Press 'Q' inside the video window to terminate.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("[FATAL] Camera connected, but dropping frames.")
        break
    
    cv2.putText(frame, "BARE-METAL DIAGNOSTIC ACTIVE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow('HVF HARDWARE DIAGNOSTIC - PRESS Q TO EXIT', frame)
    
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("[*] Diagnostic terminated. Hardware safely released.")