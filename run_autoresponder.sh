#!/bin/bash
# HVF Autonomous Commercial Intake Trigger
cd /home/mrshumphrey3251/HVF_MEDIA_MATRIX
export GMAIL_APP_PASSWORD="[REDACTED_FOR_PUBLIC_AUDIT]"
echo "--- INTAKE SWEEP INITIATED: $(date) ---" >> autoresponder_cron.log
python3 commercial_autoresponder.py >> autoresponder_cron.log 2>&1
echo "--- INTAKE SWEEP CONCLUDED ---" >> autoresponder_cron.log
