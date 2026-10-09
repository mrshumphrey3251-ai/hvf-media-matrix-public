import json
import time

def emit_kinetic_payload(vertical, target_node, pwr_state, actuator_state, kinetic_rate):
    """
    Translates UI commands into raw industrial JSON payloads.
    Ready to be broadcast via MQTT to physical Edge Controllers (PLCs).
    """
    payload = {
        "timestamp_ms": int(time.time() * 1000),
        "vertical_matrix": vertical,
        "target_hardware_node": target_node,
        "kinetic_states": {
            "MAIN_PWR_RELAY": 1 if pwr_state else 0,
            "ACTUATOR_VALVE": 1 if actuator_state else 0,
            "VFD_RPM_PCT": kinetic_rate
        },
        "auth_token": "EBONY_TIER_1_OVERRIDE"
    }
    
    json_payload = json.dumps(payload, indent=2)
    
    # FUTURE HARDWARE EXPANSION: 
    # mqtt_client.publish(f"HVF/{vertical}/{target_node}/CMD", json_payload)
    
    return json_payload
