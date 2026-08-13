#!/bin/bash
echo "[HVF SYSTEM] Initializing Cinematic Animation Matrix..."

# Process Clip 1
if [ -f "VIDEO_01_RAW_CLIPS/img_01_swarm.jpg" ]; then
    echo "Animating Clip 1: The Swarm..."
    ffmpeg -y -loop 1 -i VIDEO_01_RAW_CLIPS/img_01_swarm.jpg -vf "zoompan=z='min(zoom+0.0015,1.15)':d=120:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)',framerate=24" -c:v libx264 -t 5 -s 1920x1080 -pix_fmt yuv420p VIDEO_01_RAW_CLIPS/clip_01_swarm.mp4 2>/dev/null
fi

# Process Clip 2
if [ -f "VIDEO_01_RAW_CLIPS/img_02_tactical.jpg" ]; then
    echo "Animating Clip 2: The Warzone..."
    ffmpeg -y -loop 1 -i VIDEO_01_RAW_CLIPS/img_02_tactical.jpg -vf "zoompan=z='min(zoom+0.0015,1.15)':d=120:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)',framerate=24" -c:v libx264 -t 5 -s 1920x1080 -pix_fmt yuv420p VIDEO_01_RAW_CLIPS/clip_02_tactical.mp4 2>/dev/null
fi

# Process Clip 3
if [ -f "VIDEO_01_RAW_CLIPS/img_03_office.jpg" ]; then
    echo "Animating Clip 3: The Command Center..."
    ffmpeg -y -loop 1 -i VIDEO_01_RAW_CLIPS/img_03_office.jpg -vf "zoompan=z='min(zoom+0.0015,1.15)':d=120:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)',framerate=24" -c:v libx264 -t 5 -s 1920x1080 -pix_fmt yuv420p VIDEO_01_RAW_CLIPS/clip_03_office.mp4 2>/dev/null
fi

echo "[HVF SYSTEM] Animation matrix complete. Video clips synthesized."
