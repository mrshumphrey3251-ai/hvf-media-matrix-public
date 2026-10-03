import os
import sys
import py_compile

BASE_DIR = r"C:\HVF_Repos\hvf-media-matrix-private"
TARGET_FILES = [
    os.path.join(BASE_DIR, "ebony_console.py"),
    os.path.join(BASE_DIR, "ebony_console_GREEN.py")
]

print("=" * 80)
print("REPAIRING CONSOLE INDENTATION & VERIFYING AST INTEGRITY")
print("=" * 80)

for fpath in TARGET_FILES:
    if not os.path.exists(fpath):
        continue

    print(f"\nAuditing: {os.path.basename(fpath)}")
    with open(fpath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Remove all injected PRAGMA busy_timeout lines causing indentation mismatches
    cleaned_lines = []
    removed_count = 0
    for line in lines:
        if 'PRAGMA busy_timeout = 30000;' in line:
            removed_count += 1
            continue
        cleaned_lines.append(line)

    print(f"  * Excised {removed_count} malformed inline PRAGMA statements.")

    # Write back clean source
    with open(fpath, "w", encoding="utf-8") as f:
        f.writelines(cleaned_lines)

    # Perform strict AST compilation check
    try:
        py_compile.compile(fpath, doraise=True)
        print(f"  * [SUCCESS] Clean compile: Zero IndentationErrors, Zero SyntaxErrors.")
    except py_compile.PyCompileError as e:
        print(f"  * [FAIL] Compilation error detected:\n{e}")
        sys.exit(1)

print("\n" + "=" * 80)
print("INDENTATION REPAIR VERIFIED ACROSS ALL CONSOLE CONTROLLERS")
print("=" * 80)
