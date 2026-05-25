"""Day 2 demo: filters, edge detection and contour visualization."""
from pathlib import Path
import cv2
import numpy as np

BASE = Path(__file__).resolve().parents[1]
img = cv2.imread(str(BASE / "assets" / "objects.png"))
if img is None:
    raise FileNotFoundError("Run create_sample_assets.py first.")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blur, 50, 150)

kernel = np.ones((5, 5), np.uint8)
closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

cv2.imshow("Original", img)
cv2.imshow("Gray", gray)
cv2.imshow("Gaussian Blur", blur)
cv2.imshow("Canny Edges", edges)
cv2.imshow("Morphological Close", closed)
cv2.waitKey(0)
cv2.destroyAllWindows()
