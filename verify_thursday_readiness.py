"""
HVF OMNI-INDUSTRIAL PRE-FLIGHT VERIFICATION HARNESS
Compliance: Submission 9-26-3703 // CAGE 1AHA8
Target: Rapid Pre-Demo Diagnostic Sweep
"""

import sys
import os

print("=" * 60)
print("[*] INITIATING THURSDAY DEMO READINESS SWEEP...")
print("=" * 60)

# Check 1: Authority & Identity Core
try:
    from ebony_authority_matrix import get_sovereign_system_prompt
    prompt = get_sovereign_system_prompt()
    assert "1AHA8" in prompt and "S1M4ENLHTDH5" in prompt
    print("[+] 1. AUTHORITY MATRIX: CAGE 1AHA8 / UEI Verified.")
except Exception as e:
    print(f"[-] 1. AUTHORITY MATRIX FAULT: {e}")
    sys.exit(1)

# Check 2: Vocal Cortex
try:
    from ebony_vocal_cortex import ignite_voice
    wav = ignite_voice("Demonstration readiness nominal.")
    assert wav and os.path.exists(wav)
    print(f"[+] 2. VOCAL CORTEX: Acoustic WAV Verified ({wav}).")
except Exception as e:
    print(f"[-] 2. VOCAL CORTEX FAULT: {e}")
    sys.exit(1)

# Check 3: Persistent SQLite WORM Ledger
try:
    import ebony_ledger as el
    assert el.record_entry(role="system", content="PRE_FLIGHT_SWEEP", model_core="DIAGNOSTIC"), "Insert failed"
    entries = el.get_recent_entries(limit=1)
    assert len(entries) > 0 and entries[0][3] == "PRE_FLIGHT_SWEEP"
    print("[+] 3. AUDIT LEDGER: SQLite Write/Read Verified.")
except Exception as e:
    print(f"[-] 3. AUDIT LEDGER FAULT: {e}")
    sys.exit(1)

# Check 4: SCADA Telemetry Engine
try:
    import ebony_scada_poll as esp
    metrics = esp.poll_system_metrics()
    assert metrics.get("status") == "NOMINAL"
    print(f"[+] 4. SCADA POLLING: Nominal ({metrics.get('node')} | {metrics.get('disk_free_gb')} GB Free).")
except Exception as e:
    print(f"[-] 4. SCADA POLLING FAULT: {e}")
    sys.exit(1)

# Check 5: Autonomous Agent Swarm Triad
try:
    import ebony_agent_swarm as eas
    sweep = eas.dispatch_swarm_task("all")
    assert "AGENT_ALPHA_RECON" in sweep and "AGENT_BETA_SEC" in sweep and "AGENT_GAMMA_ANALYST" in sweep
    print("[+] 5. AGENT SWARM: Triad Sweep Verified.")
except Exception as e:
    print(f"[-] 5. AGENT SWARM FAULT: {e}")
    sys.exit(1)

# Check 6: Modular Bridge Routing
try:
    from ebony_bridge import route_matrix_command
    scada_res = route_matrix_command("GAMMA_SCADA")
    assert "GAMMA_SCADA_TELEMETRY" in scada_res
    print("[+] 6. BRIDGE ROUTER: Subsystem Dispatch Verified.")
except Exception as e:
    print(f"[-] 6. BRIDGE ROUTER FAULT: {e}")
    sys.exit(1)

print("=" * 60)
print("[+] ALL 6 CORE DEMONSTRATION PILLARS VERIFIED 100% OPERATIONAL")
print("=" * 60)
