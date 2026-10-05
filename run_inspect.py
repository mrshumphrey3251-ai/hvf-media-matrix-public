filepath = r"C:\HVF_Repos\hvf-media-matrix-private\c2_cockpit\ebony_console_GREEN.py"
with open(filepath, "r", encoding="utf-8-sig") as f:
    lines = f.readlines()
for idx in range(max(0, 580), min(len(lines), 615)):
    print(f"{idx+1:4d}: {repr(lines[idx])}")
