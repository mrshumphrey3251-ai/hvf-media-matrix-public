"""
HVF Sovereign C2 // Official 83-Suite Unit & Extreme Stress Test Runner (CAGE: 1AHA8)
"""
import os, subprocess, sys
from pathlib import Path

def main() -> int:
    c2 = Path(__file__).resolve().parent
    test_files = sorted(c2.glob("test_*.py"))
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["HVF_SILENT_CLIPBOARD"] = "1"
    env["PYTHONPATH"] = str(c2) + os.pathsep + str(c2.parent)

    passed, failed = [], []
    for tf in test_files:
        res = subprocess.run([sys.executable, str(tf)], cwd=str(c2), capture_output=True, encoding="utf-8", errors="replace", env=env, timeout=30)
        if res.returncode == 0:
            passed.append(tf.name)
        else:
            out_str = (res.stderr or "") + "\n" + (res.stdout or "")
            lines = [ln.strip() for ln in out_str.splitlines() if ln.strip()]
            failed.append((tf.name, " || ".join(lines[-3:])))

    print("=" * 84)
    print(f"=== HVF SOVEREIGN 83-TEST LEDGER: {len(passed)} / {len(test_files)} PASSED ===")
    print(f"  Unit Test Suites PASSED : {len(passed)} / {len(test_files)}")
    print(f"  Unit Test Suites FAILED : {len(failed)} / {len(test_files)}")
    for fn, msg in failed:
        print(f"    [FAIL] {fn:36s} -> {msg[:115]}")
    print("=" * 84)
    return 0 if not failed else 1

if __name__ == "__main__":
    sys.exit(main())
