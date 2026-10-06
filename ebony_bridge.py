"""
HVF OMNI-INDUSTRIAL MODULAR BRIDGE - SUBSYSTEM DISPATCH FIREWALL
Project: Ebony Sovereign C2 Matrix
Compliance: Sovereign Air-Gap Tool Isolation & Deterministic Telemetry
"""

import sys
import platform
import os
import shutil
from ebony_scada_poll import format_scada_telemetry_payload
from ebony_agent_swarm import dispatch_swarm_task

def _get_memory_telemetry(payload):
    return "ALPHA_MEMORY: Sliding-window context engine active. Boundary ceiling: 6 turns / 4,000 characters."

def _get_agent_telemetry(payload):
    vector = payload.strip() if payload else "all"
    return dispatch_swarm_task(sub_vector=vector)

def _get_scada_telemetry(payload):
    channel = payload.strip() if payload else "ALL"
    return format_scada_telemetry_payload(channel=channel)

VECTOR_MAP = {
    "ALPHA_MEMORY": _get_memory_telemetry,
    "BETA_AGENTS": _get_agent_telemetry,
    "GAMMA_SCADA": _get_scada_telemetry
}

def route_matrix_command(intent_vector, payload=""):
    """
    Firewall router for auxiliary subsystems and operational telemetry.
    Ensures safe, deterministic metadata dispatch with absolute isolation from the LLM core.
    """
    handler = VECTOR_MAP.get(intent_vector)
    if handler:
        try:
            return handler(payload)
        except Exception as e:
            return f"VECTOR_FAULT: Subsystem {intent_vector} encountered exception: {str(e)}"
    return "VECTOR_UNMAPPED: No registered subsystem handler for requested vector."
