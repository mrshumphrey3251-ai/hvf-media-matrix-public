# ⚡ E.B.O.N.Y. SOVEREIGN INDUSTRIAL COMMAND & CONTROL PLATFORM
## OPERATIONAL USAGE MANUAL, ARCHITECTURAL SPECIFICATION & STATUTORY LEGAL DISCLAIMER
**ENTITY:** Humphrey Virtual Farms LLC | **CAGE:** 1AHA8 | **UEI:** S1M4ENLHTDH5  
**HOST NODE SPECIFICATION:** Bare-Metal Edge (HVFNexus Architecture)  
**GOVERNING FRAMEWORK:** State of Oklahoma Title 61 & OK HB 2992 Commercial Enclave  
**DEFENSE CONTRACTING VEHICLE:** Tradewinds CDAO Docket 9-26-3703  
**DOCUMENT CLASSIFICATION:** Level-5 Sovereign Commercial Release // Rev. 2026.4  

---

### PART I: EXECUTIVE CHARTER & DATA SOVEREIGNTY MANDATE

#### 1.1 The Sovereign Compute Principle
E.B.O.N.Y. (Executive-Built Operations that Never-Yield) is an air-gapped, on-premise industrial command and intelligence platform. Unlike commercial software-as-a-service (SaaS) applications, E.B.O.N.Y. does not route user data, correspondence, telemetry, or cryptographic hashes through third-party multi-tenant cloud servers (e.g., AWS, Microsoft Azure, Google Cloud).

When installed, the host computer functions as an independent, decentralized, on-premise data center. All transactional logs, mailbox credentials, local neural models, and diagnostic streams remain in the exclusive physical custody of the subscriber.

#### 1.2 Statutory Oklahoma Authority
Humphrey Virtual Farms LLC operates under the sovereign industrial exemptions and public infrastructure resilience standards established by:
* **Oklahoma Statutes Title 61 (Public Buildings & Public Works):** Standards governing resilient public facility infrastructure, state procurement channels, and local defense asset mobilization.
* **Oklahoma House Bill 2992 (Certified Test Facility Framework):** Legal authority authorizing behind-the-meter (BTM) microgrid development, local power offload, and independent high-density compute testbed validation without Southwest Power Pool (SPP) transmission interconnect queue delays.
* **Federal Defense Ingress:** CAGE Code `1AHA8` and SAM.gov Unique Entity Identifier (UEI) `S1M4ENLHTDH5` recognized under Tradewinds CDAO Docket `9-26-3703`.

---

### PART II: FUNCTION-BY-FUNCTION OPERATIONAL GUIDE

#### 2.1 Zero-API Mailbox Authentication & Credential Ingestion
* **Functional Scope:** Ingests incoming correspondence and dispatches outbound executive responses over direct RFC Layer-7 network sockets without requiring Google Cloud Console projects, OAuth developer tokens, or third-party middleware (e.g., Zapier).
* **Network Binding:**
  * **Inbound Telemetry:** Secure IMAP via TLS/SSL (Port 993).
  * **Outbound Transmission:** Secure SMTP via TLS/SSL (Port 465 or Port 587).
* **Authentication Protocol:**
  * **Google Accounts / Workspace:** Requires a 16-character Google App Password generated under *Account Security > 2-Step Verification > App Passwords* labeled `EBONY`. Standard master account passwords will be rejected by Google's IMAP security gateway.
  * **Enterprise / State Accounts (`@ok.gov`):** Connects using standard agency credentials or authorized relay credentials on designated internal mail hosts (`mail.agency.ok.gov`).

#### 2.2 Sovereign Dispatch Deck & Tactical Threat Scrubber
* **Functional Scope:** Real-time communications triage, plain-text response authoring, and zero-trust inbound threat sanitization.
* **Inbound Threat Scrubber:**
  * Strips 100% of tracking pixels, malicious CSS payloads, JavaScript injection vectors, and obfuscated hyperlinks prior to displaying inbound email text.
  * Renders clean, sanitized plain text inside the executive transmission stepper.
