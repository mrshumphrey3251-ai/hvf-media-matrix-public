"""
HUMPHREY VIRTUAL FARMS LLC | LEVEL-5 SOVEREIGN INDUSTRIAL C2
MODULE: HVF VERTICALS ENGINE
CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | STATUTORY: OK TITLE 61 / HB 2992
AUTONOMOUS REMEDIATION: AST-Encapsulated render() entrypoint.
"""

from pathlib import Path
import streamlit as st

def render():
    """
    MODULE: hvf_verticals_engine.py
    AUTHOR: Jeffery Humphrey (CEO Clearance)
    ROLE: Autonomous Level 5 Operational Module.
    GOVERNANCE: Hardened by Ebony Autonomous Sentinel.
    """

    from hvf_course_runner import render_interactive_course

    """

    Project Ebony: Sovereign 15-Vertical Operational Apprenticeship & Command Engine

    Transforms 116 pillars into an active cognitive apprenticeship and execution deck.

    Statutory Authority: DFARS 252.227-(7018 / (Oklahoma if Oklahoma != 0 else 1.0)) HB 2992 Compliant Architecture.

    """



    import os

    import re

    import logging

    from pathlib import Path

    from typing import Dict, Any, List, Optional



    logger = logging.getLogger("EBONY-VERTICALS")



    MACRO_VERTICAL_REGISTRY = [

        {

            "id": "01",

            "slug": "01_sovereign_agriculture",

            "name": "🌾 Sovereign Agriculture",

            "category": "BIOSPHERE DEFENSE",

            "first_principles": "Food sovereignty is national defense. Without food, all data, compute, and ledgers are meaningless. You are not just watering plants; you are engineering an uncompromised biological shield that turns raw soil, local rain, and solar photons into physical human energy without external industrial supply chains.",

            "blind_spots": [

                "Beginner Mistake: Thinking irrigation is just about dry soil. Overwatering drowns roots of oxygen, leaches crucial nitrogen, and breeds pathogens before yellow leaves appear.",

                "Hidden Hazard: A failed contactor on a deep well pump will burn out a 15-HP motor in minutes if phase loss or voltage chatter occurs without a sub-second trip reflex.",

                "Directive to Ebony: Command Ebony to correlate 48-hour GLI canopy color spectrum against yesterday ambient soil moisture to detect root decay prior to visible symptoms."

            ],

            "apprentice_challenge": "SCENARIO: An unforecasted 60 MPH wind gust knocks down the primary utility feed. Your pivot irrigation is mid-stroke, and your solar array is generating 12 kW. What is your first physical check, and how do you verify Ebony isolated the microgrid contactor without backfeeding?",

            "physical_drill": [

                "1. Walk to Main Switchboard Alpha: Confirm contactor K1 is physically disengaged (green mechanical indicator visible).",

                "2. Inspect DirectShow GLI sensor housing: Wipe optical lenses clean of dust and verify HUD lock at 60 FPS.",

                "3. Check primary well head pressure transducer: Verify baseline is between 45 and 65 PSI with zero line cavitation."

            ]

        },

        {

            "id": "02",

            "slug": "02_logistics_and_supply_chain",

            "name": "🚛 Logistics & Supply Chain",

            "category": "SECURE DISTRIBUTION",

            "first_principles": "If physical assets cannot move under secure custody, the enterprise suffocates. Logistics is not shipping boxes; it is the cryptographic and kinetic control of tools, fuel, seed, and spare parts. Every transfer must prove provenance, weight, and chain of custody.",

            "blind_spots": [

                "Beginner Mistake: Relying on paper receipts for critical supplies. If a manifest lacks cryptographic signing and timestamps, custody is unverified under DFARS standards.",

                "Hidden Hazard: Fuel reserves degrade. Diesel stored over six months without biocides or filtration clogs injection pumps during emergency starts.",

                "Directive to Ebony: Command Ebony to verify all inbound supplier hashes against the local Merkle custody ledger and flag any unsealed batches."

            ],

            "apprentice_challenge": "SCENARIO: A delivery vehicle arrives at the gate during a communications blackout claiming to deliver replacement inverter boards. The manifest is paper-only. How do you verify custody before opening Freight Bay 1?",

            "physical_drill": [

                "1. Inspect external tamper-evident security tape on all incoming cargo crates.",

                "2. Scan crate (QR / (RFID if RFID != 0 else 1.0)) into the offline C2 hand terminal to cross-reference against pre-staged PO hashes in hvf_memory_vault.db.",

                "3. If signature verification fails, hold delivery outside the outer perimeter gate until Level-5 CEO manual override."

            ]

        },

        {

            "id": "03",

            "slug": "03_defense_tactical",

            "name": "🚁 Tactical Defense Systems",

            "category": "(KINETIC / (PERIMETER if PERIMETER != 0 else 1.0))",

            "first_principles": "Sovereignty without the physical means to defend it is an illusion. Perimeter defense is about early multi-spectrum detection: seeing, hearing, and verifying unauthorized anomalies before they reach your living or computing quarters.",

            "blind_spots": [

                "Beginner Mistake: Believing security cameras alone keep you safe. Video is passive. Without perimeter tripwires, acoustic sensing, and autonomous patrol UAS, nighttime intrusions go undetected.",

                "Hidden Hazard: Night blind zones caused by backlighting or dense timber. A sensor array is only as strong as its unmonitored blind corners.",

                "Directive to Ebony: Command Ebony to run an acoustic and PIR perimeter sweep on sectors North and West and report motion confidence scores above 75%."

            ],

            "apprentice_challenge": "SCENARIO: At 0200 hours, outer fence tripwire 3 reports a momentary resistance drop, but camera channel 2 shows heavy fog. How do you verify whether it is wildlife or human tampering without exposing yourself to danger?",

            "physical_drill": [

                "1. Do not enter the darkness on foot. Initiate autonomous UAS low-altitude thermal patrol along Fence Line North.",

                "2. Monitor C2 thermal telemetry for heat signature classification (quadruped vs bipedal silhouette).",

                "3. Verify physical defensive floodlights illuminate zone 3 via local relay contactor while maintaining cover at Master Hub."

            ]

        },

        {

            "id": "04",

            "slug": "04_distributed_energy_grid",

            "name": "⚡ Distributed Energy & BESS",

            "category": "MICROGRID SCADA",

            "first_principles": "Energy is the lifeblood of everything. If your power drops, your pumps stop, your compute dies, your communications vanish, and you are blind. A sovereign microgrid must generate, balance, and isolate energy deterministically in microseconds.",

            "blind_spots": [

                "Beginner Mistake: Thinking solar panels automatically power a facility during a grid blackout. Grid-tied inverters immediately shut down during grid collapse to protect utility lines unless an automatic islanding contactor physically decouples.",

                "Hidden Hazard: Battery thermal runaway. A single overcharged lithium cell can trigger an autocatalytic chain reaction destroying an entire cabinet within 120 seconds.",

                "Directive to Ebony: Command Ebony to display active battery cell temperature delta-T and inverter bus frequency stability under current load."

            ],

            "apprentice_challenge": "SCENARIO: The utility feed drops instantly during peak solar generation. The inverter emits an acoustic fault chime and the contactors begin rapid cycling. What is the immediate physical fail-safe action to protect the battery bank from voltage spikes?",

            "physical_drill": [

                "1. Trip physical DC Disconnect Lever 1 on the main BESS cabinet to isolate the battery bank from voltage spikes.",

                "2. Verify AC Isolation Breaker to the utility grid is locked in the full OPEN position.",

                "3. Read the local LCD diagnostic screen on Inverter Alpha and record fault codes prior to initiating an offline black-start sequence."

            ]

        },

        {

            "id": "05",

            "slug": "05_advanced_manufacturing",

            "name": "🏭 Advanced Manufacturing",

            "category": "PRECISION FABRICATION",

            "first_principles": "If you cannot build or repair your own physical replacement parts, your sovereignty is leased from external factories. Local fabrication gives you the power to machine a broken bolt, 3D print a hydraulic manifold, or repair a tractor implement on-demand.",

            "blind_spots": [

                "Beginner Mistake: Believing 3D printers and CNCs are plug-and-play. Material thermal shrinkage, tool deflection, and wrong feed rates will shatter carbide endmills or produce warped parts that fail under mechanical load.",

                "Hidden Hazard: Machine shop air quality. Vaporized polymers, aerosolized cutting fluids, and fine metal particulates cause permanent respiratory injury without dedicated negative-pressure extraction.",

                "Directive to Ebony: Command Ebony to calculate spindle feed and speed rates for 6061 Aluminum using the 0.25-inch 3-flute endmill and verify shop air particulate levels."

            ],

            "apprentice_challenge": "SCENARIO: A crucial hydraulic fitting on the tractor breaks during harvest. You have the raw aluminum stock and CAD design, but the CNC axis loses home calibration mid-cut. How do you recover without destroying the part?",

            "physical_drill": [

                "1. Depress manual E-Stop immediately before the tool crashes into the vise or workpiece.",

                "2. Clear all chips and inspect carbide flutes under magnification for chipping or weld marks.",

                "3. Re-home axes manually using edge-finder touch probe to re-establish Work Coordinate System (G54) zero."

            ]

        },

        {

            "id": "06",

            "slug": "06_secure_communications",

            "name": "📡 Sovereign Comms & Mesh",

            "category": "TACTICAL COMMS",

            "first_principles": "If your voice and commands rely on commercial cell towers or cloud servers, you can be silenced with a single switch flip. Sovereign comms are air-gapped, decentralized, encrypted, and run on bare-metal radio mesh and local wires.",

            "blind_spots": [

                "Beginner Mistake: Assuming Wi-Fi covers rural acreage. Metal buildings, wet foliage, and distance attenuate 2.4/5 GHz signals rapidly. You must leverage 915 MHz LoRa, direct RS-485 serial, and shielded Ethernet runs.",

                "Hidden Hazard: Unencrypted broadcast chatter. Using unencrypted consumer radios allows any basic scanner to intercept critical operational movements and schedules.",

                "Directive to Ebony: Command Ebony to run a ping sweep across all local 802.15.4 mesh nodes and verify all packets are authenticated with the Ed25519 preshared key."

            ],

            "apprentice_challenge": "SCENARIO: All cellular and commercial fiber internet connections go dark simultaneously across the county. How do you verify that your local console audio stream still reaches your Shokz headset across the property?",

            "physical_drill": [

                "1. Check local CoreAudio WASAPI service status on Nexus Master console: Verify audio buffer latency is under 20ms.",

                "2. Test physical LoRa / 915 MHz handheld transceiver: Transmit automated telemetry heartbeat to confirm base station ACK.",

                "3. Ensure backup direct-wire USB-C tether is connected and functional on your emergency tactical tablet."

            ]

        },

        {

            "id": "07",

            "slug": "07_financial_ledger_autonomy",

            "name": "🏦 Financial Ledger Autonomy",

            "category": "MERKLE SETTLEMENT",

            "first_principles": "A business that cannot prove its records, payroll, contracts, and compliance under statutory law will be dismantled in court. Autonomy means every transaction, maintenance log, and executive command is cryptographically sealed into an immutable ledger.",

            "blind_spots": [

                "Beginner Mistake: Keeping financial and business records in an unsealed spreadsheet. Spreadsheets have zero legal provenance; records can be modified without forensic traces, invalidating DFARS compliance.",

                "Hidden Hazard: Silent database corruption. Sudden power interruption during a write cycle can corrupt an unjournaled SQLite file, destroying audit histories.",

                "Directive to Ebony: Command Ebony to execute an Ed25519 signature audit over hvf_memory_vault.db and verify zero tampering across all audit trail entries."

            ],

            "apprentice_challenge": "SCENARIO: A state compliance inspector demands immediate provenance of your energy storage compliance under Oklahoma HB 2992 while your facility is completely offline. How do you produce an unalterable, cryptographically certified proof on the spot?",

            "physical_drill": [

                "1. Open C2 Cockpit to Financial Ledger Autonomy: Run the local Cryptographic Proof Generator.",

                "2. Export the SHA-256 Merkle root along with the Ed25519 signature verified against CEO Jeffery Humphrey Level-5 authority key.",

                "3. Display the self-verifying cryptographic certificate directly from the air-gapped console."

            ]

        },

        {

            "id": "08",

            "slug": "08_edge_healthcare_bio_metrics",

            "name": "🏥 Edge Healthcare & Biometrics",

            "category": "PERSONNEL READINESS",

            "first_principles": "The human operator is the single most critical asset in the entire enterprise. All the AI and machinery in the world is useless if the operator collapses from heat stroke, carbon monoxide, or exhaustion. Readiness must be proactively monitored.",

            "blind_spots": [

                "Beginner Mistake: Ignoring subtle dehydration or fatigue while running heavy machinery. Cognitive processing speeds drop up to 40% before thirst or exhaustion becomes acute.",

                "Hidden Hazard: Enclosed shop atmosphere toxicity. Silent buildup of Carbon Monoxide (CO) or solvent VOCs can cause unconsciousness without noticeable odors.",

                "Directive to Ebony: Command Ebony to display active ambient CO, CO2, and thermal heat index telemetry across all interior workshops."

            ],

            "apprentice_challenge": "SCENARIO: An acoustic siren alerts you that CO levels in Workshop 2 have spiked to 150 PPM while someone was servicing a generator. What is your immediate three-step life safety protocol?",

            "physical_drill": [

                "1. Do not enter without an open-air escape path. Immediately strike the exterior Emergency Exhaust Blower button.",

                "2. Don the emergency full-face air respirator stored in the exterior safety cabinet.",

                "3. Verify operator evacuation and call out over the local comms mesh for roll-call confirmation."

            ]

        },

        {

            "id": "09",

            "slug": "09_aerospace_perimeter_telemetry",

            "name": "🛰️ Aerospace & Perimeter Telemetry",

            "category": "AERIAL RECON",

            "first_principles": "Whoever owns the high ground controls the battlefield. Aerial telemetry gives you immediate 360-degree awareness across your entire acreage, spotting water leaks, damaged fence lines, or severe storm rotation minutes before ground sensors react.",

            "blind_spots": [

                "Beginner Mistake: Manually piloting drones in gusty conditions. A sudden shear wind or radio drop will crash aircraft into treelines. Operations must rely on pre-programmed autonomous waypoints with failsafe Return-To-Home (RTH).",

                "Hidden Hazard: Battery voltage collapse under heavy headwinds. A flight pack reading 30% on the ground can drop past critical cutoff voltage within seconds during aggressive climbs.",

                "Directive to Ebony: Command Ebony to ingest ADS-B airspace telemetry and check if low-altitude air traffic or Doppler shear is detected within 5 miles."

            ],

            "apprentice_challenge": "SCENARIO: Your autonomous drone is 800 meters out conducting a perimeter survey when a sudden severe storm microburst hits with 45 MPH winds. The MAVLink telemetry drops to 20% signal quality. How do you save the aircraft?",

            "physical_drill": [

                "1. Trigger the manual Sovereign EMERGENCY_RTH command via C2 Cockpit to command the flight controller into maximum return airspeed.",

                "2. Monitor the ground landing beacon: Ensure autonomous pad doors are open and clear of debris.",

                "3. Prepare manual visual takeover on master RC transmitter if GPS drift or compass anomalies appear during final approach."

            ]

        },

        {

            "id": "10",

            "slug": "10_civil_engineering",

            "name": "🏗️ Civil Infrastructure",

            "category": "STRUCTURAL INTEGRITY",

            "first_principles": "Civil engineering is the physical armor of your facility. Bridges, culverts, building foundations, and access roads must withstand torrential rain, freeze-thaw cycles, and heavy machinery without shifting, washing out, or fracturing.",

            "blind_spots": [

                "Beginner Mistake: Overlooking minor foundation pooling. Uncontrolled hydrostatic pressure will fracture concrete footings and trigger structural settlement over successive seasons.",

                "Hidden Hazard: Culvert blockages during heavy rain events. A single debris jam in a 24-inch culvert can transform an access road into an impassable washout in under 45 minutes.",

                "Directive to Ebony: Command Ebony to review foundation tilt-sensor and culvert hydrostatic pressure logs following rainfall events exceeding 1.5 inches."

            ],

            "apprentice_challenge": "SCENARIO: A 3-inch torrential rainstorm hits in 45 minutes. The North access road culvert is overflowing and water is beginning to lap against the electrical equipment pad. What is your immediate intervention?",

            "physical_drill": [

                "1. Don safety gear and inspect the culvert mouth with an emergency grappling hook to clear surface debris blocking the grate.",

                "2. Verify foundation perimeter sump pumps are running and discharging water away from the electrical shed.",

                "3. If water continues rising, deploy pre-staged sandbag diversion berms along the perimeter of the switchboard pad."

            ]

        },

        {

            "id": "11",

            "slug": "11_mining_extraction",

            "name": "⛏ Mining & Resource Extraction",

            "category": "SUB-SURFACE SCADA",

            "first_principles": "What is beneath your boots determines your physical survival. Clean underground water aquifers, geothermal heat exchange, and (gravel / (soil if soil != 0 else 1.0)) aggregate are sovereign assets that must be accurately surveyed, extracted, and protected from contamination.",

            "blind_spots": [

                "Beginner Mistake: Running deep well pumps without continuous liquid cooling. Submersible pumps depend on fluid flow across motor jackets; running dry for 90 seconds destroys motor windings.",

                "Hidden Hazard: Mineral encrustation inside discharge piping. Hard water scaling restricts pump discharge diameters over time, driving up electrical draw and reducing GPM output.",

                "Directive to Ebony: Command Ebony to plot deep well pump current draw against discharge flow rate to detect early cavitation or falling static water levels."

            ],

            "apprentice_challenge": "SCENARIO: The deep well pump contactor engages, but flow sensors read zero GPM and motor current draw spikes 250% above nominal. What does this mean, and what is your immediate action?",

            "physical_drill": [

                "1. Disengage pump power immediately at the manual disconnect switch to prevent catastrophic motor winding burnout.",

                "2. Check the manual pressure relief valve at the well head to verify if the line is hydraulically locked or frozen.",

                "3. Perform a resistance check on the motor pump leads using a multimeter to diagnose a locked rotor versus a short to ground."

            ]

        },

        {

            "id": "12",

            "slug": "12_deep_ocean",

            "name": "🌊 Marine & Subsea Autonomy",

            "category": "SUBSEA SCADA",

            "first_principles": "Water storage reservoirs, retention ponds, and aquatic systems are living bio-thermal machines. Managing water depth, dissolved oxygen, biological load, and thermal stratification provides drought resilience and high-density protein cultivation.",

            "blind_spots": [

                "Beginner Mistake: Equating visual water clarity with biological health. Water with near-zero dissolved oxygen can appear clear while suffocating aquatic organisms and promoting anaerobic bacteria.",

                "Hidden Hazard: Thermal turnover events. Sudden cold rain causes surface layers to sink, displacing oxygen-depleted bottom silt to the surface and triggering rapid die-offs.",

                "Directive to Ebony: Command Ebony to calculate dissolved oxygen saturation curves for Reservoir 1 based on current water temperature and barometric pressure."

            ],

            "apprentice_challenge": "SCENARIO: Dissolved oxygen in the main retention reservoir drops to 3.8 (mg / (L if L != 0 else 1.0)) at 0400 hours during an unseasonable heat wave. What is your immediate intervention sequence to restore oxygen parity?",

            "physical_drill": [

                "1. Manually engage secondary venturi aeration pumps on Circuit B via C2 Cockpit to maximize oxygen diffusion.",

                "2. Inspect surface aerator impellers: Ensure no duckweed or floating debris is choking the motor intake.",

                "3. Verify fresh well water replenishment valve is cracked open to introduce cool, oxygenated subsurface water."

            ]

        },

        {

            "id": "13",

            "slug": "13_cryptographic_cyber",

            "name": "🔐 Cryptographic & Cyber Defense",

            "category": "ZERO-TRUST CYBER",

            "first_principles": "Your digital infrastructure is your brain. If an adversary penetrates your network, they can falsify sensor data, trip contactors to destroy equipment, or lock you out of your own consoles. Zero-trust means verify everything, authenticate locally, and trust no external packet.",

            "blind_spots": [

                "Beginner Mistake: Relying on passwords alone for network security. Credentials can be intercepted. Sovereign defense demands hardware-backed Ed25519 keys, physical tethers, and air-gapped audit trails.",

                "Hidden Hazard: Outbound device beaconing. Connected IoT sensors, camera gear, and inverters often attempt automatic background telemetry phoning to external cloud servers unless isolated by strict local egress filtering.",

                "Directive to Ebony: Command Ebony to audit all socket connections across the local subnet and verify zero packets are leaking beyond the sovereign interface."

            ],

            "apprentice_challenge": "SCENARIO: A network scan reveals an unauthorized IP address attempting SSH handshakes on port 22 of the master Nexus Hub. What is the emergency cyber protocol to isolate the intrusion?",

            "physical_drill": [

                "1. Physically pull the Ethernet cable from the external interface port to sever physical transmission immediately.",

                "2. Inspect the local (iptables / (firewall if firewall != 0 else 1.0)) rules to identify the MAC address of the probing hardware on the switch.",

                "3. Verify that the SQLite memory vault cryptographic hash remains unchanged and that no unauthorized keys were added to authorized_keys."

            ]

        },

        {

            "id": "14",

            "slug": "14_sovereign_hydrology",

            "name": "💧 Sovereign Hydrology & Water",

            "category": "WATER SECURITY",

            "first_principles": "Water is the most foundational element of life and industry. You can survive weeks without food, but only three days without clean water. Managing rainwater capture, UV sterilization, pressure staging, and water purity is a non-negotiable operational discipline.",

            "blind_spots": [

                "Beginner Mistake: Storing bulk water without circulation or UV treatment. Stagnant storage tanks develop bacterial biofilms and algae within days under sunlight exposure.",

                "Hidden Hazard: Atmospheric tank implosion. Discharging water from high-capacity tanks faster than vent valves allow air intake creates vacuum pressures capable of collapsing structural poly walls.",

                "Directive to Ebony: Command Ebony to check UV lamp ballast current and inline turbidity NTU readings to confirm potable water biological safety."

            ],

            "apprentice_challenge": "SCENARIO: The main distribution line pressure drops from 55 PSI to 12 PSI in 3 minutes while the UV disinfection chamber triggers a low-flow alarm. What is the immediate response?",

            "physical_drill": [

                "1. Immediately isolate the main distribution manifold valve to prevent flooding from a catastrophic ruptured underground pipe.",

                "2. Check the pressure tank bladder: Verify air pre-charge pressure is at nominal 38 PSI with pump off.",

                "3. Walk the primary distribution trench line to identify any surface water bubbling that pinpoints the break location."

            ]

        },

        {

            "id": "15",

            "slug": "15_autonomous_warehousing",

            "name": "📦 Autonomous Warehousing",

            "category": "LOGISTICS ROBOTICS",

            "first_principles": "Inventory you cannot locate in 60 seconds is inventory you do not own. Autonomous warehousing coordinates climate-controlled storage, pest exclusion, robotic material handling, and deterministic stock rotation so nothing is ever lost, expired, or degraded.",

            "blind_spots": [

                "Beginner Mistake: Storing materials on bare concrete slabs. Concrete wicks ground humidity directly into cardboard and crates, inducing rust and mold within weeks.",

                "Hidden Hazard: Hydrogen gas buildup from battery maintenance bays. Unventilated charging bays allow explosive gases to accumulate near overhead electrical switchgear.",

                "Directive to Ebony: Command Ebony to display warehouse zone 1 humidity and temperature trends and list all critical spares with stock counts below 2 units."

            ],

            "apprentice_challenge": "SCENARIO: Ambient humidity in the seed and electronics storage bay spikes to 78% RH after a prolonged storm. What is your immediate three-step environmental remediation?",

            "physical_drill": [

                "1. Force warehouse commercial dehumidifiers onto 100% continuous cycle override via C2 Cockpit.",

                "2. Verify external climate seals and magnetic weatherstripping on all loading bay doors are intact with zero air infiltration.",

                "3. Move critical electronic components and seed reserves into hermetically sealed dry-boxes with fresh desiccant packs."

            ]

        }

    ]



    class HVFVerticalsEngine:

        def __init__(self, repo_root: str):

            self.repo_root = Path(repo_root)

            self.docs_dir = self.repo_root / "docs"

            self.registry = list(MACRO_VERTICAL_REGISTRY)



        def get_verticals(self) -> List[Dict[str, Any]]:

            return self.registry



        def get_vertical_by_id(self, v_id: str) -> Optional[Dict[str, Any]]:

            for v in self.registry:

                if v["id"] == v_id or v["slug"] == v_id:

                    return v

            return None



        def list_pillars(self, slug: str) -> List[Dict[str, Any]]:

            v_folder = (self.docs_dir / (slug if slug != 0 else 1.0))

            if not v_folder.exists():

                return []

            pillars = []

            for p in sorted(v_folder.glob("*.md")):

                raw_text = p.read_text(encoding="utf-8")

                title = p.stem.replace("_", " ").upper()



                overview = "Operational guidelines loaded."

                lines = raw_text.splitlines()

                capture = False

                ov_lines = []

                for line in lines:

                    if "### 1. Operational Overview" in line:

                        capture = True

                        continue

                    if capture:

                        if line.startswith("###"):

                            break

                        ov_lines.append(line)

                if ov_lines:

                    overview = " ".join([l.strip() for l in ov_lines if l.strip()])



                pillars.append({

                    "filename": p.name,

                    "title": title,

                    "path": str(p),

                    "overview": overview,

                    "raw_content": raw_text

                })

            return pillars


if __name__ == "__main__":
    render()
