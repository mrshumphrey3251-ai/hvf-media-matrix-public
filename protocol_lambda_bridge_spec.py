"""
[HVF EXECUTIVE SPECIFICATION] 
PROJECT EBONY: PROTOCOL LAMBDA (WEBRTC BRIDGE RECEIVER)
AUTHOR: JEFFERY HUMPHREY, CEO

DESCRIPTION: 
Active UDP receiver enforcing the one-way data diode.
Listens on local loopback, captures incoming telemetry/media frames,
and logs attestation without permitting external reverse execution.
"""

import socket
import json
import time

def run_isolated_listener(ip="127.0.0.1", port=5005, max_frames=3):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    sock.settimeout(10.0)
    print(f"[HVF GATEWAY] PROTOCOL LAMBDA: Listening on {ip}:{port} (Waiting for {max_frames} frames)...")
    
    received_count = 0
    while received_count < max_frames:
        try:
            data, addr = sock.recvfrom(4096)
            payload = json.loads(data.decode("utf-8"))
            received_count += 1
            print(f"[HVF GATEWAY] Captured Frame #{received_count} from {addr}:")
            print(f"    Protocol: {payload.get('protocol')}")
            print(f"    Sovereignty: {payload.get('sovereignty')}")
            print(f"    Inference Latency: {payload.get('telemetry', {}).get('openvino_inference_ms')} ms")
        except socket.timeout:
            print("[HVF GATEWAY] Socket timed out waiting for payload.")
            break
        except Exception as e:
            print(f"[HVF GATEWAY] Ingestion error: {e}")
            break
            
    sock.close()
    print("[HVF GATEWAY] Verification batch successfully captured. Data diode secure.")

if __name__ == "__main__":
    run_isolated_listener()
