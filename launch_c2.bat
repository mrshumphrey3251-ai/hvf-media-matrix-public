@echo off
cd /d "C:\HVF_Repos\hvf-media-matrix-private"
"C:\Users\mrshu\AppData\Local\Programs\Python\Python311\python.exe" -m streamlit run c2_cockpit\ebony_console_GREEN.py --server.port 8501 --server.headless false
