def evaluate_clearance(user_tier, action_type="READ"):
    """
    SOVEREIGN RBAC MATRIX // RECALIBRATED
    """
    # Tier-1 (CEO): Absolute Omni-Matrix Authority
    if user_tier == 1:
        return {"access_granted": True, "msg": "TIER-1 CEO CLEARANCE ACCEPTED. SOVEREIGN SECRETS UNLOCKED."}
        
    # Tier-2 (Drew / Executive): Standard + Emergency Actuation. Locked from CEO Secrets.
    if user_tier == 2:
        if action_type in ["CEO_SECRET", "ZERO_DAY", "LETHAL", "TREASURY_LIQUIDATION"]:
            return {"access_granted": False, "msg": "ACCESS DENIED. ACTION INTERSECTS CEO SOVEREIGN SECRETS. EXECUTIVE CLEARANCE INSUFFICIENT."}
        return {"access_granted": True, "msg": "TIER-2 EXECUTIVE CLEARANCE ACCEPTED. EMERGENCY & OPERATIONAL SCADA UNLOCKED."}
        
    # Tier-3 (Paid Member): Read-Only Telemetry, Zero Kinetic Actuation
    if user_tier == 3:
        if action_type in ["KINETIC", "EMERGENCY_OVERRIDE", "CEO_SECRET", "ZERO_DAY", "LETHAL"]:
            return {"access_granted": False, "msg": "ACCESS DENIED. COMMERCIAL MEMBERSHIP PERMITS READ-ONLY TELEMETRY."}
        return {"access_granted": True, "msg": "TIER-3 MEMBER CLEARANCE ACCEPTED. TELEMETRY STREAM ONLINE."}
        
    # Tier-4 (Guest): Absolute Lockout
    return {"access_granted": False, "msg": "ACCESS DENIED. GUEST CLEARANCE INSUFFICIENT FOR SOVEREIGN OPERATIONS."}

def map_identity_to_tier(identity_string):
    if "CEO" in identity_string: return 1
    if "Drew" in identity_string: return 2
    if "Member" in identity_string: return 3
    return 4
