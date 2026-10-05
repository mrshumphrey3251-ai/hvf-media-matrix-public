from pathlib import Path
from datetime import datetime, timezone

targets = [
    Path(r"C:\HVF_Repos\hvf-media-matrix-private\governance\legal\MUTUAL_NDA_VANDERPOOL_ENERGY_DESIGN_FINAL.md"),
    Path(r"C:\HVF_Repos\hvf-media-matrix-public\governance\legal\MUTUAL_NDA_VANDERPOOL_ENERGY_DESIGN_FINAL.md")
]

today_str = datetime.now(timezone.utc).strftime('%B %d, %Y')

nda_text = f"""# MUTUAL NON-DISCLOSURE AND INTELLECTUAL PROPERTY PROTECTION AGREEMENT

**EFFECTIVE DATE:** {today_str}  
**GOVERNING LAW:** State of Oklahoma  

This Mutual Non-Disclosure and Intellectual Property Protection Agreement ("Agreement") is entered into by and between:

1. **Humphrey Virtual Farm & Media Matrix** ("HVF"), having an operational desk under CAGE Code `1AHA8`, represented by **Jeffery Humphrey**, Chief Executive Officer & Founder (Principal Architect, Project Ebony), with primary offices in the State of Oklahoma; and

2. **Vanderpool Energy Design LLC** ("Company"), a limited liability company incorporated under the laws of the **Commonwealth of Pennsylvania**, represented by **Richard Vanderpool**, Founder, having a corporate delivery address at `rickyvanderpool15@gmail.com`.

HVF and Company may collectively be referred to as the "Parties" or individually as a "Party."

---

### 1. PURPOSE OF ENGAGEMENT
The Parties desire to conduct high-level, preliminary exploratory discussions strictly limited to evaluating commercial compatibility between Company's proprietary modular physical containment/vault blueprints and HVF's sovereign bare-metal control layer ("Project Ebony" / "Chronos SCADA" / "Protocol Lambda").

### 2. STRICT CARVE-OUT & PRESERVATION OF PRE-EXISTING IP
**2.1 Exclusive Ownership:** Company expressly acknowledges that **Project Ebony**, **Protocol Lambda**, **Chronos SCADA**, the **Tri-Brain Bare-Metal Edge Architecture**, **Sub-Microsecond Kinetic Isolation**, **Docket 9-26-3703**, and all associated algorithms, firmware, Modbus/DNP3 switchgear controls, and system state logic are the sole, exclusive, pre-existing intellectual property of Jeffery Humphrey and HVF.  
**2.2 No Grant of Rights:** Nothing contained in this Agreement or any technical briefing shall be construed as granting, by implication, estoppel, or otherwise, any license, right, title, equity, co-development claim, or joint venture in or to either Party's pre-existing intellectual property.

### 3. PATENT PRECLUSION & NON-CIRCUMVENTION COVENANT
**3.1 Patent Preclusion:** Company explicitly covenants that it shall not use, reference, adapt, reverse-engineer, or incorporate any technical concepts, logic flows, latency benchmarks, or architectural methodologies disclosed by HVF into any current, pending, provisional, or future patent applications, continuations, continuations-in-part, or foreign utility filings.  
**3.2 Non-Circumvention:** Neither Party shall bypass the other to exploit proprietary processes disclosed during the evaluation period.

### 4. CONFIDENTIALITY OBLIGATIONS & EXCLUSIONS
**4.1 Standard of Care:** Each Party agrees to protect Confidential Information using the same degree of care it uses to protect its own sensitive trade secrets, but not less than reasonable care.  
**4.2 Duration:** Obligations of non-disclosure shall survive for a period of five (5) years from the Effective Date, with trade secret protections enduring indefinitely under applicable law.

### 5. GOVERNING LAW & DISPUTE RESOLUTION
This Agreement shall be governed by, construed, and enforced in accordance with the laws of the **State of Oklahoma**, without regard to conflict of law principles. Any legal proceeding arising out of or relating to this Agreement shall be brought exclusively in the state or federal courts situated in the State of Oklahoma.

---

### EXECUTION & SIGNATURES

**HUMPHREY VIRTUAL FARM & MEDIA MATRIX**  
Signature: _________________________________________  
Printed Name: Jeffery Humphrey  
Title: Chief Executive Officer & Founder  
Entity: Humphrey Virtual Farm & Media Matrix  
Date: {today_str}  

**VANDERPOOL ENERGY DESIGN LLC**  
Signature: _________________________________________  
Printed Name: Richard Vanderpool  
Title: Founder  
Entity: Vanderpool Energy Design LLC (Pennsylvania)  
Email: rickyvanderpool15@gmail.com  
Date: ________________________  
"""

for target in targets:
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(nda_text.strip())
    print(f"[+] Finalized Mutual NDA created at: {target}")
