import os
import cv2
import sqlite3
import numpy as np
from datetime import datetime

REPO_DIR = os.path.abspath(r"C:\HVF_Repos\hvf-media-matrix-private")
DB_PATH = os.path.join(REPO_DIR, "hvf_memory_vault.db")
OUTPUT_DIR = os.path.join(REPO_DIR, "analyzed_frames")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def analyze_drone_video(video_path: str, mission_name: str = "MISSION-AIR-ALPHA", zone_id: str = "ZONE-1-NORTH", frame_interval: int = 30):
    """
    Extracts frames from DJI Air 3S footage, calculates Green Leaf Index (GLI),
    and saves telemetry diagnostics to hvf_memory_vault.db.
    """
    if not os.path.exists(video_path):
        print(f"❌ Error: Video file not found at {video_path}")
        return

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"🎬 Processing video: {os.path.basename(video_path)} ({total_frames} total frames @ {fps:.1f} FPS)")

    frame_idx = 0
    analyzed_count = 0
    scores = []

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % frame_interval == 0:
            # Normalize BGR channels
            b = frame[:, :, 0].astype(float)
            g = frame[:, :, 1].astype(float)
            r = frame[:, :, 2].astype(float)

            # GLI Formula: (2G - R - B) / (2G + R + B + epsilon)
            numerator = (2.0 * g) - r - b
            denominator = (2.0 * g) + r + b
            denominator[denominator == 0] = 0.001
            gli_map = numerator / denominator

            avg_gli = float(np.mean(gli_map))
            scores.append(avg_gli)

            # Save diagnostic keyframe
            out_name = f"{mission_name}_f{frame_idx}.jpg"
            out_path = os.path.join(OUTPUT_DIR, out_name)
            cv2.imwrite(out_path, frame)

            cur.execute("""
                INSERT INTO drone_survey_images (mission_name, zone_id, file_path, latitude, longitude, altitude_m, vegetation_index)
                VALUES (?, ?, ?, 35.4712, -98.3541, 45.0, ?)
            """, (mission_name, zone_id, out_path, round(avg_gli, 4)))

            analyzed_count += 1

        frame_idx += 1

    conn.commit()
    conn.close()
    cap.release()

    overall_mean = np.mean(scores) if scores else 0.0
    print("--------------------------------------------------")
    print(f"✅ Analysis Complete: {analyzed_count} frames analyzed.")
    print(f"🌿 Average Green Leaf Index (GLI): {overall_mean:.4f}")
    if overall_mean > 0.25:
        print("🌱 Canopy Verdict: VIGOROUS & HEALTHY")
    elif overall_mean > 0.10:
        print("⚠️ Canopy Verdict: MODERATE STRESS / THIN COVERAGE")
    else:
        print("🚨 Canopy Verdict: SEVERE MOISTURE DEFICIT / LOW VEGETATION")
    print("--------------------------------------------------")

if __name__ == "__main__":
    print("[HVF VISION ENGINE]: Standalone computer vision analyzer initialized.")