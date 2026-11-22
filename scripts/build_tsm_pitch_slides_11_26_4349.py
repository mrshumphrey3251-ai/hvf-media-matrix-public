from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PRIV_OUT = Path(r"C:\hvf_c2\hvf-media-matrix-private\governance\dossiers\tsm_11_26_4349_slides")
PUB_OUT  = Path(r"C:\hvf_c2\hvf-media-matrix-public\governance\dossiers\tsm_11_26_4349_slides")
PRIV_OUT.mkdir(parents=True, exist_ok=True)
PUB_OUT.mkdir(parents=True, exist_ok=True)

W, H = 1920, 1080
BG_DARK     = (11, 16, 26)
PANEL_BG    = (20, 29, 46)
PANEL_ALT   = (26, 38, 60)
BORDER      = (56, 82, 122)
ACCENT_CYAN = (0, 212, 255)
ACCENT_GOLD = (245, 184, 65)
ACCENT_GRN  = (46, 213, 115)
TEXT_WHITE  = (245, 248, 255)
TEXT_MUTED  = (176, 192, 218)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = (
        [r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\calibrib.ttf"]
        if bold
        else [r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\calibri.ttf"]
    )
    for fp in candidates:
        if Path(fp).exists():
            return ImageFont.truetype(fp, size=size)
    return ImageFont.load_default()


F_BRAND  = load_font(22, bold=True)
F_TAG    = load_font(21, bold=True)
F_H1     = load_font(46, bold=True)
F_H2     = load_font(28, bold=True)
F_SUB    = load_font(25, bold=False)
F_CARD_T = load_font(25, bold=True)
F_BODY   = load_font(22, bold=False)
F_BIG    = load_font(42, bold=True)
F_FOOT   = load_font(19, bold=False)


def draw_wrapped(draw: ImageDraw.ImageDraw, text: str, x: int, y: int, max_w: int, font, fill, line_h: int = 32) -> int:
    words = text.split(" ")
    line = ""
    cur_y = y
    for w in words:
        test = (line + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if (bbox[2] - bbox[0]) <= max_w:
            line = test
        else:
            if line:
                draw.text((x, cur_y), line, font=font, fill=fill)
                cur_y += line_h
            line = w
    if line:
        draw.text((x, cur_y), line, font=font, fill=fill)
        cur_y += line_h
    return cur_y


def base_canvas(slide_num: str, criterion_tag: str, title: str, subtitle: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), BG_DARK)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 68], fill=PANEL_BG)
    d.line([(0, 68), (W, 68)], fill=BORDER, width=2)
    d.text((64, 20), "HUMPHREY VIRTUAL FARMS LLC  |  CAGE: 1AHA8  |  UEI: S1M4ENLHTDH5", font=F_BRAND, fill=ACCENT_CYAN)
    d.text((W - 500, 20), "DOCKET 11-26-4349  |  ASSESSOR-ALIGNED FINAL", font=F_TAG, fill=ACCENT_GOLD)

    d.rounded_rectangle([64, 92, 680, 136], radius=8, fill=PANEL_ALT, outline=ACCENT_CYAN, width=2)
    d.text((82, 102), criterion_tag, font=F_TAG, fill=ACCENT_CYAN)

    d.text((64, 152), title, font=F_H1, fill=TEXT_WHITE)
    d.text((64, 214), subtitle, font=F_SUB, fill=TEXT_MUTED)
    d.line([(64, 258), (W - 64, 258)], fill=BORDER, width=2)

    d.rectangle([0, H - 54, W, H], fill=PANEL_BG)
    d.line([(0, H - 54), (W, H - 54)], fill=BORDER, width=2)
    d.text((64, H - 38), "PROJECT E.B.O.N.Y. v8.0.0  |  All Prior Evaluator Observations Resolved With Reproducible Bare-Metal Receipts", font=F_FOOT, fill=TEXT_MUTED)
    d.text((W - 210, H - 38), f"SLIDE {slide_num}", font=F_FOOT, fill=ACCENT_GOLD)
    return img, d


