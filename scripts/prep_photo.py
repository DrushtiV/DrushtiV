"""
STEP A — Get the photo ready.

A normal, flatly-lit selfie turns into a dark, unreadable blob if you
convert it to ASCII art directly. This script fixes that in 3 moves:

  1. Cut out the background (so only you are left).
  2. Put you on a plain white background (so the background becomes
     blank space in the ASCII art, not noise).
  3. Boost local contrast so your face has real light & shadow.

Usage:
    python scripts/prep_photo.py my-photo.jpg
"""
import sys
import cv2
from PIL import Image
from rembg import remove

OUTPUT_PATH = "source-prepped.png"


def prep_photo(input_path, output_path=OUTPUT_PATH):
    # 1. Remove the background
    with open(input_path, "rb") as f:
        input_bytes = f.read()
    output_bytes = remove(input_bytes)

    with open("_no_bg.png", "wb") as f:
        f.write(output_bytes)

    # 2. Put the cutout onto a pure white background
    img = Image.open("_no_bg.png").convert("RGBA")
    white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, img).convert("L")
    composited.save("_white_bg.png")

    # 3. Boost local contrast (CLAHE) so the face has real depth
    gray = cv2.imread("_white_bg.png", cv2.IMREAD_GRAYSCALE)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    cv2.imwrite(output_path, enhanced)
    print(f"✅ Prepped photo saved -> {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <your-photo.jpg>")
        sys.exit(1)
    prep_photo(sys.argv[1])
