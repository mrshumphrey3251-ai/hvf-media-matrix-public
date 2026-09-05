# Project Ebony: Sovereign P2P Telemetry Bridge (Architecture Spec)

## Overview
Project Ebony integrates a zero-cloud, peer-to-peer telemetry and communications bridge leveraging the Holepunch / Pear runtime ecosystem.

## Key Tenets
1. **Twin-Brain Air-Gap:** Deterministic kinetic control (Brain One) remains isolated from communications layers.
2. **Zero Central Relays:** Direct cryptographic addressing eliminates third-party infrastructure and intermediary exposure.
3. **Diode Ingress:** Internal sensor telemetry feeds the P2P transport layer across a strictly bounded local UDP ingress diode (Port 5005) governed by a 200ms kinetic watchdog.
4. **Append-Only Distributed Logs:** Telemetry frames are committed directly to Ed25519-signed Hypercore logs replicated over the Hyperswarm DHT without intermediary cloud brokers.
5. **Ingress Pipeline Verification:** End-to-end integration verified: Local UDP telemetry frames parse and serialize into cryptographic Hypercore log blocks with clean socket lifecycle management.
6. **Decentralized Consumer Mesh:** Remote subscribers resolve the Hypercore feed using public key capability tokens and discover peers via Hyperswarm DHT without centralized discovery servers.