def build_slide_1() -> Path:
    img, d = base_canvas(
        "1 / 5",
        "EXECUTIVE IDENTITY & FULL ASSESSOR RESOLUTION",
        "Project E.B.O.N.Y. v8.0.0: Zero-Cloud OT/SCADA Interlock Architecture",
        "Direct Resolution of Every Evaluator Observation From Docket 10-26-4046 (TRL 4 Bare-Metal Baseline)",
    )
    boxes = [
        ("PRIME CONTRACTOR IDENTITY", [
            "Humphrey Virtual Farms LLC (Oklahoma, USA)",
            "CAGE: 1AHA8  |  SAM.gov UEI: S1M4ENLHTDH5",
            "Non-Traditional Small Business (10 U.S.C. Sec. 3014)",
            "Jeffery Humphrey, Founder & CEO",
        ], ACCENT_CYAN),
        ("VERIFIED TRL 4 BARE-METAL RECEIPTS", [
            "5,577,006 Sequential WORM SHA-256 Merkle Blocks",
            "59 Empirical Bare-Metal Stress Arenas (Integrity: OK)",
            "1,024-Writer OS Swarm & 2.0 GB Block Scaling",
            "NIST SP 800-171 Rev. 2 Self-Assessment (SPRS: 110/110)",
        ], ACCENT_GRN),
        ("ALL 8 EVALUATOR CRITIQUES RESOLVED", [
            "Crit. 1: SEL-751 vs. Supervisory Bus + IEEE 1584 / I^2t",
            "Crit. 2: 5-Stage Benchmark + OOB Root-Tamper + HIL Plan",
            "Crit. 3: Equivalent 1,000-Trial Benchmark + 28-45 W Draw",
            "Crit. 4: $0 Federal Awards Disclosed + CLINs & DFARS",
        ], ACCENT_GOLD),
    ]
    for i, (hdr, items, col) in enumerate(boxes):
        x0 = 64 + i * 608
        d.rounded_rectangle([x0, 294, x0 + 576, 960], radius=14, fill=PANEL_BG, outline=col, width=3)
        d.text((x0 + 30, 326), hdr, font=F_CARD_T, fill=col)
        d.line([(x0 + 30, 372), (x0 + 546, 372)], fill=BORDER, width=2)
        y = 404
        for it in items:
            y = draw_wrapped(d, "•  " + it, x0 + 30, y, 516, F_BODY, TEXT_WHITE, line_h=34) + 24

    for p in (PRIV_OUT, PUB_OUT):
        img.save(p / "Slide_01_Title_Verification_Anchor.png", format="PNG")
    return PUB_OUT / "Slide_01_Title_Verification_Anchor.png"


def build_slide_2() -> Path:
    img, d = base_canvas(
        "2 / 5",
        "CRITERION 1: DEFINING THE PROBLEM",
        "Dedicated Relays vs. Supervisory SCADA Gap & Fault Physics",
        "Resolving Evaluator 1 & 2 Questions on PLC Scan Timing, Shared Root Cause & Threshold Basis",
    )
    d.rounded_rectangle([64, 290, 1080, 965], radius=14, fill=PANEL_BG, outline=ACCENT_CYAN, width=3)
    d.text((96, 318), "ASSESSOR CRITIQUE RESOLVED: RELAYS VS. SUPERVISORY BUS", font=F_CARD_T, fill=ACCENT_GOLD)
    d.line([(96, 360), (1048, 360)], fill=BORDER, width=2)

    pts = [
        ("Dedicated Local Relays (SEL-751):", "Clear local hardwired overcurrent faults in 40-58 ms. Project E.B.O.N.Y. does NOT replace local overcurrent relays."),
        ("The 70-150+ ms Supervisory SCADA Gap:", "Multi-source DoD microgrids (Utility + Solar PV + BESS + Diesel) coordinate islanding via polled Modbus TCP / DNP3 buses lacking per-frame cryptographic authentication."),
        ("Single Shared Operational Root Cause:", "Unauthenticated trust in supervisory telemetry/commands + >16.0 ms trip delay drives cyber spoofing, arc-flash escalation, and thermal excursions (GAO-21-81, GAO-24-106137, CISA AA24-038A)."),
        ("Representative Substation Blueprint:", "13.8 kV Utility PCC -> 5 MVA Transformer (13.8 kV / 480 V, Z = 5.75%) -> 104,606 A bolted 3-phase fault current at 480 V bus."),
    ]
    y = 382
    for lbl, body in pts:
        d.text((96, y), lbl, font=F_CARD_T, fill=ACCENT_CYAN)
        y = draw_wrapped(d, body, 96, y + 32, 952, F_BODY, TEXT_WHITE, line_h=30) + 16

    d.rounded_rectangle([1116, 290, 1856, 610], radius=14, fill=PANEL_BG, outline=ACCENT_GRN, width=3)
    d.text((1148, 318), "IEEE STD 1584-2018 ARC-FLASH BASIS", font=F_CARD_T, fill=ACCENT_GRN)
    d.text((1148, 372), "84.0% Duration Reduction", font=F_BIG, fill=TEXT_WHITE)
    draw_wrapped(d, "Cutting supervisory trip assertion from 100 ms (6 cycles) to <16.0 ms (1 cycle) reduces supervisory arc-flash incident energy contribution by 84.0% (E proportional to I_arc x t_arc).", 1148, 444, 676, F_BODY, TEXT_MUTED, line_h=31)

    d.rounded_rectangle([1116, 642, 1856, 965], radius=14, fill=PANEL_BG, outline=ACCENT_GOLD, width=3)
    d.text((1148, 670), "IEEE C57.91 THERMAL I^2t BASIS", font=F_CARD_T, fill=ACCENT_GOLD)
    d.text((1148, 724), "6.25x Thermal Reduction", font=F_BIG, fill=TEXT_WHITE)
    draw_wrapped(d, "Limiting supervisory fault persistence from 100 ms to 16.0 ms reduces adiabatic conductor/busbar thermal let-through energy by 6.25x (Integral of i(t)^2 dt).", 1148, 796, 676, F_BODY, TEXT_MUTED, line_h=31)

    for p in (PRIV_OUT, PUB_OUT):
        img.save(p / "Slide_02_Criterion1_Problem_Microgrid.png", format="PNG")
    return PUB_OUT / "Slide_02_Criterion1_Problem_Microgrid.png"


