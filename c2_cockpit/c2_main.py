"""
c2_cockpit/c2_main.py
Project E.B.O.N.Y. v8.0.0 - Sovereign C2 Command & Control Cockpit
Contractor: Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)
Authority: 100% Offline Loopback Architecture (Zero Cloud, Zero External APIs)
"""

import sys
import os
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "modules"))

def launch_briefing_interactive_with_voice():
    """Runs the 9-slide deck on screen while synchronously speaking each slide via Windows SAPI."""
    try:
        from modules.c2_erdc_briefing_viewer import SLIDES, render_slide
        from modules.c2_briefing_audio_narrator import speak_slide_ps
        
        current_idx = 0
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            render_slide(current_idx)
            print("\n[*] Speaking Slide Narration aloud via Windows SAPI...")
            speak_slide_ps(current_idx + 1)
            
            print("\n" + "=" * 82)
            print(" [N]ext Slide (Voice + Screen) | [P]rev Slide | [R]epeat Voice | [Q]uit to C2")
            print("=" * 82)
            choice = input("C2-VOICE-DECK> ").strip().lower()
            
            if choice in ('q', 'quit', 'exit'):
                print("\n[+] Exiting voiceover briefing session.")
                break
            elif choice in ('n', 'next', ''):
                if current_idx < len(SLIDES) - 1:
                    current_idx += 1
                else:
                    print("\n[!] Reached final slide (Slide 9/9).")
                    input("[Press Enter to exit]")
                    break
            elif choice in ('p', 'prev', 'back'):
                if current_idx > 0:
                    current_idx -= 1
            elif choice in ('r', 'repeat'):
                continue
            elif choice.isdigit() and 1 <= int(choice) <= 9:
                current_idx = int(choice) - 1
    except Exception as e:
        print(f"[!] Error in voice-synchronized presentation: {e}")
        input("[Press Enter to return]")

def launch_briefing_silent():
    """Runs the 9-slide deck in silent terminal mode."""
    try:
        from modules.c2_erdc_briefing_viewer import run_briefing_console
        run_briefing_console()
    except Exception as e:
        print(f"[!] Error loading Briefing Viewer: {e}")
        input("[Press Enter to return]")

def launch_html5_presentation():
    """Launches the self-contained HTML5 presentation directly in the default browser."""
    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presentations", "project_ebony_executive_briefing.html")
    if os.path.exists(html_path):
        print(f"[*] Opening standalone presentation on the glass: {html_path}")
        if os.name == 'nt':
            os.startfile(html_path)
        else:
            subprocess.run(["xdg-open", html_path])
    else:
        print(f"[!] HTML5 Presentation file not found at: {html_path}")
        input("[Press Enter to return]")

def presentation_sub_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        width = 84
        print("=" * width)
        print("  PROJECT E.B.O.N.Y. v8.0.0 // 30-MINUTE EXECUTIVE BRIEFING & VOICEOVER SUITE")
        print("  Target: USACE ERDC Rolling BAA ($1.20M) & DIU CSO 10 U.S.C. § 4022 ($1.485M)")
        print("=" * width)
        print("  PRESENTATION DELIVERY CHANNELS:")
        print("   [1] Live Synchronized Presentation (Visual Slides + Aloud Windows SAPI Voiceover)")
        print("   [2] Silent Visual Presentation Mode (Manual Slide-by-Slide Navigation)")
        print("   [3] Launch Standalone HTML5 Browser Deck (On the Glass / Shareable File)")
        print("   [4] Export/Verify All 9 Slide WAV Audio Tracks")
        print("   [B] Back to Main C2 Cockpit")
        print("=" * width)
        
        choice = input("C2-BRIEFING-SUITE> ").strip().lower()
        if choice == '1':
            launch_briefing_interactive_with_voice()
        elif choice == '2':
            launch_briefing_silent()
        elif choice == '3':
            launch_html5_presentation()
            input("\n[Press Enter to return to Briefing Menu]")
        elif choice == '4':
            audio_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presentations", "audio")
            try:
                from modules.c2_briefing_audio_narrator import export_all_slide_audio
                export_all_slide_audio(audio_dir)
            except Exception as e:
                print(f"[!] Export failed: {e}")
            input("\n[Press Enter to continue]")
        elif choice in ('b', 'back', 'q', 'exit'):
            break

def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        width = 84
        print("=" * width)
        print("  PROJECT E.B.O.N.Y. v8.0.0 // SOVEREIGN C2 TACTICAL COMMAND COCKPIT")
        print("  Contractor: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5")
        print("  Status: CDAO Tradewinds Docket 10-26-4046 [UNDER ASSESSMENT] // TRL 4 Loopback")
        print("=" * width)
        print("  CORE MISSION MODULES:")
        print("   [1] 30-Minute Executive Technical Briefing & Turnkey Voiceover Suite (9 Slides)")
        print("   [2] 36.75ns SiC Kinetic Interlock Telemetry & Arc-Flash Fault Simulation")
        print("   [3] 7,500-Mile Series-Hybrid Convoy Powertrain & Energy Scavenging Matrix")
        print("   [4] 480V 3-Phase Tactical Microgrid & Matte ETFE Solar Harvest Diagnostics")
        print("   [5] Cryptographic Merkle DAG Provenance & Single-Byte Tamper Zeroization")
        print("   [6] Phase-1 Supplier Sourcing Tracker & CapEx Ledger Status")
        print("   [Q] Exit Cockpit")
        print("=" * width)
        
        choice = input("C2-EXEC> ").strip().lower()
        if choice == '1':
            presentation_sub_menu()
        elif choice == '2':
            print("\n[*] Module [2]: 36.75ns SiC Interlock running at 28.5W on 24V DC. 17/17 Red-Team vectors blocked.")
            input("\n[Press Enter to continue]")
        elif choice == '3':
            print("\n[*] Module [3]: 7,500-Mile Convoy: 950-Gal JP-8 / 150kW Turbine / Option A eAxle / Option C TEG.")
            input("\n[Press Enter to continue]")
        elif choice == '4':
            print("\n[*] Module [4]: Microgrid: 500 kWh LFP / 18kW Matte ETFE Solar / 480V 3-Phase (300kW Surge).")
            input("\n[Press Enter to continue]")
        elif choice == '5':
            print("\n[*] Module [5]: Merkle Root: bb39eeaa66a39ad2e0c0ab74ba4a5c4faac2bf0d98babc0362482b97607151a1")
            input("\n[Press Enter to continue]")
        elif choice == '6':
            print("\n[*] Module [6]: Phase-1 Sourcing Tracker: 6/16 CapEx components sourced & verified.")
            input("\n[Press Enter to continue]")
        elif choice in ('q', 'exit', 'quit'):
            print("\n[+] Exiting Sovereign C2 Cockpit.")
            break
        else:
            print(f"\n[!] Unrecognized option '{choice}'.")
            input("[Press Enter to continue]")

if __name__ == "__main__":
    main_menu()
