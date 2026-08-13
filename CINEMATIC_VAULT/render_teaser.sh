#!/bin/bash
echo "[HVF SYSTEM] Initializing Project Ebony Teaser Render..."

# Create the sequence ledger for FFmpeg
cat << 'LIST' > render_list.txt
file 'VIDEO_01_RAW_CLIPS/clip_01_swarm.mp4'
file 'VIDEO_01_RAW_CLIPS/clip_02_tactical.mp4'
file 'VIDEO_01_RAW_CLIPS/clip_03_office.mp4'
LIST

# Execute the seamless render
ffmpeg -y -f concat -safe 0 -i render_list.txt -c copy PROJECT_EBONY_TEASER.mp4
rm render_list.txt

echo "[HVF SYSTEM] Render complete: PROJECT_EBONY_TEASER.mp4 generated."
