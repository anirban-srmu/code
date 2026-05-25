"""Day 5 demo: real-time object detection using YOLOv8.

Before class, download `yolov8n.pt` once by running this with internet.
"""
import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Could not open webcam")

while True:
    ok, frame = cap.read()
    if not ok:
        break
    results = model(frame, conf=0.45, verbose=False)
    annotated = results[0].plot()
    cv2.imshow("YOLO Detection", annotated)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