* **Outbound Executive Dispatch:**
  * Provides a direct, non-repudiated message composer stamped with Humphrey Virtual Farms LLC CAGE `1AHA8` credentials.
  * Formats transmissions in strict RFC 5322 compliance.

#### 2.3 Executive Travel Autopilot & Background Daemon
* **Functional Scope:** Unattended 24/7 inbox management engineered specifically for executives in transit.
* **Daemon Execution (`daemon_autopilot.ps1`):**
  * Executes silent background sweeps on an automated 300-second (5-minute) cadence via an invisible Windows Script Host launcher (`launch_ebony_autopilot.vbs`).
  * Persists across machine reboots via Windows User Startup bindings without requiring elevated Administrator rights.
* **Autonomous Inbound Filtering & Noise Neutralization:**
  * Detects `List-Unsubscribe` and `Precedence: bulk` headers and filters commercial marketing bots, e-commerce notifications, and system alerts directly into `ARCHIVED_BULK` status without notifying the operator.
* **Self-Loop Circuit Breaker:**
  * Automatically inspects inbound sender headers against the active node mailbox and suppresses recursive auto-replies to prevent infinite SMTP ping-pong loops.
* **Executive Return Debrief Report:**
  * Summarizes mission totals upon return from travel: Total Ingested, Autonomously Resolved, Newsletters Filtered, and Priority Action Items Flagged.
  * Delivers a plain-English briefing directly on glass and can transmit the debrief to the executive's mobile device with one click (`📱 EMAIL DEBRIEF TO MY PHONE`).

#### 2.4 Priority Triage Queue & Response Inspector
* **Functional Scope:** Isolates high-consequence correspondence (State Grants, ODOT Infrastructure, Title 61 dockets, Executive Scheduling) from routine inquiries.
* **Operational Actions:**
  * **Inspect:** Read full inbound message bodies side-by-side with drafted executive responses without text truncation.
  * **Edit & Transmit:** Modify drafted responses in an interactive text area and dispatch immediately via encrypted SMTP (`🚀 TRANSMIT RESPONSE VIA SMTP`).
  * **Resolve:** Clear items from the priority queue and update the WORM ledger (`✅ MARK AS RESOLVED`).

#### 2.5 Sovereign Command AI (Neural Routing Terminal)
* **Functional Scope:** Air-gapped on-premise neural command terminal operating locally on hardware without routing prompts through commercial LLM cloud endpoints.
* **Operational Capabilities:** Executive policy dictation, prompt engineering, tactical response drafting, and technical specification synthesis.

#### 2.6 Master C2 Cockpit & SCADA Telemetry HUD
* **Functional Scope:** High-voltage industrial microgrid monitoring, Modbus RTU telemetry supervision, and autonomous agent coordination.
* **Telemetry Baselines:**
  * Continuous Load Testing: **450.0 Amps** steady-state draw.
  * Active Power Offload: **355.4 Kilowatts** at 480V 3-phase.
  * Kinetic Islanding Velocity: **<16 milliseconds (<1 electrical cycle)** high-speed utility isolation via solid-state Static Transfer Switches (STS).
* **Triad Agent Swarm:** Multi-agent autonomous supervisory loop coordinating Recon, Security, and Analyst agent sweeps across enclave assets.

#### 2.7 Environmental Situational Awareness (NOAA Doppler Radar)
* **Functional Scope:** Live meteorological Doppler radar streams providing severe weather warnings, tornadic activity tracking, and corridor hazard monitoring across Oklahoma transportation routes.

#### 2.8 Downstream Client Updater & WORM Ledger Protection
* **Functional Scope:** Pulls application improvements downstream from verified public repositories while guaranteeing zero customer data leakage.
* **Data Isolation Guarantee:** Updates strictly overwrite application runtime scripts (`ebony_console_GREEN.py`, `ebony_tier_manager.py`, etc.). Customer database files (`matrix_ledger.db`), mailbox credentials (`email_accounts.json`), and system logs (`autopilot_daemon.log`) are permanently protected and never overwritten.

