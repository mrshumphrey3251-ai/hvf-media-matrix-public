import os
import numpy as np
from PIL import Image, ImageDraw

REPO_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
OUT_PATH = os.path.join(REPO_DIR, "drone_field_view.jpg")

# Create high-res 1200x800 simulated aerial crop scan
width, height = 1200, 800
img = Image.new("RGB", (width, height), color=(34, 139, 34))
draw = ImageDraw.Draw(img)

# Draw simulated crop rows (dark green, light green, soil tracks)
for x in range(0, width, 24):
    color = (20, 100, 20) if (x // 24) % 2 == 0 else (45, 160, 45)
    draw.rectangle([x, 0, x + 18, height], fill=color)

# Add access road / tractor line
draw.rectangle([width // 2 - 20, 0, width // 2 + 20, height], fill=(139, 115, 85))

# Add HUD Overlay directly on image
draw.rectangle([20, 20, 360, 80], fill=(5, 7, 9))
draw.text((30, 30), "DJI AIR 3S // AERIAL CANOPY SCAN", fill=(0, 255, 102))
draw.text((30, 50), "ZONE-1-NORTH | ALT: 45.0m | GLI: 0.3842 (HEALTHY)", fill=(255, 255, 255))

img.save(OUT_PATH, quality=95)
print(f"✅ Drone field image created: {OUT_PATH}")