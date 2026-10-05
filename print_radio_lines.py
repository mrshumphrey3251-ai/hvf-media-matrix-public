from pathlib import Path
p = Path(r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py")
with open(p, "r", encoding="utf-8", errors="replace") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "st.sidebar.radio" in line or "Command Modules" in line:
        start = max(0, i - 5)
        end = min(len(lines), i + 15)
        print(f"--- Context around line {i+1} ---")
        for j in range(start, end):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
