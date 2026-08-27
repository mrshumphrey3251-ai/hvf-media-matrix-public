import os
import numpy as np
from PIL import Image

REPO_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
OUT_PATH = os.path.join(REPO_DIR, "test_aerial_crop.jpg")

height, width = 600, 800
img_array = np.zeros((height, width, 3), dtype=np.uint8)

# Simulating healthy corn/alfalfa canopy: Higher Green (G: 170-220), Lower Red (R: 40-70), Lower Blue (B: 30-50)
img_array[:, :, 0] = np.random.randint(40, 75, (height, width), dtype=np.uint8)   # Red
img_array[:, :, 1] = np.random.randint(160, 220, (height, width), dtype=np.uint8) # Green
img_array[:, :, 2] = np.random.randint(30, 60, (height, width), dtype=np.uint8)   # Blue

# Add simulated soil rows
for row in range(0, height, 40):
    img_array[row:row+8, :, 0] = 110 # Soil Red
    img_array[row:row+8, :, 1] = 85  # Soil Green
    img_array[row:row+8, :, 2] = 45  # Soil Blue

img = Image.fromarray(img_array)
img.save(OUT_PATH)
print(f"✅ Created synthetic aerial survey frame: {OUT_PATH}")