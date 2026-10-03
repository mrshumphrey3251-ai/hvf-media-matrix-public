# PROJECT EBONY: PHASE 2 INTEGRATION PARAMETERS
**Date:** September 4, 2026
**Governance:** Humphrey Virtual Farms (52% Majority) | SignalLink Protocol (48% Minority)

## 1. The Signaling Architecture (The Handshake)
*   SignalLink will manage the WebRTC signaling (SDP offer/answer) and STUN/TURN external relays.
*   **HVF Mandate:** All signaling must interface through a sovereign HVF-controlled API gateway. Direct inbound connection to the bare-metal execution hardware is strictly prohibited.

## 2. The Media Pipeline (The Payload)
*   HVF's OpenVINO matrix will synthesize the neural media assets natively on local silicon.
*   **HVF Mandate:** The matrix will pass the finalized media stream to SignalLink's WebRTC bridge via a secure, localized UDP port. SignalLink is responsible purely for external transport; HVF retains absolute control over asset generation.

## 3. The IP Boundary (The Vault)
*   Both corporate codebases remain 100% isolated. 
*   **HVF Mandate:** SignalLink will receive endpoint documentation and API keys for the handshake. They will receive zero access to HVF's private GitHub repositories, model weights, or Python/C++ pipelines.
