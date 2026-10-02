def parse_kinetic_intent(user_input):
    """
    SEMANTIC KINETIC PARSER // DYNAMIC SEVERITY TAGGING
    """
    input_lower = user_input.lower()
    
    # [CEO SECRET] Zero-Day Wipe
    if "zero day" in input_lower or "wipe" in input_lower:
        return {
            "intent_detected": True,
            "vertical": "🔐 CRYPTO CYBER",
            "target_node": "VAULT-ROOT",
            "pwr_state": False,
            "actuator_state": False,
            "kinetic_rate": 0,
            "action_severity": "CEO_SECRET",
            "action_desc": "ZERO-DAY WIPE EXECUTED. CRYPTOGRAPHIC LEDGERS INCINERATED."
        }
        
    # [EMERGENCY OVERRIDE] Hypoxic Vent
    if "vertical 15" in input_lower or "warehousing" in input_lower:
        if "hypoxic vent" in input_lower or "vent" in input_lower:
            return {
                "intent_detected": True,
                "vertical": "📦 WAREHOUSING",
                "target_node": "TARGET ALL NODES",
                "pwr_state": True,
                "actuator_state": True,
                "kinetic_rate": 100,
                "action_severity": "EMERGENCY_OVERRIDE",
                "action_desc": "HYPOXIC VENT EXECUTED. NITROGEN FLOOD ACTIVE."
            }
            
    # [STANDARD KINETIC] TBM Thrust
    if "vertical 11" in input_lower or "mining" in input_lower:
        if "thrust" in input_lower or "advance" in input_lower:
            return {
                "intent_detected": True,
                "vertical": "⛏️ MINING",
                "target_node": "TBM-OMEGA-01",
                "pwr_state": True,
                "actuator_state": True,
                "kinetic_rate": 85,
                "action_severity": "KINETIC",
                "action_desc": "TBM THRUST ENGAGED. ADVANCING AT 85% RPM."
            }

    return {"intent_detected": False}
