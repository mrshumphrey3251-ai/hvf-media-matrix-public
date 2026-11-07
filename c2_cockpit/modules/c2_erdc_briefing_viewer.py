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
        "segment": "Segment 2: Hardware Air-Gap & 7,500-Mile Convoy (10:00 - 20:00)",
        "bullets": [
            "Energy Reservoir: 950 Gallons total multi-fuel (300 gal dual tractor tanks + 650 gal trailer belly cell).",
            "Prime Generation: 150kW underbelly multi-fuel micro-turbine burning JP-8, F-24, or diesel.",
            "Option A: Powered Trailer eAxle eliminates deadweight drag and recaptures dynamic braking energy.",
            "Option C: Solid-state Exhaust Thermoelectric Generator (TEG) returns 6.5kW waste-heat electricity.",
            "Mission Envelope: Over 110 continuous rolling hours (LA -> NY -> LA -> DC) without refueling or charging."
        ],
        "metrics": "Continuous Range: ~7,500 Miles | Fuel: 950 Gal JP-8/Diesel | Stops Required: ZERO"
    },
    {
        "num": "6/9",
        "title": "SOVEREIGN EXPEDITIONARY MICROGRID & LOW-OBSERVABLE SOLAR",
        "segment": "Segment 2: Hardware Air-Gap & 7,500-Mile Convoy (10:00 - 20:00)",
        "bullets": [
            "Storage Bank: 500 kWh NDAA-compliant KORE Power LFP battery bank (NDAA Section 889 compliant).",
            "Tactical Solar Canopy: 18kW deployable non-specular, micro-textured matte ETFE solar array.",
            "Counter-ISR Protection: Specular reflectance < 1.5% at 60°; zero glint/glare against aerial EO/IR drones.",
            "Camouflage Net Interlock: Perimeter mechanical coupling with ULCANS radar-scattering/transparent garnish.",
            "Base Support Endurance: Powers Tier-1 nodes (TOCs, FSUs, radars) for 30+ days off-grid."
        ],
        "metrics": "Microgrid Export: 480V 3-Phase (300kW Surge) | Solar: 18kW Low-Observable ETFE | Duration: 30+ Days"
    },
    {
        "num": "7/9",
        "title": "COMMERCIAL TITLE RETENTION & DFARS IP PROTECTION",
        "segment": "Segment 3: Contracting & Phase-1 Milestones (20:00 - 30:00)",
        "bullets": [
            "Contractor-Acquired Property: Humphrey Virtual Farms LLC retains 100% commercial title to prime mover & trailer.",
            "Statutory Exemption: 10 U.S.C. Section 4022 prototype OTA prevents government title seizure.",
            "IP Rights Protection: 100% DFARS 252.227-7018 Background IP retained across all code and firmware.",
            "Commercial Freedom: Full statutory authorization to market hybrid platform to commercial freight carriers.",
            "Government License: Government Purpose Rights (GPR) strictly limited to defense testing and evaluation."
        ],
        "metrics": "Asset Ownership: 100% HVF Commercial Title | IP Retained: DFARS 252.227-7018 Background"
    },
    {
        "num": "8/9",
        "title": "12-MONTH PHASE-1 PROTOTYPE OTA MILESTONES ($1.20M - $1.485M)",
        "segment": "Segment 3: Contracting & Phase-1 Milestones (20:00 - 30:00)",
        "bullets": [
            "Day 15-30: $150,000 Mobilization & Long-Lead Hardware Procurement Lock (Tractor, Cells, Turbine).",
            "Month 3: Subsystem Bench Assembly & 36.75ns SiC HIL Oscilloscope Electrical Verification.",
            "Month 6: Physical Trailer Underbelly Integration (150kW Turbine, 650-Gal Cell, eAxle Bogie).",
            "Month 9: Closed-Loop 7,500-Mile Transit Emulation & 480V Microgrid Black-Start Demonstration.",
            "Month 12: Joint USACE ERDC Live Base Demonstration at Vicksburg ERDC or Fort Leonard Wood."
        ],
        "metrics": "Execution Schedule: 12 Months | Day-15 Cashflow: $150,000 | Transition Authority: 10 U.S.C. 4022(f)"
    },
    {
        "num": "9/9",
        "title": "TRL 4 VERIFICATION AUDIT & CALL TO ACTION",
        "segment": "Segment 3: Contracting & Phase-1 Milestones (20:00 - 30:00)",
        "bullets": [
            "Zero Cloud Dependency: Runs 100% on 127.0.0.1 loopback with 0 external API dependencies.",
            "Unit Test Verification: 85 of 85 automated test suites passing (100.0% coverage).",
            "Red-Team Resilience: 17 of 17 adversarial attack vectors blocked with automatic tamper zeroization.",
            "Compliance: Full 110-control NIST SP 800-171 Rev 2 and NIST SP 800-82 Rev 2 architectural mapping.",
            "Action Requested: Direct Phase-1 Prototype OTA award via USACE ERDC Rolling BAA / DIU CSO."
        ],
        "metrics": "Test Suite Pass Rate: 85/85 (100%) | Red-Team Vectors Blocked: 17/17 | CAGE: 1AHA8"
    }
]

def render_slide(index: int) -> None:
    slide = SLIDES[index]
    width = 82
    print("\n" + "=" * width)
    print(f" PROJECT E.B.O.N.Y. v8.0.0 // USACE ERDC 30-MIN TECHNICAL BRIEFING   [SLIDE {slide['num']}]")
    print("=" * width)
    print(f" TIMING / FOCUS : {slide['segment']}")
    print(f" SLIDE TITLE    : {slide['title']}")
    print("-" * width)
    for b in slide["bullets"]:
        print(f"  * {b}")
    print("-" * width)
    print(f" TELEMETRY / DATA : {slide['metrics']}")
    print("=" * width)
    print(" [N]ext Slide  |  [P]revious Slide  |  [1-9] Direct Jump  |  [Q]uit to C2")

def run_briefing_console() -> None:
    current_idx = 0
    while True:
        render_slide(current_idx)
        try:
            choice = input("\nC2-BRIEFING> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting Briefing Viewer...")
            break

        if choice in ('q', 'quit', 'exit'):
            print("\n[+] Briefing session closed. Returning to C2 Console.")
            break
        elif choice in ('n', 'next', ''):
            if current_idx < len(SLIDES) - 1:
                current_idx += 1
            else:
                print("\n[!] Reached final slide (Slide 9/9).")
        elif choice in ('p', 'prev', 'back'):
            if current_idx > 0:
                current_idx -= 1
            else:
                print("\n[!] Already at Slide 1/9.")
        elif choice.isdigit() and 1 <= int(choice) <= 9:
            current_idx = int(choice) - 1
        else:
            print(f"\n[!] Invalid input '{choice}'. Enter N, P, 1-9, or Q.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--auto-test":
        print("[*] Running automated verification of 9 briefing slides...")
        for i in range(len(SLIDES)):
            assert "title" in SLIDES[i] and len(SLIDES[i]["bullets"]) == 5
        print(f"[+] All {len(SLIDES)} slides verified structurally compliant.")
        sys.exit(0)
    run_briefing_console()
