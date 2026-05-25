"""Day 3 demo: simple motion detection using background subtraction."""
import time
import datetime
import cv2

#--Initialize webcam (try 0, 1, 2 etc. if you have multiple cameras or if the default doesn't work)
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    raise RuntimeError("Could not open webcam")

bg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)

#Initialize HOG person detector 
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

#state variables for rules
last_event_time = 0
cooldown_sec = 3

motion_start_time = None
is_recording = False

OBJECT_THRESHOLD = 3  # Alert if more than 3 objects are moving


while True:
    ok, frame = cap.read()
    if not ok:
        break

    frame = cv2.resize(frame, (640, 480))
    fg = bg.apply(frame)
    _, mask = cv2.threshold(fg, 250, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #frame specific flags
    current_motion = False
    person_detected = False
    moving_object_count = 0

    for c in contours:
        area = cv2.contourArea(c)
        #1500 px is for noise filtering, you can adjust it based on your environment and needs
        if area > 1500:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            current_motion = True
            moving_object_count += 1
            # Extarct the region of interest (ROI) with slight padding
            pad = 20
            y1, y2 = max(0, y - pad), min(frame.shape[0], y + h + pad)
            x1, x2 = max(0, x - pad), min(frame.shape[1], x + w + pad)
            roi = frame[y1:y2, x1:x2]

            if roi.shape[0] > 0 and roi.shape[1] > 60:  # Check if ROI is valid
                # Detect people in the ROI
                rects, _ = hog.detectMultiScale(roi, winStride=(8, 8), padding=(4, 4), scale=1.05)
                if len(rects) > 0:
                    person_detected = True
                    cv2.putText(frame, "Person Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    current_time =time.time()
    current_hour = datetime.datetime.now().hour
    #Rule 1: person detected after 7 PM
    if person_detected and current_hour >= 19:
        if current_time - last_event_time > cooldown_sec:
            print({"event": "person_detected_after_hours", "camera_id": "webcam01", "timestamp": current_time})
            last_event_time = current_time

    #rule 2: motion continues for more than 5 seconds
    if current_motion:
        if motion_start_time is None:
            motion_start_time = current_time
        elif current_time - motion_start_time > 5.0 and not is_recording:
            print({"event": "start recoding", "camera_id": "webcam01", "timestamp": current_time})
            is_recording = True
    else:
        if is_recording:
            print({"event": "stop recording", "camera_id": "webcam01", "timestamp": current_time})
            is_recording = False
        motion_start_time = None

    #rule 3: more than 3 moving objects detected
    if moving_object_count > OBJECT_THRESHOLD:
        if current_time - last_event_time > cooldown_sec:
            print({"event": "multiple_objects_detected", "camera_id": "webcam01", "timestamp": current_time, "count": moving_object_count})
            last_event_time = current_time

    cv2.imshow("Start Motion Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
