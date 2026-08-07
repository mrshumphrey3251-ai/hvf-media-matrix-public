#!/bin/bash
# HVF Autonomous Log Rotation Matrix
echo "--- COMMENCING LOG ROTATION: $(date) ---"

LOGS=(
  "/home/mrshumphrey3251/HVF_NEXUS_CORE_V2_PRIVATE/omni_sight_execution.log"
  "/home/mrshumphrey3251/HVF_INTEL_SCRAPER/scraper_cron.log"
  "/home/mrshumphrey3251/HVF_INTEL_SCRAPER/osint_targets.log"
  "/home/mrshumphrey3251/HVF_MEDIA_MATRIX/autoresponder_cron.log"
)

for log in "${LOGS[@]}"; do
  if [ -f "$log" ]; then
    tail -n 1000 "$log" > "$log.tmp" && mv "$log.tmp" "$log"
    echo "[+] Rotated and truncated: $log"
  fi
done

echo "--- LOG ROTATION CONCLUDED ---"
