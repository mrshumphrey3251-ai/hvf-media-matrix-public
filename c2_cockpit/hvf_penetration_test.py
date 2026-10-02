# hvf_penetration_test.py - HVF Media Matrix End-to-End System Verification
# Engineered to prove structural integrity from ingestion to tactical execution.

import urllib.request
import urllib.error
import json
from hvf_security_gateway import HVFSecurityGateway

gateway = HVFSecurityGateway()
url = "http://localhost:3000/api/ingest"

print("[SYSTEM START] Initiating HVF Tactical Deployment Protocol...")

# AUTHORIZED STRIKE: Trigger the LinkedIn Arm with Dynamic Content
print("\n[TACTICAL STRIKE] Firing AUTHORIZED payload (Dynamic LinkedIn Broadcast)...")

dynamic_message = "End-to-end dynamic payload routing verified. The HVF Sovereign Core Server is now actively translating secure API ingestion directly into live network deployment. Architecture secured."

payload_dict = {
    "directive": "LinkedIn Broadcast",
    "message": dynamic_message
}

data = json.dumps(payload_dict).encode('utf-8')
valid_token = gateway.generate_timestamp_token()

req_auth = urllib.request.Request(url, data=data, method='POST')
req_auth.add_header('X-HVF-Token', valid_token)

try:
    response = urllib.request.urlopen(req_auth)
    print(f"       Result: DOMINANCE VERIFIED - Payload accepted (HTTP {response.getcode()})")
    print(f"       Server Output: {response.read().decode('utf-8')}")
except Exception as e:
    print(f"       Result: FAILURE - Error processing authorized payload: {e}")