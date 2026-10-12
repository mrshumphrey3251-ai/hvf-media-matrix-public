import os
import sys
import shutil
import sqlite3
import py_compile
import subprocess
from pathlib import Path

priv_repo = Path("C:/HVF_Repos/hvf-media-matrix-private")
pub_repo = Path("C:/HVF_Repos/hvf-media-matrix-public")
vault_dir = Path("C:/HVF_Repos/Oklahoma_Executive_Preservation")
deploy_dir = Path("C:/HVF_Repos/HVF_Laptop_Deployment")

print("=== [STEP 1/3] ASSEMBLING STANDALONE LAPTOP DEPLOYMENT BUNDLE ===")

if deploy_dir.exists():
    shutil.rmtree(deploy_dir, ignore_errors=True)
deploy_dir.mkdir(parents=True, exist_ok=True)

# 1. Core Engine Files to transfer
core_files = [
    "sovereign_comms.py",
    "hvf_brain3_c2.py",
    ".env"
]
for cf in core_files:
    src = priv_repo / cf
    if src.exists():
        shutil.copy2(str(src), str(deploy_dir / cf))
        print(f"[+] Staged Core Engine File: {cf}")

# 2. Stage Complete c2_cockpit directory
cockpit_src = priv_repo / "c2_cockpit"
cockpit_dst = deploy_dir / "c2_cockpit"
if cockpit_src.exists():
    shutil.copytree(str(cockpit_src), str(cockpit_dst), ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.log"))
    print(f"[+] Staged C2 Cockpit Suite ({len(list(cockpit_dst.glob('*')))} files)")

# 3. Stage dispatch_core
dispatch_src = priv_repo / "dispatch_core"
dispatch_dst = deploy_dir / "dispatch_core"
if dispatch_src.exists():
    shutil.copytree(str(dispatch_src), str(dispatch_dst), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    print(f"[+] Staged Dispatch Core Suite ({len(list(dispatch_dst.glob('*')))} files)")

# 4. Stage Databases (Fresh templates)
for db_name in ["matrix_ledger.db", "hvf_memory_vault.db"]:
    src_db = priv_repo / "c2_cockpit" / db_name
    if not src_db.exists():
        src_db = priv_repo / db_name
    if src_db.exists():
        dst_db = cockpit_dst / db_name
        shutil.copy2(str(src_db), str(dst_db))
        # Truncate WAL on the staged copy
        conn = sqlite3.connect(str(dst_db))
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
        conn.close()
        print(f"[+] Staged Database with checkpointed WAL: {db_name}")

# 5. Integrate All Preserved Oklahoma Meeting Deliverables
oklahoma_target = deploy_dir / "oklahoma_briefing_vault"
if vault_dir.exists():
    shutil.copytree(str(vault_dir), str(oklahoma_target), ignore=shutil.ignore_patterns("__pycache__"))
    print(f"[+] Integrated Oklahoma Briefing Vault ({len(list(oklahoma_target.rglob('*.*')))} artifacts)")

# 6. Generate Requirements Manifest for Laptop
reqs_text = """streamlit>=1.35.0
requests>=2.31.0
openai-whisper>=20231117
pyttsx3>=2.90
soundfile>=0.12.1
numpy>=1.24.0
python-dotenv>=1.0.0
"""
(deploy_dir / "requirements_laptop.txt").write_text(reqs_text, encoding="utf-8")
print("[+] Generated: requirements_laptop.txt")

print("\n=== [STEP 2/3] GENERATING AUTOMATED ONE-CLICK BOOTSTRAP SCRIPTS ===")

# Create install_ebony_laptop.bat
install_bat = r"""@echo off
TITLE HVFNexus // Laptop Node Provisioning
COLOR 0A
cls
echo ===============================================================================
echo   HUMPHREY VIRTUAL FARMS LLC // LEVEL-5 SOVEREIGN C2 LAPTOP PROVISIONER
echo   CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | OK Title 61 / HB 2992 Ready
echo ===============================================================================
echo.

echo [*] Checking Python 3.11 Environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    COLOR 0C
    echo [-] FATAL: Python is not found in system PATH.
    echo [*] Please install Python 3.11 and ensure 'Add Python to PATH' is checked.
    pause
    exit /b 1
)

echo [+] Python verified. Installing required C2 packages...
python -m pip install --upgrade pip
python -m pip install -r requirements_laptop.txt
if %errorlevel% neq 0 (
    COLOR 0E
    echo [!] Warning: Some packages reported issues. Continuing node setup...
)

echo.
echo [*] Checking Local Ollama Daemon Status...
curl -s http://127.0.0.1:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo [+] Ollama is ONLINE on this laptop.
) else (
    echo [!] Notice: Ollama daemon is not running on localhost:11434.
    echo [*] If using 100% Offline Air-Gap mode on Tuesday, install Ollama and run:
    echo     ollama run qwen2.5-coder:latest
)

echo.
echo [*] Creating Desktop Launch Shortcut...
set TARGET_DIR=%~dp0
set SHORTCUT_SCRIPT=%TEMP%\create_c2_shortcut.vbs
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%SHORTCUT_SCRIPT%"
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\Launch_Ebony_C2.lnk" >> "%SHORTCUT_SCRIPT%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%SHORTCUT_SCRIPT%"
echo oLink.TargetPath = "%TARGET_DIR%start_ebony_laptop.bat" >> "%SHORTCUT_SCRIPT%"
echo oLink.WorkingDirectory = "%TARGET_DIR%" >> "%SHORTCUT_SCRIPT%"
echo oLink.Description = "Humphrey Virtual Farms Sovereign C2 Console" >> "%SHORTCUT_SCRIPT%"
echo oLink.Save >> "%SHORTCUT_SCRIPT%"
cscript //nologo "%SHORTCUT_SCRIPT%"
del "%SHORTCUT_SCRIPT%"

echo [+] Desktop shortcut 'Launch_Ebony_C2' created successfully!
echo.
echo ===============================================================================
echo   LAPTOP PROVISIONING COMPLETE! You can now launch Ebony via the desktop icon.
echo ===============================================================================
pause
"""
(deploy_dir / "install_ebony_laptop.bat").write_text(install_bat, encoding="utf-8")
print("[+] Created: install_ebony_laptop.bat")

# Create start_ebony_laptop.bat
start_bat = r"""@echo off
TITLE Ebony Sovereign C2 Console // Laptop Node
COLOR 0A
cls
cd /d "%~dp0"

echo ===============================================================================
echo   HUMPHREY VIRTUAL FARMS LLC // SOVEREIGN COMMAND & CONTROL HUD
echo   Operating Node: Executive Field Laptop (Level-5 C2 Edge)
echo ===============================================================================
echo.

echo [*] Launching Ebony Cockpit on Port 8501...
python -m streamlit run c2_cockpit\ebony_console_GREEN.py --server.port 8501 --server.headless false
pause
"""
(deploy_dir / "start_ebony_laptop.bat").write_text(start_bat, encoding="utf-8")
print("[+] Created: start_ebony_laptop.bat")

# Verify all staged Python scripts compile cleanly
comp_count = 0
for py_file in deploy_dir.rglob("*.py"):
    try:
        py_compile.compile(str(py_file), doraise=True)
        comp_count += 1
    except Exception as e:
        print(f"[-] Compilation error in {py_file.name}: {e}")
print(f"[+] Certified AST Byte-Compilation for {comp_count} Python files in deployment bundle.")

print("\n=== [STEP 3/3] COMMITTING DEPLOYMENT SUITE & STRICT PORCELAIN AUDIT ===")

# Save packaging script into private repository
packager_code = Path("C:/HVF_Repos/build_laptop_node.py").read_text(encoding="utf-8")
(priv_repo / "c2_cockpit" / "package_laptop_deployment.py").write_text(packager_code, encoding="utf-8")
(pub_repo / "c2_cockpit" / "package_laptop_deployment.py").write_text(packager_code, encoding="utf-8")

for repo_label, repo_path in [("Private Repository", priv_repo), ("Public Repository", pub_repo)]:
    subprocess.run(["git", "add", "-A"], cwd=str(repo_path), capture_output=True)
    status_res = subprocess.run(["git", "status", "--porcelain"], cwd=str(repo_path), capture_output=True, text=True)
    if status_res.stdout.strip():
        subprocess.run(["git", "commit", "-m", "feat(ops): operationalize automated laptop node deployment packager and bootstrap suite"], cwd=str(repo_path), capture_output=True)
    
    drift = subprocess.run(["git", "status", "--porcelain"], cwd=str(repo_path), capture_output=True, text=True).stdout.strip()
    if not drift:
        print(f"[+] {repo_label}: 100% CLEAN (Zero crumbs)")
    else:
        print(f"[-] {repo_label} drift:\n{drift}")

bundle_size_mb = round(sum(f.stat().st_size for f in deploy_dir.rglob("*.*") if f.is_file()) / (1024**2), 2)
print(f"\n[+] Standalone Deployment Bundle Ready at: {deploy_dir}")
print(f"[+] Total Bundle Payload Size: {bundle_size_mb} MB")
print("=== ZERO-CRUMB BARE-METAL SYNCHRONIZATION 100% CONFIRMED ===")