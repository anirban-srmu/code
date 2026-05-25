"""Day 1 demo: capture live frames from webcam."""
import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Could not open webcam. Check camera permissions or device index.")

print("Press 's' to save a frame. Press 'q' to quit.")
frame_id = 0
while True:
    ok, frame = cap.read()
    if not ok:
        print("Failed to read frame")
        break

    cv2.putText(frame, "Press s=save, q=quit", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.imshow("Webcam", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        filename = f"captured_frame_{frame_id}.jpg"
        cv2.imwrite(filename, frame)
        print("Saved", filename)
        frame_id += 1
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
