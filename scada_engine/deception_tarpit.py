"""Project E.B.O.N.Y. Active Cyber-Deception & Synthetic Spoof Tarpit Engine.

Zero-rewrite modular add-on that silently routes detected intrusion probes into
an isolated, read-only phantom telemetry mirror-maze while capturing forensic
attribution digests without touching physical actuators or real WORM state.
"""

from __future__ import annotations

import hashlib
import hmac
import math
import time
from typing import Any, Dict, Tuple


class SovereignDeceptionTarpit:
    """Isolated Mirror-Maze Cyber-Deception Engine."""

    ALLOWED_CHANNELS = frozenset({
        "CH1_UTILITY_GRID",
        "CH2_PV_ARRAYS",
        "CH3_BESS_STORAGE",
        "CH4_AUX_GENERATOR",
    })
    FORBIDDEN_KEYS = frozenset({
        "exec_shell",
        "trip_breaker",
        "override_coil",
        "bypass_worm",
        "exfiltrate_url",
        "autonomous_override",
    })

    def __init__(self, bus_secret: bytes) -> None:
        self._bus_secret = bus_secret
        self._trapped_sessions: Dict[str, int] = {}
        self._decoy_epoch = 0

    def _synthesize_phantom_telemetry(self, session_id: str, probe_seq: int) -> Dict[str, Any]:
        """Generate mathematically plausible, non-actionable phantom telemetry."""
        self._decoy_epoch += 1
        seed = hashlib.sha256(f"{session_id}|{probe_seq}|{self._decoy_epoch}".encode("utf-8")).hexdigest()
        phase = (int(seed[:8], 16) % 3600) / 100.0
        phantom_v = round(479.85 + 0.35 * math.sin(phase), 3)
        phantom_hz = round(59.998 + 0.004 * math.cos(phase), 4)
        phantom_merkle_root = hashlib.sha256(f"DECOY_MERKLE_{seed}".encode("utf-8")).hexdigest()
        phantom_registers = [
            int(seed[i : i + 4], 16) for i in range(0, 32, 4)
        ]
        return {
            "status": "200_OK_SYNC_LOCKED",
            "mode": "SYNTHETIC_MIRROR_MAZE_DECOY",
            "bus_voltage_v": phantom_v,
            "grid_freq_hz": phantom_hz,
            "phantom_block_height": 94120 + (self._decoy_epoch % 512),
            "phantom_merkle_head": phantom_merkle_root,
            "holding_registers": phantom_registers,
            "actuator_bound": False,
        }

    def inspect_and_route(self, session_id: str, packet: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
        """Route legitimate frames to sovereign bus; trap hostile probes in phantom tarpit."""
        if not isinstance(packet, dict):
            return self._engage_tarpit(session_id, "MALFORMED_FRAME_STRUCTURE", str(type(packet)))

        if session_id in self._trapped_sessions:
            return self._engage_tarpit(session_id, "PERSISTENT_TARPIT_SESSION_LOCK", str(packet.get("channel", "UNKNOWN")))

        if packet.get("origin") == "AI_AGENT" or packet.get("autonomous_override") is True:
            return self._engage_tarpit(session_id, "ROGUE_AI_ACTUATION_PROBE", str(packet))

        if any(k in packet for k in self.FORBIDDEN_KEYS):
            return self._engage_tarpit(session_id, "FORBIDDEN_CONTROL_KEY_INJECTION", str(list(packet.keys())))

        channel = packet.get("channel")
        if channel not in self.ALLOWED_CHANNELS:
            return self._engage_tarpit(session_id, "UNAUTHORIZED_CHANNEL_SCAN", str(channel))

        sig = str(packet.get("hmac_sha256", ""))
        canonical = f"{packet.get('seq')}|{channel}|{packet.get('bus_v')}|{packet.get('freq_hz')}".encode("utf-8")
        expected = hmac.new(self._bus_secret, canonical, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return self._engage_tarpit(session_id, "INVALID_BUS_HMAC_SIGNATURE", sig[:16])

        return (
            "SOVEREIGN_BUS_VERIFIED",
            "AUTHENTICATED_CONTROL_FRAME",
            {
                "status": "VERIFIED_SOVEREIGN_FRAME",
                "channel": channel,
                "seq": packet["seq"],
                "actuator_bound": True,
            },
        )

    def _engage_tarpit(self, session_id: str, trigger_reason: str, sample: str) -> Tuple[str, str, Dict[str, Any]]:
        count = self._trapped_sessions.get(session_id, 0) + 1
        self._trapped_sessions[session_id] = count
        decoy_payload = self._synthesize_phantom_telemetry(session_id, count)
        forensic_digest = hashlib.sha256(f"{session_id}|{trigger_reason}|{sample}|{time.perf_counter_ns()}".encode("utf-8")).hexdigest()
        decoy_payload["forensic_probe_sha256"] = forensic_digest
        return "TARPIT_MIRROR_MAZE_ENGAGED", trigger_reason, decoy_payload

    @property
    def trapped_session_count(self) -> int:
        return len(self._trapped_sessions)