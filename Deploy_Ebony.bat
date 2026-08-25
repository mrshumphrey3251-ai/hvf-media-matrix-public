@echo off
title Humphrey Virtual Farm - Sovereign Node Installer
color 0A
cls
echo =====================================================================
echo    HUMPHREY VIRTUAL FARM (HVF) - SOVEREIGN NODE AUTO-DEPLOYMENT
echo =====================================================================
echo.
echo [*] Checking System Environment...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Python 3 not detected. Please install Python 3.10+ and re-run.
    pause
    exit /b
)

echo [*] Initializing Local Node Workspace in C:\HVF_Client_Node...
if not exist "C:\HVF_Client_Node" mkdir "C:\HVF_Client_Node"
cd /d "C:\HVF_Client_Node"

echo [*] Pulling Public Architecture from GitHub...
where git >nul 2>nul
if %errorlevel% equ 0 (
    if not exist "hvf-media-matrix-public" (
        git clone https://github.com/mrshumphrey3251-ai/hvf-media-matrix-public.git
    ) else (
        cd hvf-media-matrix-public
        git pull origin main
        cd ..
    )
    cd hvf-media-matrix-public
) else (
    echo [*] Downloading core files directly...
    powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/mrshumphrey3251-ai/hvf-media-matrix-public/main/ebony_console_GREEN.py' -OutFile 'ebony_console_GREEN.py'"
    powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/mrshumphrey3251-ai/hvf-media-matrix-public/main/requirements.txt' -OutFile 'requirements.txt'"
)

echo [*] Installing Sovereign Engine Dependencies...
pip install -r requirements.txt --quiet

echo.
echo =====================================================================
echo    INSTALLATION COMPLETE - LAUNCHING 7-DAY PILOT NODE
echo =====================================================================
echo.
streamlit run ebony_console_GREEN.py --server.port 8501
pause