def build_slide_3() -> Path:
    img, d = base_canvas(
        "3 / 5",
        "CRITERION 2: ACCELERATING THE MISSION",
        "5-Stage Bare-Metal Proof, Privileged-Tamper Guard & 180-Day HIL",
        "Resolving Evaluator Questions on Modeled Targets, Relay Integration, Root Tampering & Maturation",
    )
    d.rounded_rectangle([64, 290, 1110, 965], radius=14, fill=PANEL_BG, outline=ACCENT_GRN, width=3)
    d.text((96, 318), "ASSESSOR CRITIQUE RESOLVED: STAGE-BY-STAGE PROOF", font=F_CARD_T, fill=ACCENT_GOLD)
    d.line([(96, 360), (1078, 360)], fill=BORDER, width=2)

    stages = [
        ("Stages 1-4 Fast Control Loop (Verified TRL 4)", "p50 = 2.60 us  |  p99 = 4.50 us", "Telemetry parse -> HMAC-SHA256 verify -> Interlock decision -> Trip register (0xAA55)."),
        ("400% CPU Oversubscription (Arena 57)", "max = 117.10 us  |  0 Breaches", "64 spin processes pinning all 16 logical cores across 50,000 cycles (<16,000 us ceiling)."),
        ("Stage 5 Immutable Audit Seal (Verified TRL 4)", "p50 = 6.04 ms (500 Trials)", "Append-only WORM SHA-256 Merkle commit (5/5 SQL rewrite/upsert vectors blocked)."),
        ("Privileged-Admin Root Tamper Guard (Arena 59)", "100% Replacement Detected", "Detached out-of-band HMAC-SHA256 anchor catches root/admin DB file swap on disk."),
        ("Stage 6 Physical Switch / Breaker (Phase I HIL)", "36.75 ns MOSFET Spec + Breaker", "Explicitly separated as funded TRL 5 -> TRL 6 Hardware-in-the-Loop deliverable."),
    ]
    y = 380
    for st_name, metric, desc in stages:
        d.text((96, y), st_name, font=F_CARD_T, fill=TEXT_WHITE)
        d.text((710, y), metric, font=F_CARD_T, fill=ACCENT_CYAN)
        y = draw_wrapped(d, desc, 96, y + 32, 982, F_BODY, TEXT_MUTED, line_h=28) + 18

    d.rounded_rectangle([1142, 290, 1856, 965], radius=14, fill=PANEL_BG, outline=ACCENT_CYAN, width=3)
    d.text((1174, 318), "PLAN OF INCLUSION & 180-DAY HIL PLAN", font=F_CARD_T, fill=ACCENT_GOLD)
    d.line([(1174, 360), (1824, 360)], fill=BORDER, width=2)

    hil_items = [
        ("Parallel Relay Wiring (Zero SPOF):", "Installs alongside SEL-751/351 relays with IEC 61508 fail-safe watchdog fallback; never disables local relay trips."),
        ("Milestone 1 (Days 1-45 | TRL 4 -> 5):", "Wire bare-metal edge node to CT/PT sensors, SEL-751 relay, and OPAL-RT / 480 V benchtop HIL simulator (<1.0 ms wire-to-coil)."),
        ("Milestone 2 (Days 46-120 | TRL 5):", "Execute 500+ 480 V undervoltage, phase-loss, and live HMAC-spoof tests under resistive/inductive loads."),
        ("Milestone 3 (Days 121-180 | TRL 6):", "Independent DoD witness certification (<16.0 ms solid-state / <50 ms breaker) + RMF ATO inheritance package."),
    ]
    y = 382
    for h_lbl, h_txt in hil_items:
        d.text((1174, y), h_lbl, font=F_CARD_T, fill=ACCENT_CYAN)
        y = draw_wrapped(d, h_txt, 1174, y + 32, 650, F_BODY, TEXT_WHITE, line_h=30) + 20

    for p in (PRIV_OUT, PUB_OUT):
        img.save(p / "Slide_03_Criterion2_Mission_HIL_Plan.png", format="PNG")
    return PUB_OUT / "Slide_03_Criterion2_Mission_HIL_Plan.png"


