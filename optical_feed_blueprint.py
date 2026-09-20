"""
HUMPHREY VIRTUAL FARMS LLC | SOVEREIGN COMMUNICATIONS DECK
Public Architecture Blueprint: One-Touch Optical Hardware Switcher & Tailscale Routing
Compliance: DFARS 252.227-7018 Data Rights Protection (Sanitized Public Export)
"""

class OneTouchOpticalSwitcherBlueprint:
    """
    Architectural specification for immediate one-touch optical sensor selection.
    - Default state automatically activates physical host desktop hardware (Arducam-1080P-HDR HD)
    - One-touch tactical buttons toggle between Desktop Index 1 (HD), Index 0 (SD), and Mobile Uplink
    - Dynamic Tailscale IP gateway resolution (100.87.162.117:8502) allows phone browsers
      to display physical desktop workstation cameras at 30 FPS without client camera hijacking
    - Zero cloud dependencies; strictly sovereign LAN and Tailscale encrypted mesh transport
    """
    def __init__(self):
        self.default_source = "DESKTOP_ARDUCAM_HD"
        self.tailscale_gateway = "100.87.162.117:8502"
        self.fps = 30
        self.compliance = "DFARS 252.227-7018"

    def architectural_rules(self):
        return [
            "1. C2 HUD defaults to physical desktop hardware bus upon initial session load",
            "2. Direct touch buttons execute daemon control API without multi-step dropdown delays",
            "3. Cross-origin global CORS headers permit fluid video rendering across mobile endpoints",
            "4. Both private and public repositories synchronize on every operational release"
        ]
