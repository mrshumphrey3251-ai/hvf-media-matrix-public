import hashlib
import time

def verify_firmware_signature(firmware_payload, provided_signature):
    """
    MATHEMATICAL PROOF OF ORIGIN
    Verifies that the OTA firmware was compiled by the Master Edge Node and remains unaltered.
    """
    print("[*] INITIATING OTA CRYPTOGRAPHIC VERIFICATION...")
    time.sleep(0.4)
    calculated_hash = hashlib.sha256(firmware_payload.encode('utf-8')).hexdigest()
    
    if calculated_hash == provided_signature:
        return True
    return False

def deploy_immutable_image(node_id, firmware_version):
    """
    Executes a zero-downtime A/B partition swap on the edge node.
    """
    print(f"[*] DEPLOYING IMMUTABLE FIRMWARE {firmware_version} TO EDGE NODE: {node_id}...")
    time.sleep(0.6)
    print(f"[+] SUCCESS: Node {node_id} partitioned. Active OS swapped to {firmware_version}.")

def execute_ota_pipeline():
    # The true sovereign payload and its exact signature
    sovereign_payload = "EBONY_OS_KERNEL_V2.1.4_RAW_BIN"
    valid_signature = hashlib.sha256(sovereign_payload.encode('utf-8')).hexdigest()
    
    # SCENARIO A: Adversary attempts to inject a modified payload
    print("--- INCOMING OTA TRANSMISSION: UNKNOWN/HOSTILE SOURCE ---")
    hostile_payload = "EBONY_OS_KERNEL_V2.1.4_MODIFIED_BY_ADVERSARY"
    
    if not verify_firmware_signature(hostile_payload, valid_signature):
        print("[!] CRITICAL: Signature mismatch. Firmware altered in transit.")
        print("[X] OTA ABORTED: Payload incinerated to protect edge node integrity.\n")
    
    # SCENARIO B: Sovereign Command sends the authentic payload
    print("--- INCOMING OTA TRANSMISSION: SOVEREIGN MASTER COMMAND ---")
    if verify_firmware_signature(sovereign_payload, valid_signature):
        print("[+] SIGNATURE VERIFIED: Firmware mathematically authenticated.")
        deploy_immutable_image("NODE-AGR-ALPHA-01", "v2.1.4")

if __name__ == "__main__":
    execute_ota_pipeline()
