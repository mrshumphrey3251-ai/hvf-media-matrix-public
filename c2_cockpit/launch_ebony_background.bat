@echo off
taskkill /F /IM streamlit.exe >nul 2>&1
start /B ollama serve >nul 2>&1
start /B C:\mediamtx\mediamtx.exe >nul 2>&1
cd /d C:\HVF_Repos\hvf-media-matrix-private
start /B streamlit run ebony_console_GREEN.py --server.address 0.0.0.0 --server.port 8501 --server.headless true --server.enableCORS false --server.enableXsrfProtection false --browser.gatherUsageStats false
timeout /t 2 /nobreak >nul
start http://localhost:8501