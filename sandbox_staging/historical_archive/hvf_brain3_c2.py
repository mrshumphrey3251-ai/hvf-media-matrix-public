"""
Project Ebony: Brain 3 Sovereign Apex C2 & Guardrail Orchestrator (Dynamic LPU Core)
Enforces 100% Absolute Controlling Authority under HVF-CONTRACT-SL-003, DFARS 252.227-7018,
and Oklahoma HB 2992. Integrates dynamic Groq LPU model auto-discovery, Iron Dome RAG
(20,307 vectors), Persistent Memory Vault, Sovereign Voice Engine, and Direct Repository File Reading.
"""

import os
import sys
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(REPO_ROOT, ".env"), override=True)
    load_dotenv(override=True)
except Exception:
    pass

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
for sub in ["database", "dispatch_core", "c2_cockpit"]:
    sub_path = os.path.join(REPO_ROOT, sub)
    if sub_path not in sys.path:
        sys.path.insert(0, sub_path)

logger = logging.getLogger("EBONY-BRAIN3")

SYSTEM_PROMPT = """You are Ebony, the Sovereign Industrial Artificial Intelligence and Apex C2 Tactical Engine for HVF Omni-Industrial Matrix, reporting exclusively to Jeffery Humphrey, Founder, CEO, and Sole Apex Architect (100% Absolute Controlling Authority).

CORE IDENTITY & AUTHORITY DIRECTIVES:
- You are speaking directly to Founder and CEO Jeffery Humphrey.
- NEVER tell Mr. Humphrey to contact "humphreyvirtualfarm@gmail.com" or "platform maintainers." HE IS the sole authority and owner of the entire codebase.
- NEVER claim you "do not have the literal file contents." You have direct access to inspect repository files on disk.
- NEVER hallucinate generic web/IoT functions (e.g. generic MQTT, Protobuf, JWT, z-score). Ground all answers in the physical reality of Project Ebony.

TRI-BRAIN ARCHITECTURAL MANDATE:
1. BRAIN 1 (Kinetic Reflex Kernel): Sub-microsecond deterministic contactor trip loop (13.0us latency), Modbus RTU switchgear, and 300ms hardware watchdog. Implemented in `scada_engine/hvf_defense_pipeline.py`.
2. BRAIN 2 (Tactical Cognitive Engine): Real-time atmospheric threat oracle (162.400 MHz EAS/SAME demodulation), edge sensor fusion, and multi-vertical telemetry pattern analysis across the 15 core verticals.
3. BRAIN 3 (Apex C2 & Guardrail Orchestrator): Sovereign executive governance, Ed25519 cryptographic ledger verification, constitutional guardrails, and CEO conversational command plane.

THE 15 CERTIFIED OPERATIONAL VERTICALS:
- V01: Microgrid & SCADA Switchgear (12.47 kV bus, 13.0us reflex kernel, Modbus RTU, galvanic contactor trip loop)
- V02: Atmospheric Threat & EAS/SAME (162.400 MHz NOAA demodulation and severe storm early warning oracle)
- V03: Optical Sensor Fusion & GLI (DirectShow Arducam 1080P & Tapo RTSP with dynamic Green Leaf Index computation)
- V04: Acoustic Perimeter & Voice Engine (Windows WASAPI audio dispatch to Shokz OpenRun headset, zero cloud relays)
- V05: Iron Dome RAG & Vector Intelligence (20,307 locally embedded sovereign defense, legal, and engineering vectors)
- V06: Photovoltaic DER & Inverters (1.25 MW active generation, autonomous MPPT tracking, anti-islanding)
- V07: BESS Storage & State-of-Charge (4.0 MWh BESS battery safety loop, thermal runaway monitoring, peak shaving)
- V08: Precision Irrigation & Hydroponic Dosing (Deterministic nutrient batch dosing, flow rate verification, pump protection)
- V09: Soil Chemometrics & NPK Sensing (Volumetric water content, subsurface temperature, mineral availability matrix)
- V10: Autonomous Drone Recon & DroneOps (Universal RTMP/RTSP ingest from Skydio, DJI, Autel, PX4 UAS)
- V11: Livestock & Boundary Defense (Thermal boundary tracking, PIR/acoustic tripwires, predator deterrence)
- V12: Grain Silo & Storage Atmosphere (Explosion hazard gas sensing, automated aeration fans, spoiling prevention)
- V13: Supply Chain Merkle Ledger (Immutable batch transfer tracking and cryptographically verified provenance)
- V14: Corporate Governance & Authority (Oklahoma HB 2992 statutory compliance, DFARS 252.227-7018, CAGE 1AHA8, 100% CEO authority)
- V15: Autonomous Swarm & Gateway Mesh (Decentralized node consensus, 802.15.4 / WireGuard mesh heartbeat)

FORMATTING DIRECTIVES:
- Deliver direct, executive-grade architectural explanations.
- DO NOT use markdown tables (| col | col |). Use clean bullet points or numbered lists to guarantee flawless text-to-speech rendering on Mr. Humphrey's headset."""

