"""Read ESP32-CAM MJPEG stream from Python/OpenCV.
Update STREAM_URL with the IP printed by ESP32 serial monitor.
"""
import cv2

STREAM_URL = "http://YOUR_ESP32_IP/stream"
cap = cv2.VideoCapture(STREAM_URL)
if not cap.isOpened():
    raise RuntimeError(f"Could not open stream: {STREAM_URL}")

while True:
    ok, frame = cap.read()
    if not ok:
        print("Frame read failed")
        break
    cv2.imshow("ESP32-CAM Stream", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
