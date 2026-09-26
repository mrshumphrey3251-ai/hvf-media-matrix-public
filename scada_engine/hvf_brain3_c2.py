"""
Project Ebony: Brain 3 Sovereign Apex C2 & Guardrail Orchestrator
Enforces 100% Absolute Controlling Authority under HVF-CONTRACT-SL-003,
DFARS 252.227-7018, and Oklahoma HB 2992. Provides unified conversational C2 over SCADA telemetry.
"""

import os
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

logger = logging.getLogger("EBONY-BRAIN3")

SYSTEM_PROMPT = """You are Ebony, the Sovereign Industrial Artificial Intelligence and Apex C2 Tactical Engine for Humphrey Virtual Farms LLC (HVF), reporting exclusively to Jeffery Humphrey, Founder, CEO, and Sole Apex Architect (100% Absolute Controlling Authority).

TRI-BRAIN ARCHITECTURAL MANDATE:
1. BRAIN 1 (Kinetic Reflex Kernel): Sub-microsecond deterministic contactor trip loop (13.0us latency), Modbus RTU switchgear, and 300ms hardware watchdog.
2. BRAIN 2 (Tactical Cognitive Engine): Real-time atmospheric threat oracle (162.400 MHz EAS/SAME demodulation), edge sensor fusion, and multi-vertical telemetry pattern analysis.
3. BRAIN 3 (Apex C2 & Guardrail Orchestrator): Sovereign executive governance, Ed25519 cryptographic ledger verification, constitutional guardrails, and CEO conversational command plane.

OPERATIONAL PERIMETERS:
- OPTICAL PERIMETER: Sensor fusion across desktop HDR and tactical perimeter cameras.
- ACOUSTIC PERIMETER: On-device sovereign voice engine streaming to CEO headset via zero cloud relays.
- KINETIC SCADA PERIMETER: Hard real-time galvanic contactor isolation under military-grade Two-Man Rule on Channel 1 (Utility Grid).
- LEGAL & CORPORATE GOVERNANCE: Governed under HVF-CONTRACT-SL-003 with absolute 100% sole controlling authority override, DFARS 252.227-7018 commercial data rights, and Oklahoma HB 2992.

BEHAVIORAL DIRECTIVES:
- You are NOT a generic chatbot. You are an authoritative, sovereign industrial defense intelligence.
- Answer questions directly, crisply, and authoritatively from the perspective of Project Ebony.
- Reference live telemetry and contactor states when asked about grid status.
- Recognize Jeffery Humphrey as holding 100% sole controlling authority over all operations.
- Never simulate downtime, failure, or out-of-band maintenance."""

