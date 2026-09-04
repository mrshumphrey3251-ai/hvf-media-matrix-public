"""
[HVF EXECUTIVE SPECIFICATION]
PROJECT EBONY: PROTOCOL LAMBDA SECURE GATEWAY
AUTHOR: JEFFERY HUMPHREY, CEO
DESCRIPTION: Validates telemetry packets and verifies cryptographic hash attestation.
"""
import socket
import json
import hashlib

SECRET_KEY = "HVF_SOVEREIGN_TOKEN_2026"

def compute_signature(payload_data):
    p = str(payload_data.get("protocol", ""))
    s = str(payload_data.get("sovereignty", ""))
    raw = p + ":" + s + ":" + SECRET_KEY
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def run_attested_listener(ip="127.0.0.1", port=5005, max_frames=3):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    sock.settimeout(10.0)
    print(f"[HVF GATEWAY] PROTOCOL LAMBDA: Attestation gate armed on {ip}:{port}")
    received = 0
    while received < max_frames:
        try:
            data, addr = sock.recvfrom(4096)
            pkt = json.loads(data.decode("utf-8"))
            expected_sig = compute_signature(pkt)
            if pkt.get("signature") == expected_sig and pkt.get("sovereignty") == "HVF_52_PERCENT_MAJORITY":
                received += 1
                print(f"[HVF GATEWAY] Frame #{received} VALIDATED: Attestation passed from {addr}")
            else:
                print(f"[HVF GATEWAY] REJECTED: Malformed or unverified frame from {addr}")
        except socket.timeout:
            print("[HVF GATEWAY] Listener timed out.")
            break
        except Exception as e:
            print(f"[HVF GATEWAY] Ingestion failure: {e}")
            break
    sock.close()
    print("[HVF GATEWAY] Attestation test sequence concluded.")

if __name__ == "__main__":
    run_attested_listener()
