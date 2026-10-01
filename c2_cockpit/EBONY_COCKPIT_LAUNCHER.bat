@echo off
title PROJECT EBONY MASTER COMMAND COCKPIT
cd /d C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit
echo IGNITING LEVEL 5 SCADA ENGINE...
python -m streamlit run tactical_glass_cockpit.py
pause