---

### PART III: COMMERCIAL SUBSCRIPTION TIERS & LICENSING RULES

| Commercial Tier | Price Point | Included Operational Capabilities | Access Enforcement |
| :--- | :--- | :--- | :--- |
| **Tier 1: Personal Comms** | **$19.99 / Month** | Sovereign Dispatch Deck, Travel Autopilot, Inbound Threat Scrubber, Return Debrief, NOAA Radar, System Overview, Feedback Hub. | Base Tier. Bounded to communications & weather telemetry. |
| **Tier 1.5: Sovereign Command** | **$39.99 / Month** | Everything in Tier 1 PLUS 💬 Sovereign Command Neural Terminal & 📡 Live Optical Sensor Bus (Arducam & Tapo IP Streams). | Requires active Tier 1.5 entitlement. |
| **Tier 2: VIP Operational** | **$249.00 / Month** | Everything in Tier 1.5 PLUS 🎛️ Master C2 Cockpit HUD, 🌾 Drone Diagnostics, 📡 LinkedIn Engine, Weather SCADA, Grain Silo Telemetry. | Requires active Tier 2 entitlement. |
| **Tier 3: Enterprise CEO** | **$2,499.00 / Year** | Full Suite PLUS Multi-Site Admin Keys, Client Dashboards, Title 61 Statutory Interlocks, and State Grant Application Packs. | Annual Enterprise Agreement. |
| **Hardware Appliance** | **$4,950 Setup + $299/mo** | Physical 2U/4U Bare-Metal Industrial Server (HVFNexus), Air-Gapped Rack Integration, Hardware Watchdog, On-Site Maintenance SLA. | Physical Bare-Metal Deployment. |
| **👑 CEO Clearance** | **Executive Root** | Unrestricted administrative bypass across all 30+ modules, engineering workbenches, and physical hardware buses. | Sovereign Root Authority. |

---

### PART IV: STATUTORY LEGAL DISCLAIMERS & TERMS OF LICENSING

#### 4.1 Disclaimer of Autonomous Agency & Executive Representation
1. **Autonomous Drafting as Non-Binding Advice:** E.B.O.N.Y., Humphrey Virtual Farms LLC, its generative neural routines, and its automated response dispatchers operate solely as executive intelligence aids. The platform generates draft text and automated communications based on algorithmic pattern analysis, user-defined rules, and localized model scoring.
2. **Sole Operator Responsibility:** The licensed subscriber, account holder, or designated organizational user maintains full, exclusive, and non-delegable legal, ethical, and fiduciary responsibility for all communications dispatched from accounts provisioned in the system. 
3. **No Agency Relationship:** The deployment or engagement of the Executive Travel Autopilot mode does not establish Humphrey Virtual Farms LLC as an attorney, broker, fiduciary, or commercial agent of the subscriber. Outbound messages transmitted over SMTP (Port 465/587) carry the legal significance of messages transmitted manually by the account owner. The subscriber is required to review priority queues and audit logs regularly.

#### 4.2 Disclaimer of Critical Infrastructure & Electrical Interties
1. **Physical Voltage & Arc Flash Hazard:** Industrial substation and kinetic grid islanding features described within E.B.O.N.Y. documentation (specifically 480V 3-phase, 450A continuous draw, and sub-16ms fast transfer) involve hazardous electrical currents capable of causing catastrophic equipment damage, severe bodily injury, or death.
2. **Professional Engineer (PE) Mandate:** No software instruction, SCADA register write, or Modbus control loop initiated by E.B.O.N.Y. replaces physical electrical interlocks, certified protective relays (e.g., SEL-751), or utility-approved disconnects. All physical substation installations, Static Transfer Switch alignments, and busbar terminations must be designed, stamped, and commissioned by licensed Professional Engineers and certified electrical contractors in compliance with Oklahoma Title 61 and National Electrical Code (NEC/NFPA 70) standards.
3. **Utility Intertie Authority:** Statutory exemptions under Oklahoma HB 2992 apply strictly to behind-the-meter (BTM) certified test facilities. Connection to regional distribution or transmission utility grids remains governed by applicable regional transmission organizations (e.g., Southwest Power Pool) and local electric utility tariffs.

