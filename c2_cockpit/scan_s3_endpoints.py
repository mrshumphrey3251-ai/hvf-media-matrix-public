import os
import re
import urllib.request
from pathlib import Path

cockpit_dir = Path(r"C:\hvf_c2\hvf-media-matrix-private\c2_cockpit")
s3_pattern = re.compile(r'https?://[a-zA-Z0-9.\-_]*amazonaws\.com[a-zA-Z0-9./_\-?&=%]*')

print("=" * 84)
print("     E.B.O.N.Y. SOVEREIGN AWS S3 & CLOUD ENDPOINT AUDIT     ")
print("=" * 84)

found_urls = []

for py_file in cockpit_dir.glob("*.py"):
    try:
        content = py_file.read_text(encoding="utf-8")
        matches = s3_pattern.findall(content)
        for match in matches:
            found_urls.append((py_file.name, match))
    except Exception:
        pass

if not found_urls:
    print("[*] No direct AWS S3 URLs found hardcoded in c2_cockpit Python modules.")
    print("[*] Checking for other external storage links (storage.googleapis.com, etc.)...")
    generic_pattern = re.compile(r'https?://[a-zA-Z0-9.\-_]*(?:storage|bucket|blob)[a-zA-Z0-9./_\-?&=%]*')
    for py_file in cockpit_dir.glob("*.py"):
        try:
            content = py_file.read_text(encoding="utf-8")
            matches = generic_pattern.findall(content)
            for match in matches:
                found_urls.append((py_file.name, match))
        except Exception:
            pass

print(f"Total Cloud Storage References Detected: {len(found_urls)}\n")

for filename, url in set(found_urls):
    print(f"File: {filename}")
    print(f"URL:  {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "EBONY-Diagnostic/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f"Status: HTTP {resp.status} (OK)")
    except urllib.error.HTTPError as e:
        print(f"Status: HTTP {e.code} ({e.reason}) <--- POTENTIAL CULPRIT")
    except Exception as e:
        print(f"Status: Error ({e})")
    print("-" * 84)

print("=" * 84)