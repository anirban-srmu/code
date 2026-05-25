"""Day 2 mini project: count high-contrast objects using contours."""
from pathlib import Path
import cv2
import numpy as np

BASE = Path(__file__).resolve().parents[1]
img = cv2.imread(str(BASE / "assets" / "objects.png"))
if img is None:
    raise FileNotFoundError("Run create_sample_assets.py first.")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7, 7), 0)
_, mask = cv2.threshold(blur, 230, 255, cv2.THRESH_BINARY_INV)

kernel = np.ones((5, 5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

count = 0
for c in contours:
    area = cv2.contourArea(c)
    if area < 1000:
        continue
    #draw contour and bounding box (blue and green respectively)
    cv2.drawContours(img, [c], -1, (255, 0, 0), 2)
    x, y, w, h = cv2.boundingRect(c)

    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    count += 1

    #center of the shape usig moments (red circle)
    M = cv2.moments(c)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        #draw a red dot at the center of the shape
        cv2.circle(img, (cX, cY), 7, (0, 0, 255), -1)

cv2.putText(img, f"Object count: {count}", (25, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
print("Detected objects:", count)
cv2.imshow("Mask", mask)
cv2.imshow("Counted Objects", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
