"""Day 3 demo: simple motion detection using background subtraction."""
import time
import cv2

cap = cv2.VideoCapture(1)
if not cap.isOpened():
    raise RuntimeError("Could not open webcam")

bg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)
last_event_time = 0
cooldown_sec = 3

while True:
    ok, frame = cap.read()
    if not ok:
        break

    frame = cv2.resize(frame, (640, 480))
    fg = bg.apply(frame)
    _, mask = cv2.threshold(fg, 250, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion = False
    for c in contours:
        area = cv2.contourArea(c)
        #1500 px is for noise filtering, you can adjust it based on your environment and needs
        if area > 1500:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            motion = True

    if motion and time.time() - last_event_time > cooldown_sec:
        print({"event": "motion_detected", "camera_id": "webcam01", "timestamp": time.time()})
        last_event_time = time.time()

    cv2.imshow("Motion Detection", frame)
    cv2.imshow("fg", fg)
    cv2.imshow("Motion Mask", mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
