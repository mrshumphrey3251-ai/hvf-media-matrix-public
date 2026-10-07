### Sovereign C2 Cockpit - Universal Optical Uplink Architecture

#### Optical Telemetry Transport Matrix
The Sovereign C2 Cockpit abstracts physical optical hardware into three zero-trust universal transport uplinks:

| Transport Layer | Uplink Class | Protocol / Bus | Target Hardware Scope | Compliance |
| :--- | :--- | :--- | :--- | :--- |
| **Direct Hardware Bus** | `UniversalUSBUplink` | DirectShow / UVC / V4L2 | USB Cams, HDMI Capture, Onboard CSI Sensors | DFARS 252.227-7018 |
| **Network Streaming Bus** | `UniversalRTSPUplink` | RTSP / RTMP / ONVIF / HLS | IP Cameras, Drone GCS Streams, NVR Video Relays | OK Title 61 / HB 2992 |
| **Client Edge Ingest** | `UniversalEdgeUplink` | HTML5 MediaStream / W3C | Field Tablets, Mobile Endpoints, Rugged Scanners | Zero-Trust Client Edge |

#### Security & Air-Gap Standard
- Credentials load dynamically from protected local configuration vaults.
- Offline camera states fail gracefully with non-blocking thread isolation.
- Public documentation contains zero confidential credentials, static IPs, or secret keys.
