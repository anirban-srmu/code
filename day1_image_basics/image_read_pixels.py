"""Day 1 demo: read an image, inspect shape and pixel values."""
from pathlib import Path
import cv2

BASE = Path(__file__).resolve().parents[1]
image_path = BASE / "assets" / "objects.png"
# image_path = BASE / "day1_image_basics" / "captured_frame_0.jpg"

img = cv2.imread(str(image_path))
# print(img)
if img is None:
    raise FileNotFoundError(f"Image not found: {image_path}. Run create_sample_assets.py first.")

print("Image shape (height, width, channels):", img.shape)
print("Pixel at row=100, col=100 in BGR:", img[100, 100].tolist())

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print("Grayscale shape:", gray.shape)

cv2.imshow("Original", img)
cv2.imshow("Grayscale", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
