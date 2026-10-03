# PROJECT EBONY | SOVEREIGN C2 COCKPIT & OPTICAL VISION SPECIFICATION
## Decoupled Optical Inference & Deterministic Command and Control Cockpit

### 1. Architectural Overview
Project Ebony isolates physical SCADA actuation from optical vision pipelines to ensure hard real-time safety. The Sovereign C2 Cockpit provides direct, zero-cloud operator visualization, telemetry aggregation, and remote tablet monitoring.

### 2. Core Architectural Pillars
1. Decoupled Optical Pipelines: Video acquisition and edge inference run asynchronously without blocking deterministic boundary interlocks.
2. Low-Latency Local Streaming: DirectShow capture and WebRTC feeds deliver sub-100ms video directly to authenticated operator consoles.
3. Encrypted Overlay Mesh: Remote tablet command consoles bind through authenticated, encrypted network tunnels (Tailscale mesh) with zero open public ports.
4. Fail-Safe Sensor Ingestion: Edge IoT sensors and RTSP perimeter cameras route into unified telemetry buffers with deterministic drop-on-stall protections.

### 3. Subsystem Manifest
* Master Orchestrator: deploy_sovereign_cockpit_complete.py
* Telemetry Display Engine: fix_military_c2_console.py
* Video Streamer: fix_webrtc_optical_clean.py, patch_directshow_feed.py
* Optical Deck: patch_unified_optical_deck.py, identify_and_snapshot_cameras.py
* Edge Network Suite: audit_connected_devices.py, audit_tablet_ports.py, bind_tablet_tailscale.py
* Peripheral Sensor Gateway: setup_tapo_sensor.py

---
Classification: DISTRIBUTION STATEMENT A. Approved for public release; distribution is unlimited. Physical camera IP addresses, Tailscale authentication keys, and raw DirectShow device GUIDs redacted pursuant to federal commercial data rights regulations.
