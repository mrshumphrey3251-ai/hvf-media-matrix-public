# 🦅 Ebony: Sovereign Edge AI Command Deck
**Humphrey Virtual Farms | Founder & CEO: Jeffery Humphrey**

## System Architecture
Ebony is a sovereign, offline-first agricultural intelligence platform. It is engineered to operate in zero-connectivity environments, utilizing edge-based AI models, live RTMP/WebRTC optical telemetry ingestion, and encrypted federated learning pipelines.

## ⚙️ Partner Deployment Protocol (SignalLink)
This public repository contains the redacted, deployable front-end architecture. To spin up the Command HUD on your local hardware, execute the following protocol:

### 1. Secure the Architecture
Download the ZIP file of this repository and extract it to a dedicated local folder.

### 2. Provision the Environment
Ensure Python 3.10+ is installed on your system. Open your terminal in the extracted folder and install the required dependencies:
`pip install streamlit pandas numpy psutil`

### 3. Ignite the Command Deck
Launch the sovereign edge node by executing:
`streamlit run ebony_console_GREEN.py`

*Note: For live drone optical ingestion, a localized RTMP/WebRTC media gateway (e.g., MediaMTX) must be deployed on Port 1935 prior to ignition.*