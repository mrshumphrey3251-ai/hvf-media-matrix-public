import time
import hmac
import hashlib

def generate_current_token(seed: str, window_minutes=1) -> str:
    """Generates a 6-digit cryptographic token based on a seed and the current time window."""
    time_window = int(time.time() // (window_minutes * 60))
    message = str(time_window).encode('utf-8')
    secret = seed.encode('utf-8')
    
    hash_digest = hmac.new(secret, message, hashlib.sha256).digest()
    
    offset = hash_digest[-1] & 0x0f
    truncated_hash = (hash_digest[offset] & 0x7f) << 24 | \
                     (hash_digest[offset + 1] & 0xff) << 16 | \
                     (hash_digest[offset + 2] & 0xff) << 8 | \
                     (hash_digest[offset + 3] & 0xff)
                     
    return str(truncated_hash % 1000000).zfill(6)

def verify_mfa_token(input_token: str, seed: str, window_minutes=1) -> bool:
    """Verifies the token against the current and previous 60-second window."""
    if not input_token or not input_token.isdigit() or len(input_token) != 6:
        return False
        
    current_time = int(time.time() // (window_minutes * 60))
    
    # Check current and previous window to allow a grace period for execution
    for window in [current_time, current_time - 1]:
        message = str(window).encode('utf-8')
        secret = seed.encode('utf-8')
        hash_digest = hmac.new(secret, message, hashlib.sha256).digest()
        
        offset = hash_digest[-1] & 0x0f
        truncated_hash = (hash_digest[offset] & 0x7f) << 24 | \
                         (hash_digest[offset + 1] & 0xff) << 16 | \
                         (hash_digest[offset + 2] & 0xff) << 8 | \
                         (hash_digest[offset + 3] & 0xff)
                         
        expected_token = str(truncated_hash % 1000000).zfill(6)
        
        if hmac.compare_digest(input_token, expected_token):
            return True
            
    return False
    
if __name__ == "__main__":
    # Generate the live CEO token for kinetic testing
    master_seed = "EBONY_TIER_1_CEO"
    print("==================================================")
    print("🛡️ KINETIC MFA GENERATOR ONLINE")
    print("==================================================")
    print(f"Current Master CEO Token: {generate_current_token(master_seed)}")
    print("Token rotates every 60 seconds.")