def build_slide_4() -> Path:
    img, d = base_canvas(
        "4 / 5",
        "CRITERION 3: ADVANCING THE STATE OF THE ART",
        "Equivalent-Condition Benchmark & 28-45 W Enclave Power Budget",
        "Resolving Evaluator Questions on Apples-to-Apples Workflows & Full-System Power Draw",
    )
    d.rounded_rectangle([64, 290, 1856, 765], radius=14, fill=PANEL_BG, outline=ACCENT_CYAN, width=3)
    headers = ["ARCHITECTURE (IDENTICAL TEST)", "AIR-GAPPED OPS", "SPOOF REJECTION (1,000 PROBES)", "DECISION-TO-TRIP LATENCY", "TAMPER-EVIDENT AUDIT"]
    col_x = [92, 540, 820, 1210, 1540]
    for hx, htxt in zip(col_x, headers):
        d.text((hx, 320), htxt, font=F_TAG, fill=ACCENT_GOLD)
    d.line([(84, 362), (1836, 362)], fill=BORDER, width=2)

    rows = [
        ("Conventional Polled PLC\n(Modbus TCP / IEC 61131-3)", "Local only\n(no AI)", "0% (unauthenticated\ncleartext coils)", "70 - 150+ ms\n(poll + scan cycle)", "Mutable local\ncontroller logs", TEXT_MUTED),
        ("Passive OT Network IDS\n(NIST SP 800-82 Span)", "Local span\nport", "Alert-only (0 inline\nblocking authority)", "N/A (cannot trip\nphysical actuators)", "Mutable SIEM\ndatabase", TEXT_MUTED),
        ("Cloud Energy / SIEM\nMiddleware Platform", "FAILS when\nWAN severed", "Fails on WAN\ndisconnect", "250 - 2,000+ ms\n(WAN round-trip)", "External cloud\ndependency", TEXT_MUTED),
        ("PROJECT E.B.O.N.Y. v8.0.0\n(Verified TRL 4 Bare-Metal)", "100% Air-Gapped\n(Read-Only AI)", "1,000 / 1,000 (100%)\nTrapped (0 Bleeds)", "p50 = 5.40 us\n(max = 117.10 us)", "WORM SHA-256 +\nOOB HMAC Anchor", ACCENT_GRN),
    ]
    ry = 386
    for idx, (c0, c1, c2, c3, c4, rcol) in enumerate(rows):
        if idx == 3:
            d.rounded_rectangle([80, ry - 10, 1840, ry + 76], radius=10, fill=PANEL_ALT, outline=ACCENT_GRN, width=2)
        for cx, val in zip(col_x, [c0, c1, c2, c3, c4]):
            d.text((cx, ry), val, font=F_BODY, fill=rcol)
        ry += 92

    d.rounded_rectangle([64, 795, 1856, 965], radius=14, fill=PANEL_BG, outline=ACCENT_GOLD, width=3)
    d.text((96, 820), "ASSESSOR CRITIQUE RESOLVED — FULL ENCLAVE POWER BUDGET: 28 - 45 W WALL-PLUG", font=F_CARD_T, fill=ACCENT_GOLD)
    draw_wrapped(
        d,
        "Includes all supporting hardware (not bare processor TDP): Ruggedized DIN-rail compute node (15 W) + Dual isolated NICs & one-way optical OOB diode (8 W) + Industrial AC/DC PSU & transducer conditioning (5-12 W) = 28-45 W total continuous draw (<0.045 kW) vs. multi-kilowatt rack/cloud stacks.",
        96, 862, 1728, F_BODY, TEXT_WHITE, line_h=32,
    )

    for p in (PRIV_OUT, PUB_OUT):
        img.save(p / "Slide_04_Criterion3_Equivalent_Benchmark.png", format="PNG")
    return PUB_OUT / "Slide_04_Criterion3_Equivalent_Benchmark.png"


