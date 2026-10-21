"""
Humphrey Virtual Farms LLC // Rob Teele (HVF-NODE-TEELE-001) Turnkey Partner Enclave & Briefing Packet Generator
Entity: Humphrey Virtual Farms LLC | CAGE: 1AHA8 | UEI: S1M4ENLHTDH5 | Docket: 9-26-3703
Statutory: Oklahoma Title 61, HB 2992, 10 U.S.C. 4022, DFARS 252.227-7018
"""
import hashlib
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

cockpit_dir = Path(__file__).resolve().parent


def generate_teele_turnkey_packet() -> dict:
    reports_dir = (
        Path(r"C:\hvf_c2\reports\partner_enclaves")
        if os.name == "nt"
        else (cockpit_dir.parent / "reports" / "partner_enclaves")
    )
    reports_dir.mkdir(parents=True, exist_ok=True)

    packet_lines = [
        "# HUMPHREY VIRTUAL FARMS LLC // TURNKEY PARTNER ENCLAVE ONBOARDING PACKET",
        "**Partner Node ID:** `HVF-NODE-TEELE-001` | **Collaborator:** `Rob Teele (Tier-1 Sovereign Partner Seat)`  ",
        "**Prime Authority:** `Jeffery Humphrey, Founder & CEO — Humphrey Virtual Farms LLC (CAGE: 1AHA8 | UEI: S1M4ENLHTDH5)`  ",
        "**Release Seal:** `v5.0.0-sovereign-seal (593 Compiled C2 Modules | 160.0 Accredited Hours | 1,420 Verified Questions)`  ",
        "**DoD Tradewinds Docket:** `9-26-3703 (Project Ebony Tri-Brain & 36.75ns Kinetic Guillotine — Under Assessment)`",
        "",
        "---",
        "",
        "## 1. Executive Correspondence & Seat Activation Ledger",
        "- **2026-10-14 (Outbound CEO Directive):** Tier-1 E.B.O.N.Y. operational seat reserved and enclaved; Oklahoma Title 61 contractor standing and 4 non-dilutive grant vectors (Oklahoma SEP Microgrid, USDA REAP, OCAST UAS, USDA NIFA/SBIR Phase I) established.",
        "- **2026-10-20 (Inbound Partner Confirmation — Rob Teele):** *'Jeff, I am working on getting all this setup for use this week. Thanks for your patience.'*",
        "- **2026-10-21 (Turnkey Delivery Handshake Staged):** `v5.0.0-sovereign-seal` (`593 / 593` modules) certified for immediate deployment upon workstation readiness.",
        "",
        "---",
        "",
        "## 2. Click-by-Click Turnkey Node Initialization Protocol (`HVF-NODE-TEELE-001`)",
        "1. **Step 1 (Repository Sync):** Clone or pull `https://github.com/mrshumphrey3251-ai/hvf-media-matrix-public.git` at tag `v5.0.0-sovereign-seal`.",
        "2. **Step 2 (Cryptographic Self-Test):** Execute `python c2_cockpit/verify_sovereign_seal.py` to verify all `593 / 593` C2 modules and `1,420 / 1,420` Academy questions.",
        "3. **Step 3 (Live Console Launch & Hardware Enclave Lock):** Execute `python -m streamlit run c2_cockpit/ebony_console_GREEN.py` to open `http://localhost:8501` and lock Motherboard UUID / MAC anti-piracy credentials.",
    ]

    packet_md = "\n".join(packet_lines) + "\n"
    packet_hash = hashlib.sha256(packet_md.encode("utf-8")).hexdigest()
    packet_md += f"\n---\n**Turnkey Packet FIPS 180-4 SHA-256 Seal:** `{packet_hash}`\n"

    out_file = reports_dir / "HVF_TEELE_TURNKEY_ONBOARDING_PACKET_v5.md"
    out_file.write_bytes(packet_md.encode("utf-8"))

    print("=" * 92)
    print("   ROB TEELE (HVF-NODE-TEELE-001) TURNKEY ONBOARDING PACKET GENERATED   ")
    print("=" * 92)
    print(f"Packet Path        : {out_file} ({len(packet_md):,} bytes)")
    print(f"Packet SHA-256 Seal: {packet_hash}")
    print("=" * 92)
    return {"packet_file": str(out_file), "sha256_seal": packet_hash}


if __name__ == "__main__":
    generate_teele_turnkey_packet()
