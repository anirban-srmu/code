"""Create simple offline assets for the workshop demos."""
from pathlib import Path
import cv2
import numpy as np

OUT = Path(__file__).resolve().parent / "assets"
OUT.mkdir(exist_ok=True)

# sample shapes for contour counting
img = np.zeros((480, 720, 3), dtype=np.uint8)
img[:] = (245, 245, 245)
cv2.circle(img, (120, 140), 55, (40, 120, 220), -1)
cv2.rectangle(img, (250, 80), (370, 200), (40, 180, 80), -1)
cv2.circle(img, (540, 140), 60, (200, 90, 80), -1)
cv2.rectangle(img, (110, 300), (250, 410), (120, 50, 200), -1)
cv2.circle(img, (440, 350), 70, (20, 150, 150), -1)
cv2.putText(img, "Sample objects", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (20,20,20), 2)
cv2.imwrite(str(OUT / "objects.png"), img)

# sample face placeholder (no actual face, useful to test file read)
img2 = np.zeros((480, 640, 3), dtype=np.uint8)
img2[:] = (230, 235, 240)
cv2.putText(img2, "Use webcam for face demo", (65, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (30,30,30), 2)
cv2.imwrite(str(OUT / "face_placeholder.png"), img2)

print(f"Sample assets created in {OUT}")
