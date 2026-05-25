# AI Vision + Edge IoT Workshop Code

This code pack supports the 15-hour workshop on Image Processing, Facial Image Processing, IoT, Raspberry Pi, ESP32-CAM and Jetson-based object classification.

## Quick setup

```bash
cd code
python3 -m venv .venv
#windows
python -m venv venv
#for linux and mac
source .venv/bin/activate
#windows 
#cmd
venv\Scripts\activate.bat
#poweshell
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
python create_sample_assets.py
```

## Suggested run order

1. `day1_image_basics/image_read_pixels.py`
2. `day1_image_basics/webcam_capture.py`
3. `day2_processing/filters_edges_contours.py`
4. `day2_processing/object_counting.py`
5. `day3_motion/motion_detection.py`
6. `day4_face/face_detection_haar.py`
7. `day4_face/mediapipe_face_mesh.py`
8. `day5_yolo/yolo_webcam_detection.py`
9. `day6_iot_edge/mqtt_publish_event.py`
10. `day6_iot_edge/fastapi_event_server.py`
11. `day6_iot_edge/streamlit_dashboard.py`
12. `day7_capstone/smart_camera_event_pipeline.py`

## Notes

- Press `q` to quit OpenCV webcam windows.
- If the webcam is not available, use the generated sample images from `assets/`.
- YOLO downloads weights on first run if internet is available. Keep the model file ready before class if internet is unreliable.
- ESP32-CAM code is a reference sketch. Test board/camera pin configuration before class.
