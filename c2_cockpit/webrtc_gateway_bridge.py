"""
[HVF EXECUTIVE SPECIFICATION]
PROJECT EBONY: PROTOCOL LAMBDA SECURE GATEWAY & GUILLOTINE INTERLOCK
AUTHOR: JEFFERY HUMPHREY, CEO
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

def run_secured_gateway(ip="127.0.0.1", port=5005, max_frames=20):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    sock.settimeout(5.0)
    guillotine = KineticGuillotine()
    print(f"[HVF SECURE CORE] Gateway armed on {ip}:{port} (Evaluating 20-packet stream)...")
    passed = 0
    dropped = 0
    for _ in range(max_frames):
        try:
            data, addr = sock.recvfrom(4096)
            pkt = json.loads(data.decode("utf-8"))
            expected_sig = compute_signature(pkt)
            if pkt.get("signature") != expected_sig:
                print(f"[HVF GATEWAY] DROPPED: Invalid SHA-256 signature from {addr}")
                dropped += 1
                continue
            is_safe, verdict = guillotine.evaluate_command(pkt)
            if not is_safe:
                print(f"[HVF GATEWAY] BLOCKED BY GUILLOTINE: {verdict}")
                dropped += 1
                continue
            passed += 1
            print(f"[HVF GATEWAY] Frame VALIDATED & EXECUTABLE: {verdict}")
        except socket.timeout:
            break
        except Exception as e:
            print(f"[HVF GATEWAY] PARSE FAULT: {e}")
            dropped += 1
    sock.close()
    print(f"[HVF AUDIT RESULT] Packets Evaluated: {passed + dropped} | Ingested: {passed} | Dropped/Blocked: {dropped}")

if __name__ == "__main__":
    run_secured_gateway()
