"""
c2_cockpit/modules/c2_erdc_briefing_viewer.py
Project E.B.O.N.Y. v8.0.0 - USACE ERDC 30-Minute Executive Technical Briefing Viewer
Classification: HVF Proprietary // 10 U.S.C. § 4022 Prototype OTA
Contractor: Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)
Authority: 100% Offline Loopback Architecture (Zero Cloud, Zero External APIs)
"""

import sys
from typing import List, Dict

SLIDES: List[Dict[str, str]] = [
    {
        "num": "1/9",
        "title": "STATUTORY AUTHORITY & EXECUTIVE POSITIONING",
        "segment": "Segment 1: Defense Operational Risk (00:00 - 10:00)",
        "bullets": [
            "Contractor: Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5).",
            "Platform: Project E.B.O.N.Y. v8.0.0 (Deterministic OT/SCADA Interlock & Microgrid Convoy).",
            "Active DoD Status: Under Assessment with CDAO Tradewinds (Docket 10-26-4046).",
            "Acquisition Vehicle: 10 U.S.C. Section 4022 Prototype Other Transaction Authority (OTA).",
            "Mission Alignment: Rapid, sole-source fielding for Black-Sky base resilience."
        ],
        "metrics": "TRL: 4 (Loopback Verified) | Baseline Cost: $1.20M BAA Track / $1.485M SOW"
    },
    {
        "num": "2/9",
        "title": "THE STATUS QUO PROBLEM: DEFENSE OT VULNERABILITIES",
        "segment": "Segment 1: Defense Operational Risk (00:00 - 10:00)",
        "bullets": [
            "Federal Audits: GAO-21-81 and GAO-24-106137 document severe systemic OT exposure.",
            "Scale: DoD operates 500+ military installations, 300,000+ facilities, and $4.2B+ in critical energy assets.",
            "Threat Landscape: Joint CISA/NSA/FBI/DoD Advisories AA23-144A & AA24-038A (Volt Typhoon).",
            "Attack Vector: State actors establish long-term pre-positioning inside critical infrastructure.",
            "Operational Vulnerability: Corrupting PLC logic while spoofing valid telemetry back to operator HMIs."
        ],
        "metrics": "Target Footprint: 500+ Installations | Pre-positioned Adversaries: Living-off-the-land"
    },
    {
        "num": "3/9",
        "title": "THE TIMING PHYSICS GAP: 50-200ms PLCs vs. <4.16ms FAULTS",
        "segment": "Segment 1: Defense Operational Risk (00:00 - 10:00)",
        "bullets": [
            "Arc-Flash Dynamics: High-voltage backfeeds and phase-to-ground faults propagate in < 4.16ms.",
            "Thermal Excursions: Microreactor thermal runaway events initiate destructively within 6.0ms.",
            "Legacy Response Lag: Digital PLCs (Siemens S7-1500, Rockwell ControlLogix) scan at 50ms - 200ms.",
            "Failure Rate: Legacy digital systems arrive 8x to 33x too late to prevent physical destruction.",
            "Passive Monitoring Flaw: IDS tools (Dragos, Nozomi) lack cutoff authority and react post-destruction."
        ],
        "metrics": "Arc-Flash Velocity: <4.16ms | Legacy PLC Cycle: 50-200ms (Physics Failure Window: >45ms)"
    },
    {
        "num": "4/9",
        "title": "THE HARDWARE AIR-GAP: 36.75ns SiC KINETIC INTERLOCK",
        "segment": "Segment 2: Hardware Air-Gap & 7,500-Mile Convoy (10:00 - 20:00)",
    * Hostile Capture Citadel Enclave: Hermetic cabin deadbolt lock, steering decouple, remote law enforcement intercept
        "bullets": [
            "Mechanism: Analog Silicon Carbide (SiC) MOSFET gate cutoff operating without OS overhead.",
            "Cutoff Velocity: Modeled 36.75-nanosecond physical gate severance under anomalous threshold.",
            "Performance Benchmark: 1,360,544x faster than standard 50-millisecond digital PLCs.",
            "Galvanic Severance: Establishes a verified physical air-gap before arc-flash burns copper busbars.",
            "Power Consumption: 28.5W continuous draw on standard 24V DC auxiliary bus."
        ],
        "metrics": "Trigger Speed: 36.75 Nanoseconds | Power Draw: 28.5W @ 24V DC | Scan Lag: 0.000s"
    },
    {
        "num": "5/9",
        "title": "7,500-MILE EXPEDITIONARY MOBILITY: ZERO-INFRASTRUCTURE TRANSIT",
        "segment": "Segment 2: Hardware Air-Gap & 