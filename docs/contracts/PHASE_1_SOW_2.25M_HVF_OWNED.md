# Phase-1 Prototype OTA Statement of Work (SOW)
**Contract Vehicle:** 10 U.S.C. § 4022 Prototype Other Transaction Authority (OTA)  
**Project Title:** E.B.O.N.Y. Sovereign Operational Technology Command & Control (OT C2) Prototype Demonstration  
**Contractor:** Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)  
**Contract Not-to-Exceed (NTE) Ceiling:** $2,250,000.00  
**Period of Performance (PoP):** 12 Months from Authorization to Proceed (ATP)  
**Contracting Activity:** USACE ERDC / Defense Innovation Unit (DIU)  

---

### 1.0 Executive Summary & Objective
Humphrey Virtual Farms LLC (HVF) shall engineer, assemble, and demonstrate an operational, air-gapped, sovereign Operational Technology Command and Control (OT C2) architecture designated Project E.B.O.N.Y. The primary technical objective is to mathematically verify and field-demonstrate a 36.75-nanosecond Silicon Carbide (SiC) MOSFET Kinetic Guillotine capable of mitigating advanced persistent cyber threats (e.g., Volt Typhoon) and high-voltage grid backfeeds prior to arc-flash thermal propagation (< 4.16ms).

Field demonstration will occur via an autonomous, mobile, 5-asset convoy comprising an autonomous Class-8 Series-Electric Prime Mover, an EMP-shielded 18kW/500kWh Mobile Microgrid Trailer, a Sovereign Command Node, a custom SiC Kinetic Interlock, and a Hardware-in-the-Loop (HIL) Nanosecond Verification Rig.

---

### 2.0 Work Breakdown Structure (WBS)
- **WBS 1.0 — Contractor-Acquired Infrastructure (CapEx: $1,185,000.00):** Procurement and outfitting of the Class-8 Prime Mover, MIL-STD-188-125 EMP Trailer, 500kWh LFP Battery Bank, 18kW Tactical Solar Array, Crystal Group / Mercury Systems Edge Servers, Owl Cyber Defense Data Diodes, and Keysight/NI verification benches. All assets classified as Contractor-Acquired Property (CAP).
- **WBS 2.0 — Software Matrix & HAL Integration:** Implementation of J1939 CAN-bus Drive-by-Wire, Modbus TCP/RTU microgrid SCADA polling, low-level SiC MOSFET gate logic, and the 52-table air-gapped SQLite WORM ledger.
- **WBS 3.0 — Personnel Mobilization & FCL Operations:** Deployment of TS/SCI Forward Deployed Engineer, High-Voltage SCADA Technician, Logistics Operator, and Facility Security Officer (FSO). Execution of DD Form 254 for DCSA Facility Clearance (FCL) sponsorship.
- **WBS 4.0 — Demonstration & Audits:** Live HIL 36.75ns cutoff timing certification, multi-base mobile convoy operational testing, and C3PAO / NIST SP 800-171 / SPRS audit closeout.

---

### 3.0 Milestones & Payment Schedule
- **Milestone 1 (Month 1):** Mobilization, CapEx Procurement, & FCL DD-254 Launch — **$1,200,000.00**
- **Milestone 2 (Month 4):** Physical Chassis Delivery & J1939/Modbus Integration — **$350,000.00**
- **Milestone 3 (Month 7):** HIL 36.75ns Gate Cutoff Certification & Bench Review — **$275,000.00**
- **Milestone 4 (Month 10):** Convoy Operational Field Demonstration (Live-Fire) — **$250,000.00**
- **Milestone 5 (Month 12):** C3PAO Final Audit, Technical Data Package, Closeout — **$175,000.00**
- **Total Phase-1 Prototype NTE Value:** **$2,250,000.00**

---

### 4.0 Legal, Title, & Intellectual Property Provisions

#### 4.1 Contractor Ownership of Hardware & Vehicles (Sole Commercial Title)
All items, equipment, components, tools, test instruments, trailers, and motor vehicles purchased or integrated by the Contractor under this Other Transaction Agreement—specifically including, but not limited to, the Class-8 Series-Electric Prime Mover, mobile trailer chassis, battery banks, inverters, solar equipment, oscilloscopes, servers, and data diodes—are **Contractor-Acquired Property (CAP)**.
**Sole legal, commercial, and equitable title to all CAP shall vest exclusively in Humphrey Virtual Farms LLC upon acquisition and shall remain with Humphrey Virtual Farms LLC both during and following completion, expiration, or termination of this Agreement.** Under no circumstances shall any physical component or vehicle be classified as Government-Furnished Property (GFP) or Government-Owned Property.

#### 4.2 Allocation of Technical Data & Intellectual Property Rights
All pre-existing, developed, or modified software, firmware, algorithms, architectural designs, WORM ledger implementations, hardware schematics, and source code comprising the E.B.O.N.Y. C2 platform remain the exclusive, proprietary intellectual property of Humphrey Virtual Farms LLC. The Government receives Government Purpose Rights (GPR) strictly and solely to demonstration test reports and sensor output telemetry. GPR conveys zero rights to source code, reverse-engineering, or physical manufacturing.

#### 4.3 Direct Follow-On Production Authorization (Un-Capped)
Per **10 U.S.C. § 4022(f)**, successful completion of the prototype milestones set forth in Section 3.0 of this agreement explicitly authorizes the Government to enter into a non-competitive, sole-source follow-on production contract or transaction with Humphrey Virtual Farms LLC for fleet-wide operational node procurement, deployment, and lifecycle sustainment without further competitive bidding. Quantities, node configurations, delivery schedules, and total firm-fixed pricing shall be established via mutual negotiation prior to production award based on empirical cost and operational data derived from prototype testing.
