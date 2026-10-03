@echo off
title HVF Sovereign Auto-Daemon
cd /d C:\HVF_Repos\hvf-media-matrix-private

:: Ensure Ollama offline engine is active
tasklist /fi "imagename eq ollama.exe" | find /i "ollama.exe" >nul
if errorlevel 1 (
    start /min "" ollama serve
)

:: Ensure MediaMTX video stream server is active
tasklist /fi "imagename eq mediamtx.exe" | find /i "mediamtx.exe" >nul
if errorlevel 1 (
    start /min "" C:\HVF_Repos\hvf-media-matrix-private\mediamtx\mediamtx.exe C:\HVF_Repos\hvf-media-matrix-private\mediamtx\mediamtx.yml
)

:: Ensure Streamlit console is active
tasklist /fi "imagename eq streamlit.exe" | find /i "streamlit.exe" >nul
if errorlevel 1 (
    start /min "" streamlit run ebony_console_GREEN.py --server.address 0.0.0.0 --server.port 8501 --server.headless true
    timeout /t 2 >nul
)

:: Launch Browser
start http://192.168.1.175:8501