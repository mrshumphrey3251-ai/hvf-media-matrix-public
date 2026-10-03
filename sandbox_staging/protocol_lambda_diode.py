import socket
import json
import time
import hashlib
import hmac

class ProtocolLambdaDiode:
    def __init__(self, bind_ip="127.0.0.1", bind_port=5005, secret_key="HVF_SOVEREIGN_TOKEN_2026", max_latency_ms=10.0, watchdog_timeout_s=0.2):
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.secret_key = secret_key
        self.max_latency_ms = max_latency_ms
        self.watchdog_timeout_s = watchdog_timeout_s
        self.last_valid_heartbeat = time.time()
        self.actuation_engaged = False
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.bind_ip, self.bind_port))
        self.sock.settimeout(0.05)

    def _compute_hash(self, protocol_str, sovereignty_str):
        raw = f"{protocol_str}:{sovereignty_str}:{self.secret_key}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    def check_watchdog(self):
        if time.time() - self.last_valid_heartbeat > self.watchdog_timeout_s:
            if self.actuation_engaged:
                self.actuation_engaged = False
                print("[WATCHDOG TRIPPED] Heartbeat lost. Physical actuation dropped to zero-torque.")
            return False
        return True

    def poll_frame(self):
        try:
            data, addr = self.sock.recvfrom(4096)
            now = time.time()
            pkt = json.loads(data.decode("utf-8"))
            
            expected_sig = self._compute_hash(pkt.get("protocol", ""), pkt.get("sovereignty", ""))
            if not hmac.compare_digest(expected_sig, str(pkt.get("signature", ""))):
                return False, f"REJECTED: Invalid HMAC signature from {addr}", None
            
            telemetry = pkt.get("telemetry", {})
            inference_ms = float(telemetry.get("inference_ms", 999.0))
            if inference_ms > self.max_latency_ms:
                return False, f"REJECTED: Latency breach ({inference_ms}ms > {self.max_latency_ms}ms ceiling)", None
            
            throttle = float(pkt.get("throttle_demand", 0.0))
            if throttle > 0.85 or throttle < 0.0:
                return False, f"REJECTED: Throttle demand ({throttle}) outside safe operating bounds", None
            
            self.last_valid_heartbeat = now
            self.actuation_engaged = True
            return True, "EXECUTABLE: Frame compliant with bare-metal safety floors", pkt

        except socket.timeout:
            self.check_watchdog()
            return False, "IDLE: Socket poll timeout", None
        except Exception as err:
            return False, f"FAULT: Malformed packet payload ({err})", None

    def close(self):
        self.sock.close()

if __name__ == "__main__":
    print("[HVF CORE] Protocol Lambda Diode operational on Windows.")