#### 4.3 Data Custody, Air-Gap Integrity & Privacy Guarantee
1. **Zero Data Custody by Licensor:** Humphrey Virtual Farms LLC does not maintain access, custody, or control over subscriber credentials, email content, client communications, or local audit databases. All cryptographic hashes and WORM ledger entries remain on the subscriber's bare-metal hardware.
2. **Loss of Access & Encryption:** Humphrey Virtual Farms LLC cannot recover, decrypt, or restore lost local master passwords, revoked Google App Passwords, or corrupted local SQLite databases. The subscriber is solely responsible for maintaining local offline physical backups.

#### 4.4 Warranty Disclaimer & Limitation of Liability
1. **"As-Is" and "As-Available" Provision:** To the maximum extent permitted by applicable law, E.B.O.N.Y. and all associated modules are provided on an "AS-IS" and "AS-AVAILABLE" basis without warranties of any kind, whether express, statutory, or implied, including but not limited to implied warranties of merchantability, fitness for a particular purpose, title, and non-infringement.
2. **Limitation of Damages:** In no event shall Humphrey Virtual Farms LLC, its members, managers, officers, developers, or affiliates be liable for any direct, indirect, incidental, special, consequential, punitive, or exemplary damages—including but not limited to loss of profits, loss of data, email transmission failures, network outages, agricultural yield losses, utility demand ratchet penalties, electrical equipment failures, or business interruption—arising out of or in connection with the use, inability to use, or reliance upon the platform.
3. **Cap on Monetary Liability:** In any circumstance where liability is judicially determined, the aggregate cumulative liability of Humphrey Virtual Farms LLC shall not exceed the total subscription fees actually paid by the subscriber to Humphrey Virtual Farms LLC during the three (3) calendar months immediately preceding the event giving rise to liability.

#### 4.5 Indemnification
The subscriber agrees to defend, indemnify, and hold harmless Humphrey Virtual Farms LLC, its principals, officers, and technical personnel from and against any third-party claims, liabilities, losses, damages, fines, penalties, costs, or expenses (including reasonable attorneys' fees) arising out of or resulting from:
* Transmissions dispatched autonomously or manually from the subscriber's configured mailboxes.
* Unauthorized access to subscriber hardware, lost App Passwords, or compromised local networks.
* Physical installation, operation, or maintenance of electrical switchgear, substations, or drone equipment operated in conjunction with E.B.O.N.Y. software.
* Violation of state or federal laws, telecommunications regulations, or statutory disclosure obligations.

#### 4.6 Governing Law, Jurisdiction & Statutory Venue
This Agreement, the software license, and all disputes arising hereunder shall be governed by, construed, and enforced in accordance with the substantive laws of the **State of Oklahoma**, without regard to conflict of law principles. Any legal action, suit, or proceeding arising under or relating to this platform shall be instituted exclusively in the **District Court of Oklahoma County, State of Oklahoma**, or the United States District Court for the Western District of Oklahoma. The parties hereby irrevocably consent and submit to the personal and exclusive jurisdiction of said courts.

---

### PART V: CERTIFICATION & IMMUTABLE COMMITTAL

By initializing E.B.O.N.Y., completing the 60-second credential onboarding protocol, or engaging any command module, the operator certifies compliance with Oklahoma Title 61, OK HB 2992, and the Terms of Licensing set forth herein.

**HUMPHREY VIRTUAL FARMS LLC**  
Office of the Chief Executive Officer & Principal Systems Architect  
Sovereign Enclave Node // HVFNexus  
Contact & Statutory Notice: humphreyvirtualfarm@gmail.com