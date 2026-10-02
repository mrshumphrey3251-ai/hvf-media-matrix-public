import protocol_lambda_diode
import time

diode = protocol_lambda_diode.ProtocolLambdaDiode()
print("=" * 70)
print("HVF PROTOCOL LAMBDA DIODE — DESKTOP COMMAND BRIDGE (ACTIVE)")
print("UDP Port: 5005 | Bound: 127.0.0.1 | Watchdog Ceiling: 200ms")
print("=" * 70)
try:
    while True:
        valid, msg, pkt = diode.poll_frame()
        if valid:
            th = pkt.get("throttle_demand")
            print(f"[DESKTOP INGEST] {msg} | Throttle: {th}")
        time.sleep(0.01)
except KeyboardInterrupt:
    diode.close()
    print("\n[SYSTEM] Desktop listener disengaged cleanly.")
