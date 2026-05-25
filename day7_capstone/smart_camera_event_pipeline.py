"""Day 7 capstone: YOLO detection + event posting to FastAPI.

Start the API first:
cd code/day6_iot_edge
uvicorn fastapi_event_server:app --reload --host 0.0.0.0 --port 8000
"""
import time
import cv2
import requests
from ultralytics import YOLO

API_URL = "http://localhost:8000/events"
CAMERA_ID = "cam01"
CONF_THRESHOLD = 0.55
EVENT_COOLDOWN_SEC = 5
INTEREST_LABELS = {"person", "car", "truck", "bicycle", "motorcycle"}

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Could not open webcam")

last_event_at = {}

while True:
    ok, frame = cap.read()
    if not ok:
        break

    results = model(frame, conf=CONF_THRESHOLD, verbose=False)
    annotated = results[0].plot()
    names = results[0].names

    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        label = names[cls_id]
        conf = float(box.conf[0])
        if label not in INTEREST_LABELS:
            continue

        now = time.time()
        if now - last_event_at.get(label, 0) < EVENT_COOLDOWN_SEC:
            continue

        event = {
            "camera_id": CAMERA_ID,
            "event_type": "object_detected",
            "label": label,
            "confidence": conf,
            "timestamp": now,
        }
        try:
            r = requests.post(API_URL, json=event, timeout=2)
            print("Event sent:", r.json())
            last_event_at[label] = now
        except requests.RequestException as exc:
            print("Event API error:", exc)

    cv2.imshow("Smart Camera Event Pipeline", annotated)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