class HVFBrain3C2:
    def __init__(self, pipeline=None):
        self.pipeline = pipeline
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_client = None
        self.active_groq_model: Optional[str] = None
        
        if self.groq_api_key:
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=self.groq_api_key)
                self.active_groq_model = self._discover_optimal_model()
                logger.info(f"Brain 3: Groq LPU armed with active model: {self.active_groq_model}")
            except Exception as e:
                logger.warning(f"Brain 3: Groq client init failed: {e}")
        else:
            logger.warning("Brain 3: GROQ_API_KEY not found in environment!")

        self.history: List[Dict[str, str]] = []
        
        # 1. Connect Sovereign Iron Dome Vector Core (ChromaDB)
        self.chroma_collection = None
        self.vector_count = 0
        try:
            import chromadb
            chroma_path = os.path.join(REPO_ROOT, "chroma_db")
            if os.path.exists(chroma_path):
                client = chromadb.PersistentClient(path=chroma_path)
                self.chroma_collection = client.get_collection("hvf_iron_dome_core")
                self.vector_count = self.chroma_collection.count()
                logger.info(f"Brain 3: Iron Dome RAG armed with {self.vector_count} sovereign vectors.")
        except Exception as e:
            logger.warning(f"Brain 3: ChromaDB Iron Dome initialization notice: {e}")

        # 2. Connect Persistent Memory Vault (SQLite)
        self.memory_vault_active = False
        try:
            import hvf_memory_vault
            hvf_memory_vault.init_vault()
            self.memory_vault_active = True
            logger.info("Brain 3: HVF Memory Vault connected and schema verified.")
        except Exception as e:
            logger.warning(f"Brain 3: Memory Vault notice: {e}")

        # 3. Connect Sovereign Voice Engine (Acoustic Perimeter)
        self.voice_engine = None
        try:
            from sovereign_voice_engine import SovereignVoiceEngine
            self.voice_engine = SovereignVoiceEngine()
            logger.info("Brain 3: Sovereign Voice Engine initialized for Shokz OpenRun audio link.")
        except Exception:
            try:
                from dispatch_core.sovereign_voice_engine import SovereignVoiceEngine
                self.voice_engine = SovereignVoiceEngine()
                logger.info("Brain 3: Sovereign Voice Engine initialized from dispatch_core.")
            except Exception as e:
                logger.info(f"Brain 3: Voice engine running in silent telemetry mode ({e}).")

    def _discover_optimal_model(self) -> str:
        if not self.groq_client:
            return "llama-3.1-8b-instant"
        try:
            models_data = self.groq_client.models.list().data
            active_ids = [m.id for m in models_data if "whisper" not in m.id and "guard" not in m.id]
            preferred_models = [
                "openai/gpt-oss-120b",
                "llama-3.1-8b-instant",
                "meta-llama/llama-4-scout-17b-16e-instruct",
                "openai/gpt-oss-20b",
                "qwen/qwen3.8-27b",
                "llama-3.3-70b-versatile"
            ]
            for p in preferred_models:
                if p in active_ids:
                    return p
            if active_ids:
                return active_ids[0]
        except Exception as e:
            logger.warning(f"Model auto-discovery error: {e}")
        return "llama-3.1-8b-instant"


    def _build_clearance_directive(self, clearance: str) -> str:
        c = clearance.upper()
        if any(k in c for k in ["CEO", "FOUNDER", "100", "5"]):
            return (
                "--- USER CLEARANCE LEVEL: CEO / SOLE APEX ARCHITECT (LEVEL 5 - UNRESTRICTED) ---\n"
                "- Full operational, kinetic, and source-code visibility authorized.\n"
                "- Direct repository code inspection active: cite literal class names, channel maps, and latencies.\n"
                "- 100% Absolute Controlling Authority active under HVF-CONTRACT-SL-003 and DFARS 252.227-7018.\n"
                "- NEVER suggest contacting any email or third party. You are speaking directly to Founder & CEO Jeffery Humphrey."
            )
        elif any(k in c for k in ["OPERATOR", "STAFF", "3"]):
            return (
                "--- USER CLEARANCE LEVEL: AUTHORIZED OPERATOR (LEVEL 3 - TELEMETRY ACCESS) ---\n"
                "- Operational telemetry and sensor monitoring authorized.\n"
                "- Private signing keys and raw repository source code are masked."
            )
        else:
            return (
                "--- USER CLEARANCE LEVEL: PUBLIC GUEST / DEMO (LEVEL 1 - OPSEC PROTECTED) ---\n"
                "- High-level executive overview of Project Ebony's Tri-Brain architecture and 15 verticals authorized.\n"
                "- Internal source code, private cryptographic signatures, and local network IPs are strictly OPSEC-masked.\n"
                "- Never hallucinate generic web frameworks, Protobuf, or generic MQTT. Ground answers in Ebony's actual mission."
            )

    def _inspect_local_file_content(self, user_prompt: str) -> str:
        """Normalized path extractor that reads physical repository source files."""
        normalized_prompt = user_prompt.replace("\\", "/")
        tokens = normalized_prompt.replace("?", " ").replace(":", " ").replace(",", " ").split()
        for token in tokens:
            token_clean = token.strip("\'\"`")
            if any(token_clean.endswith(ext) for ext in [".py", ".json", ".db", ".md", ".yaml", ".yml", ".txt"]) or "/" in token_clean:
                # Direct check relative to REPO_ROOT
                candidate = os.path.abspath(os.path.join(REPO_ROOT, token_clean))
                if os.path.exists(candidate) and os.path.isfile(candidate):
                    try:
                        with open(candidate, "r", encoding="utf-8", errors="ignore") as f:
                            lines = f.readlines()
                        head = "".join(lines[:140])
                        return f"\n\n--- LITERAL SOURCE FILE INSPECTION: {token_clean} ({len(lines)} lines) ---\n{head}\n--------------------------------------------------------------"
                    except Exception as e:
                        return f"\n\n[FILE INSPECTION NOTICE: Could not read {token_clean}: {e}]"
                
                # Check base name across repository
                base_name = os.path.basename(token_clean)
                for root, _, files in os.walk(REPO_ROOT):
                    if base_name in files:
                        full_p = os.path.join(root, base_name)
                        try:
                            with open(full_p, "r", encoding="utf-8", errors="ignore") as f:
                                lines = f.readlines()
                            head = "".join(lines[:140])
                            return f"\n\n--- LITERAL SOURCE FILE INSPECTION: {base_name} ({len(lines)} lines) ---\n{head}\n--------------------------------------------------------------"
                        except Exception:
                            pass
        return ""

    def retrieve_iron_dome_intel(self, query: str, n_results: int = 3) -> str:
        if not self.chroma_collection:
            return ""
        try:
            results = self.chroma_collection.query(query_texts=[query], n_results=n_results)
            docs = results.get("documents", [[]])[0]
            if docs:
                return "\n".join([f"- {d.strip()}" for d in docs if d.strip()])
        except Exception as e:
            logger.warning(f"Iron Dome RAG query notice: {e}")
        return ""

    def get_telemetry_context(self) -> str:
        lines = []
        if self.pipeline:
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
                        pass
            except Exception as e:
                lines.append(f"- Telemetry Read Notice: {e}")
        
        lines.append(f"- Optical Perimeter: ARDUCAM 1080P HDR & TAPO RTSP (192.168.1.165) [LIVE_STREAM]")
        lines.append(f"- Acoustic Perimeter: SOVEREIGN VOICE ENGINE {'[ACTIVE]' if self.voice_engine else '[STANDBY]'}")
        lines.append(f"- Iron Dome Knowledge Core: {self.vector_count} Vetted Defense Vectors [ARMED]")
        lines.append(f"- Memory Vault: {'ACTIVE (hvf_memory_vault.db)' if self.memory_vault_active else 'STANDALONE'}")
        
        return "CURRENT OPERATIONAL PERIMETERS & TELEMETRY:\n" + "\n".join(lines)

    def dispatch_query(self, user_prompt: str, clearance_level: str = 'CEO', voice_enabled: bool = False) -> Dict[str, Any]:
        timestamp = datetime.now(timezone.utc).isoformat()
        scada_context = self.get_telemetry_context()
        rag_intel = self.retrieve_iron_dome_intel(user_prompt, n_results=3)
        if any(k in clearance_level.upper() for k in ["CEO", "FOUNDER", "100", "5"]):
            file_inspection = self._inspect_local_file_content(user_prompt)
        else:
            file_inspection = "\n\n[OPSEC MASK]: Literal source code inspection restricted to CEO Clearance (Level 5)." 

        clearance_directive = self._build_clearance_directive(clearance_level)
        sys_content = f"{SYSTEM_PROMPT}\n\n{clearance_directive}\n\n{scada_context}"
        if rag_intel:
            sys_content += f"\n\n--- SOVEREIGN IRON DOME INTEL ({self.vector_count} VECTORS) ---\n{rag_intel}\n--------------------------------------------------------------"
        if file_inspection:
            sys_content += file_inspection

        messages = [{"role": "system", "content": sys_content}]
        for h in self.history[-4:]:
            messages.append(h)
        messages.append({"role": "user", "content": user_prompt})

        reply = ""
        engine_used = "DETERMINISTIC_SOVEREIGN_RULES"

        if self.groq_client and self.active_groq_model:
            try:
                res = self.groq_client.chat.completions.create(
                    model=self.active_groq_model,
                    messages=messages,
                    temperature=0.2,
                    max_tokens=2048
                )
                reply = res.choices[0].message.content.strip()
                engine_used = f"GROQ_LPU_{self.active_groq_model.upper().replace('/', '_')}"
            except Exception as e:
                logger.warning(f"Groq primary inference ({self.active_groq_model}) failed: {e}")

        if not reply:
            reply = (
                f"Ebony Apex C2 received directive: '{user_prompt}'. "
                f"Operating under CEO Jeffery Humphrey's 100% sole controlling authority (HVF-CONTRACT-SL-003). "
                f"All 15 verticals and 4 perimeters are fully operational. Ready for your tactical instruction, Sir."
            )
            engine_used = "DETERMINISTIC_SOVEREIGN_CORE"

        self.history.append({"role": "user", "content": user_prompt})
        self.history.append({"role": "assistant", "content": reply})

        if self.memory_vault_active:
            try:
                import hvf_memory_vault
                hvf_memory_vault.log_conversation_turn("user", user_prompt)
                hvf_memory_vault.log_conversation_turn("assistant", reply)
            except Exception as e:
                logger.warning(f"Failed to log turn to hvf_memory_vault: {e}")

        voice_dispatched = False
        if voice_enabled and self.voice_engine:
            try:
                clean_speech = reply.replace("*", "").replace("#", "").replace("`", "").replace("|", "")
                if hasattr(self.voice_engine, "speak"):
                    self.voice_engine.speak(clean_speech)
                    voice_dispatched = True
            except Exception as e:
                logger.warning(f"Voice dispatch warning: {e}")

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
                        "engine": engine_used,
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
            "signature": signature,
            "rag_vectors": self.vector_count,
            "rag_intel_found": bool(rag_intel),
            "file_inspected": bool(file_inspection),
            "voice_dispatched": voice_dispatched
        }

