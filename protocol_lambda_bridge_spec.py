"""
[HVF EXECUTIVE SPECIFICATION]
PROJECT EBONY: PROTOCOL LAMBDA SECURE GATEWAY & GUILLOTINE INTERLOCK
AUTHOR: JEFFERY HUMPHREY, CEO
DESCRIPTION: UDP diode with cryptographic SHA-256 attestation and real-time kinetic severance.
"""
import socket
import json
import hashlib
from kinetic_guillotine_enforcer import KineticGuillotine

SECRET_KEY = "HVF_SOVEREIGN_TOKEN_2026"

def compute_signature(payload_data):
    p = str(payload_data.get("protocol", ""))
    s = str(payload_data.get("sovereignty", ""))
    raw = p + ":" + s + ":" + SECRET_KEY
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def run_secured_gateway(ip="127.0.0.1", port=5005, max_frames=3):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    sock.settimeout(10.0)
    guillotine = KineticGuillotine()
    print(f"[HVF SECURE CORE] Gateway armed on {ip}:{port} with active Kinetic Guillotine.")
    received = 0
    while received < max_frames:
        try:
            data, addr = sock.recvfrom(4096)
            pkt = json.loads(data.decode("utf-8"))
            expected_sig = compute_signature(pkt)
            if pkt.get("signature") != expected_sig:
                print(f"[HVF GATEWAY] DROPPED: Invalid SHA-256 signature from {addr}")
                continue
            is_safe, verdict = guillotine.evaluate_command(pkt)
            if not is_safe:
                print(f"[HVF GATEWAY] BLOCKED BY GUILLOTINE: {verdict}")
                continue
            received += 1
            print(f"[HVF GATEWAY] Frame #{received} INGESTED & EXECUTABLE: {verdict}")
        except socket.timeout:
            print("[HVF GATEWAY] Listener timed out.")
            break
        except Exception as e:
            print(f"[HVF GATEWAY] Socket fault: {e}")
            break
    sock.close()
    print("[HVF SECURE CORE] Secure session closed cleanly.")

if __name__ == "__main__":
    run_secured_gateway()
