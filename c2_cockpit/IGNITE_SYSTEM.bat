@echo off
echo [HVF SOVEREIGN IGNITION SEQUENCE INITIATED]
echo ===========================================
echo 1. Igniting Media Matrix Backend (Port 8000)...
start powershell -NoExit -Command "title 'Matrix Backend API'; python -m uvicorn matrix_backend_BLUE:app --port 8000"

echo 2. Igniting Ebony Command Deck (Port 8501)...
start powershell -NoExit -Command "title 'Ebony Command Deck'; streamlit run ebony_console_GREEN.py"
