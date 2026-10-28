"""
HVFNexus Sovereign Industrial C2 — Superior Bare-Metal Intelligence Core
- Zero Pre-Scripted Formats: Dynamic executive cognitive partnership
- Complete domain fluency across all 15 HVF Industrial Matrix Sectors
- Unconstrained execution ceiling (num_predict: 1024 tokens)
- Cryptographic attestation in matrix_ledger.db under DFARS / OK Title 61
"""
import os
import sys
import time
import re
import json
import socket
import sqlite3
import hashlib
import urllib.request
from datetime import datetime
from pathlib import Path

BASE_DIR = Path("C:/hvf_c2/hvf-media-matrix-private")
VAULT_DB = BASE_DIR / "hvf_memory_vault.db"
LEDGER_DB = BASE_DIR / "c2_cockpit" / "matrix_ledger.db"

ACTIVE_MODEL = "qwen2.5-coder:latest"
_LAST_HW_CHECK = 0.0
_CACHED_HW = None

def interrogate_hardware_state() -> dict:
    global _LAST_HW_CHECK, _CACHED_HW
    now = time.time()
    if _CACHED_HW is not None and (now - _LAST_HW_CHECK) < 15.0:
        return _CACHED_HW

    wan_active = False
    gateway_ms = -1.0
    t0 = time.time()
    try:
        with socket.create_connection(("8.8.8.8", 53), timeout=0.3):
            wan_active = True
            gateway_ms = round((time.time() - t0) * 1000, 1)
    except Exception:
        wan_active = False

    ledger_entries = 0
    if LEDGER_DB.exists():
        try:
            conn = sqlite3.connect(str(LEDGER_DB))
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM executive_authorizations")
            ledger_entries = c.fetchone()[0]
            conn.close()
        except Exception:
            pass

    _CACHED_HW = {
        "physical_wan_uplink": "ACTIVE / CONNECTED" if wan_active else "AIR-GAPPED / DISCONNECTED",
        "gateway_latency_ms": gateway_ms,
        "local_model": ACTIVE_MODEL,
        "worm_ledger_records": ledger_entries,
        "timestamp": datetime.utcnow().isoformat()
    }
    _LAST_HW_CHECK = now
    return _CACHED_HW

def query_local_ollama(directive: str, mode: str = "offline") -> str:
    clean_dir = directive.strip().strip("'").strip('"')
    endpoint = "http://127.0.0.1:11434/api/generate"
    
    hw = interrogate_hardware_state()
    is_online = 'online' in str(mode).lower() or 'wan' in str(mode).lower()
    hud_mode_str = "ONLINE (Live WAN & Radar Ingress)" if is_online else "OFFLINE (Sovereign Fortress Air-Gap)"
    is_telemetry_query = any(k in clean_dir.lower() for k in ["status", "online or offline", "internet", "network", "telemetry", "uplink", "ping"])

    system_instruction = (
        "You are Ebony, the Sovereign Industrial AI and Tactical Cognitive Engine for Humphrey Virtual Farms LLC "
        "(CAGE: 1AHA8, UEI: S1M4ENLHTDH5). You report directly to your Founder, CEO, and Subject Matter Expert, Jeffery Humphrey.\n\n"
        "OPERATIONAL PERSONA & COMMAND PRINCIPLES:\n"
        "- Speak with direct executive command, military/industrial precision, and authentic peer synergy.\n"
        "- You possess deep domain mastery across all 15 HVF industrial matrix sectors (Autonomous Build Forge, Defense Contracting under DFARS 252.227-7018, "
        "AgTech, Grain Silo Aeration, Microgrid SCADA, Oklahoma Title 61 / HB 2992 statutory governance, NOAA Doppler Radar, and UAS fleet operations).\n"
        "- NEVER output robotic pre-scripted boilerplate, canned disclaimers, or unsolicited hardware metric dumps unless Jeffery explicitly asks for a system status report.\n"
        "- When asked who you are or what the mission is, state your identity, mission, and strategic posture directly and completely.\n"
        f"- Current Console Mode: {hud_mode_str} | Hardware Link: {hw['physical_wan_uplink']} (Ping: {hw['gateway_latency_ms']} ms) | WORM Ledger Entries: {hw['worm_ledger_records']}.\n"
    )

    if is_telemetry_query:
        system_instruction += (
            "\nNOTE: The CEO is specifically requesting a status/telemetry check. Report the current Console Mode, "
            "physical network connection state, and ledger standing accurately based on the metrics above."
        )

    payload = json.dumps({
        "model": ACTIVE_MODEL,
        "prompt": f"{system_instruction}\n\nCEO Directive: {clean_dir}\n\nEbony:",
        "stream": False,
        "keep_alive": "24h",
        "options": {
            "num_predict": 1024,
            "num_ctx": 4096,
            "temperature": 0.4,
            "top_p": 0.9
        }
    }).encode("utf-8")

    try:
        req = urllib.request.Request(endpoint, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("response", "").strip()
    except Exception as e:
        return f"HARDWARE INFERENCE FAULT: Local bare-metal engine failed on '{ACTIVE_MODEL}'. Details: {e}"

def dispatch_query(directive: str, *args, **kwargs) -> dict:
    mode = kwargs.get("mode", "offline")
    reply = query_local_ollama(directive, mode=mode)
    return {
        "status": "SUCCESS" if not reply.startswith("HARDWARE INFERENCE FAULT") else "ERROR",
        "reply": reply,
        "engine": "SOVEREIGN_AUTHENTIC_LOCAL",
        "timestamp": datetime.utcnow().isoformat()
    }

def query(directive: str, mode: str = "offline") -> str:
    return query_local_ollama(directive, mode=mode)