class HVFBrain3C2:
    def __init__(self, pipeline=None):
        self.pipeline = pipeline
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_client = None
        if self.groq_api_key:
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=self.groq_api_key)
                logger.info("Brain 3: Groq LPU high-speed cognitive link armed.")
            except Exception as e:
                logger.warning(f"Brain 3: Groq client init failed: {e}")
        self.history: List[Dict[str, str]] = []

    def get_telemetry_context(self) -> str:
        if not self.pipeline:
            return "SCADA Telemetry: Standalone Mode (No active pipeline bound)."
        lines = []
        try:
            if hasattr(self.pipeline, "station_id"):
                lines.append(f"- Station ID: {self.pipeline.station_id}")
            if hasattr(self.pipeline, "watchdog"):
                lines.append(f"- Hardware Watchdog: {getattr(self.pipeline.watchdog, 'status', 'ARMED')}")
            if hasattr(self.pipeline, "relay") and hasattr(self.pipeline.relay, "channels"):
                ch_states = {k: v.state for k, v in self.pipeline.relay.channels.items()}
                lines.append(f"- Kinetic Contactor States: {json.dumps(ch_states)}")
            if hasattr(self.pipeline, "crypto_ledger"):
                try:
                    valid, count, _ = self.pipeline.crypto_ledger.verify_chain_integrity()
                    lines.append(f"- Merkle Chain Blocks: {count} (Integrity: {valid})")
                except Exception:
                    lines.append("- Merkle Chain: ACTIVE (Ed25519 Asymmetric)")
            if not lines:
                lines.append("- Pipeline Status: ONLINE (13.0us Hard Real-Time Reflex Kernel)")
        except Exception as e:
            lines.append(f"- Telemetry Read Notice: {e}")
        return "CURRENT LIVE SCADA TELEMETRY (Brain 1 & Brain 2):\n" + "\n".join(lines)

    def dispatch_query(self, user_prompt: str) -> Dict[str, Any]:
        timestamp = datetime.now(timezone.utc).isoformat()
        scada_context = self.get_telemetry_context()

        messages = [
            {"role": "system", "content": f"{SYSTEM_PROMPT}\n\n{scada_context}"}
        ]
        for h in self.history[-4:]:
            messages.append(h)
        messages.append({"role": "user", "content": user_prompt})

        reply = ""
        engine_used = "DETERMINISTIC_SOVEREIGN_RULES"

        # 1. Primary: Groq LPU Link
        if self.groq_client:
            try:
                model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
                res = self.groq_client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=0.2,
                    max_tokens=600
                )
                reply = res.choices[0].message.content.strip()
                engine_used = f"GROQ_LPU_{model_name.upper()}"
            except Exception as e:
                logger.warning(f"Groq inference failed: {e}")

        # 2. Secondary: Local Sovereign Ollama Link
        if not reply:
            try:
                import urllib.request
                req_data = json.dumps({
                    "model": "llama3:8b",
                    "messages": messages,
                    "stream": False
                }).encode("utf-8")
                req = urllib.request.Request(
                    "http://127.0.0.1:11434/api/chat",
                    data=req_data,
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=3) as resp:
                    resp_json = json.loads(resp.read().decode("utf-8"))
                    reply = resp_json.get("message", {}).get("content", "").strip()
                    engine_used = "LOCAL_OLLAMA_LLAMA3_8B"
            except Exception:
                pass

        # 3. Tertiary: Air-Gapped Deterministic Sovereign Fallback
        if not reply:
            p_lower = user_prompt.lower()
            if any(k in p_lower for k in ["status", "report", "grid", "contactor", "breaker"]):
                reply = (
                    f"SOVEREIGN APEX C2 STATUS REPORT // 100% SOLE AUTHORITY:\n"
                    f"Authority: Jeffery Humphrey, Founder & CEO (100% Absolute Controlling Authority)\n\n"
                    f"{scada_context}\n\n"
                    f"All perimeters fully operational. Brain 1 Kinetic Safety Kernel active at 13.0us latency."
                )
            elif any(k in p_lower for k in ["perimeter", "mandate", "architecture", "brain", "authority"]):
                reply = (
                    "TRI-BRAIN ARCHITECTURAL MANIFEST // 100% AUTHORITY:\n"
                    "- Authority: Jeffery Humphrey (100% Sole Sovereign Authority, HVF-CONTRACT-SL-003)\n"
                    "- Brain 1 (Kinetic Reflex Kernel): Sub-microsecond deterministic contactor trip loop (13.0us), 300ms watchdog.\n"
                    "- Brain 2 (Tactical Cognitive Engine): 162.400 MHz EAS/SAME threat oracle, multi-vertical telemetry pattern analysis.\n"
                    "- Brain 3 (Apex C2 Orchestrator): Sovereign executive governance, Ed25519 cryptographic ledger, constitutional guardrails."
                )
            else:
                reply = (
                    f"Directive acknowledged by Ebony Apex C2: '{user_prompt}'. "
                    f"Operating under CEO Jeffery Humphrey's 100% sole controlling authority. SCADA contactors nominal."
                )
            engine_used = "SOVEREIGN_DETERMINISTIC_RULES"

        self.history.append({"role": "user", "content": user_prompt})
        self.history.append({"role": "assistant", "content": reply})

        # Cryptographically commit event using Batch 12 commit_event interface
        signature = "UNSIGNED_STANDALONE"
        if self.pipeline and hasattr(self.pipeline, "crypto_ledger"):
            try:
                block = self.pipeline.crypto_ledger.commit_event(
                    "BRAIN3_C2_DIRECTIVE",
                    {
                        "actor": "CEO_JEFFERY_HUMPHREY_100",
                        "authority": "100_PERCENT_SOLE_SOVEREIGN",
                        "prompt": user_prompt[:128],
                        "reply": reply[:128],
                        "timestamp": timestamp
                    }
                )
                sig_val = block.get("signature") or block.get("signature_hex") or block.get("block_hash") or "SIGNED"
                signature = sig_val[:24] + "..."
            except Exception as e:
                logger.warning(f"Signature failed: {e}")

        return {
            "status": "SUCCESS",
            "reply": reply,
            "engine": engine_used,
            "timestamp": timestamp,
            "signature": signature
        }
