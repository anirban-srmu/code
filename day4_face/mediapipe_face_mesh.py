"""
Day 4 Demo:
Facial landmark detection using the newer MediaPipe Tasks API.

This replaces the older:
mp.solutions.face_mesh.FaceMesh()

New API:
mediapipe.tasks.vision.FaceLandmarker
"""

import os
import time
import urllib.request

import cv2
import mediapipe as mp


# ---------------------------------------------------------
# Step 1: Download the Face Landmarker model if not present
# ---------------------------------------------------------

MODEL_PATH = "face_landmarker.task"

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "face_landmarker/face_landmarker/float16/latest/"
    "face_landmarker.task"
)

if not os.path.exists(MODEL_PATH):
    print("Downloading Face Landmarker model...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("Model downloaded.")


# ---------------------------------------------------------
# Step 2: Create MediaPipe Face Landmarker task
# ---------------------------------------------------------

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_faces=1,
    min_face_detection_confidence=0.5,
    min_face_presence_confidence=0.5,
    min_tracking_confidence=0.5,
)


# ---------------------------------------------------------
# Step 3: Open webcam
# ---------------------------------------------------------

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    raise RuntimeError("Could not open webcam")


# ---------------------------------------------------------
# Step 4: Run face landmark detection
# ---------------------------------------------------------

with FaceLandmarker.create_from_options(options) as landmarker:

    while True:
        ok, frame = cap.read()

        if not ok:
            break

        # Flip frame horizontally for mirror-like webcam display
        frame = cv2.flip(frame, 1)

        # OpenCV gives BGR image, MediaPipe needs RGB image
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert NumPy RGB image to MediaPipe Image object
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Timestamp is required in VIDEO mode
        timestamp_ms = int(time.time() * 1000)

        # Detect facial landmarks
        result = landmarker.detect_for_video(mp_image, timestamp_ms)

        # Draw landmarks manually
        if result.face_landmarks:
            height, width, _ = frame.shape

            for face_landmarks in result.face_landmarks:
                for landmark in face_landmarks:
                    x = int(landmark.x * width)
                    y = int(landmark.y * height)

                    cv2.circle(
                        frame,
                        (x, y),
                        1,
                        (0, 255, 255),
                        -1
                    )

        cv2.imshow("MediaPipe New Face Landmarker", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


# ---------------------------------------------------------
# Step 5: Cleanup
# ---------------------------------------------------------

cap.release()
cv2.destroyAllWindows()