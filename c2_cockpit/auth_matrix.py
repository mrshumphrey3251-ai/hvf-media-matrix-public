from core.mfa_matrix import verify_mfa_token

def verify_credentials(username, password, mfa_token=None):
    """
    SOVEREIGN AUTHENTICATION MATRIX // MFA RECALIBRATED
    """
    valid_ledgers = {
        "humphrey": {"pass": "omega", "role": "👑 Mr. Humphrey (Tier-1 CEO)", "mfa_required": True},
        "drew": {"pass": "alpha", "role": "🛡️ Drew (Tier-2 Executive)", "mfa_required": True},
        "member": {"pass": "beta", "role": "💼 Paid Member (Tier-3 Commercial)", "mfa_required": False}
    }
    
    user = valid_ledgers.get(username.lower())
    if user and user["pass"] == password:
        if user["mfa_required"]:
            if mfa_token and verify_mfa_token(mfa_token):
                return user["role"]
            else:
                return "MFA_FAILED"
        return user["role"]
    return None