def build_slide_5() -> Path:
    img, d = base_canvas(
        "5 / 5",
        "CRITERION 4: BUSINESS MODEL & ACQUISITION PATHWAY",
        "Proposed CLIN Deliverables, DFARS Rights & Customer Validation",
        "Resolving Evaluator Questions on Contract Award Status, Scope, Acceptance Criteria & Data Rights",
    )
    clins = [
        ("PROPOSED CLIN 0001 — TIER 1", "$245,000  |  90 Days", [
            "Benchtop HIL & Digital Twin Pilot (FFP)",
            "1 Ruggedized Node + SEL-751 Adapters + OOB Anchor",
            "160 Engineering Hours + Weekly Reviews",
            "Acceptance: 100% spoof rejection (0 bleeds), <1.0 ms wire-to-trip pulse, 500-fault report.",
        ], ACCENT_CYAN),
        ("PROPOSED CLIN 0002 — TIER 2", "$685,000  |  180 Days", [
            "Substation HIL & Microgrid Prototype (OT)",
            "3 Ruggedized Nodes + Optical Diode + 480 V Load Harness",
            "480 Engineering Hours + On-Site Commissioning",
            "Acceptance: Independent TRL 6 witness test (<16.0 ms solid-state / <50 ms breaker) + RMF ATO pack.",
        ], ACCENT_GRN),
        ("PROPOSED CLIN 0003 — TIER 3", "$1,450,000  |  12 Months", [
            "Multi-Feeder Installation Prototype (10 U.S.C. Sec. 4022)",
            "10 Production Nodes + Enclave Aggregator + HSM OOB",
            "1,200 Engineering Hours + 12-Month Sustainment",
            "Acceptance: 99.999% uptime across 90-day operational evaluation with 0 unverified actuations.",
        ], ACCENT_GOLD),
    ]
    for i, (ctitle, cprice, citems, col) in enumerate(clins):
        x0 = 64 + i * 608
        d.rounded_rectangle([x0, 290, x0 + 576, 755], radius=14, fill=PANEL_BG, outline=col, width=3)
        d.text((x0 + 28, 316), ctitle, font=F_TAG, fill=col)
        d.text((x0 + 28, 352), cprice, font=F_H2, fill=TEXT_WHITE)
        d.line([(x0 + 28, 398), (x0 + 548, 398)], fill=BORDER, width=2)
        y = 420
        for cit in citems:
            y = draw_wrapped(d, "•  " + cit, x0 + 28, y, 520, F_BODY, TEXT_WHITE, line_h=30) + 14

    d.rounded_rectangle([64, 785, 1856, 965], radius=14, fill=PANEL_BG, outline=ACCENT_CYAN, width=3)
    d.text((96, 810), "EXPLICIT DISCLOSURE: $0 CURRENT FEDERAL AWARDS  |  DFARS 252.227-7013/7014 RIGHTS", font=F_CARD_T, fill=ACCENT_GOLD)
    draw_wrapped(
        d,
        "Government Purpose Rights (GPR) on all site HIL adapters, substation profiles, RMF/ATO artifacts, and 100% of WORM audit logs (zero vendor lock-in); Restricted Rights retained on core proprietary engines. Originally proven in zero-connectivity bridge diagnostics; executive pilot scoping scheduled Dec 8-10, 2026 with Oklahoma Dept. of Commerce CTO Rob Teel.",
        96, 852, 1728, F_BODY, TEXT_WHITE, line_h=32,
    )

    for p in (PRIV_OUT, PUB_OUT):
        img.save(p / "Slide_05_Criterion4_Business_CLINs_DFARS.png", format="PNG")
    return PUB_OUT / "Slide_05_Criterion4_Business_CLINs_DFARS.png"


def main() -> None:
    for fn in (build_slide_1, build_slide_2, build_slide_3, build_slide_4, build_slide_5):
        out = fn()
        print(f"  [OK] Updated {out.name}", flush=True)


if __name__ == "__main__":
    main()