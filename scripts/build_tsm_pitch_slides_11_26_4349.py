import hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PRIV_OUT = Path(r"C:\hvf_c2\hvf-media-matrix-private\governance\dossiers\tsm_11_26_4349_slides")
PUB_OUT  = Path(r"C:\hvf_c2\hvf-media-matrix-public\governance\dossiers\tsm_11_26_4349_slides")
PRIV_OUT.mkdir(parents=True, exist_ok=True)
PUB_OUT.mkdir(parents=True, exist_ok=True)

W, H = 1920, 1080

# High-contrast executive dark-slate palette (zero prohibited government seals or CUI markings)
BG_DARK    = (11, 16, 26)
PANEL_BG   = (20, 29, 46)
PANEL_ALT  = (26, 38, 60)
BORDER     = (56, 82, 122)
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
F_TAG    = load_font(22, bold=True)
F_H1     = load_font(48, bold=True)
F_H2     = load_font(30, bold=True)
F_SUB    = load_font(26, bold=False)
F_CARD_T = load_font(26, bold=True)
F_BODY   = load_font(23, bold=False)
F_BIG    = load_font(44, bold=True)
F_FOOT   = load_font(19, bold=False)


def draw_wrapped(draw: ImageDraw.ImageDraw, text: str, x: int, y: int, max_w: int, font, fill, line_h: int = 34) -> int:
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


def base_canvas(slide_num: str, timestamp: str, criterion_tag: str, title: str, subtitle: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), BG_DARK)
    d = ImageDraw.Draw(img)

    # Top executive header bar
    d.rectangle([0, 0, W, 68], fill=PANEL_BG)
    d.line([(0, 68), (W, 68)], fill=BORDER, width=2)
    d.text((64, 20), "HUMPHREY VIRTUAL FARMS LLC  |  CAGE: 1AHA8  |  UEI: S1M4ENLHTDH5", font=F_BRAND, fill=ACCENT_CYAN)
    d.text((W - 440, 20), f"DOCKET 11-26-4349  |  {timestamp}", font=F_TAG, fill=ACCENT_GOLD)

    # Criterion pill & main slide headline
    d.rounded_rectangle([64, 96, 620, 140], radius=8, fill=PANEL_ALT, outline=ACCENT_CYAN, width=2)
    d.text((82, 105), criterion_tag, font=F_TAG, fill=ACCENT_CYAN)

    d.text((64, 158), title, font=F_H1, fill=TEXT_WHITE)
    d.text((64, 222), subtitle, font=F_SUB, fill=TEXT_MUTED)
    d.line([(64, 268), (W - 64, 268)], fill=BORDER, width=2)

    # Bottom footer bar
    d.rectangle([0, H - 54, W, H], fill=PANEL_BG)
    d.line([(0, H - 54), (W, H - 54)], fill=BORDER, width=2)
    d.text((64, H - 38), "PROJECT E.B.O.N.Y. v8.0.0  |  TRL 4 Bare-Metal Verification Baseline (59 Stress Arenas / 5,577,006 WORM Blocks)", font=F_FOOT, fill=TEXT_MUTED)
    d.text((W - 210, H - 38), f"SLIDE {slide_num}", font=F_FOOT, fill=ACCENT_GOLD)
    return img, d


def build_thumbnail() -> Path:
    img = Image.new("RGB", (W, H), BG_DARK)
    d = ImageDraw.Draw(img)

    # Outer accent border
    d.rectangle([28, 28, W - 28, H - 28], outline=ACCENT_CYAN, width=3)
    d.rectangle([44, 44, W - 44, H - 44], outline=BORDER, width=1)

    d.text((96, 92), "HUMPHREY VIRTUAL FARMS LLC  |  CAGE: 1AHA8  |  UEI: S1M4ENLHTDH5", font=F_H2, fill=ACCENT_CYAN)
    d.rounded_rectangle([96, 152, 680, 206], radius=10, fill=PANEL_ALT, outline=ACCENT_GOLD, width=2)
    d.text((120, 165), "TRADEWINDS DOCKET 11-26-4349  |  TRL 4 VERIFIED", font=F_TAG, fill=ACCENT_GOLD)

    d.text((96, 250), "PROJECT E.B.O.N.Y. v8.0.0", font=load_font(86, bold=True), fill=TEXT_WHITE)
    d.text((96, 362), "Deterministic Zero-Cloud OT/SCADA Interlock & WORM Merkle Provenance", font=load_font(38, bold=True), fill=ACCENT_CYAN)
    d.text((96, 424), "Sub-Cycle Microgrid Protection  |  Read-Only Air-Gapped AI  |  Tamper-Proof Audit Ledger", font=F_H2, fill=TEXT_MUTED)

    metrics = [
        ("2.60 us (p50)", "Stages 1-4 Fast Control Loop\n(p99 = 4.50 us | 10,000 Trials)", ACCENT_GRN),
        ("5,577,006", "Sequential WORM SHA-256 Blocks\n(59 Bare-Metal Stress Arenas)", ACCENT_CYAN),
        ("84.0% / 6.25x", "IEEE 1584 Arc-Flash & I^2t Cut\n(13.8kV/480V Substation Model)", ACCENT_GOLD),
        ("1,000 / 1,000", "Spoofed Commands Trapped\n(0 Actuator Bleeds | 28-45 W)", ACCENT_GRN),
    ]
    card_w = 408
    gap = 32
    start_x = 96
    for idx, (big_val, desc, col) in enumerate(metrics):
        cx = start_x + idx * (card_w + gap)
        cy = 530
        d.rounded_rectangle([cx, cy, cx + card_w, cy + 310], radius=14, fill=PANEL_BG, outline=col, width=3)
        d.text((cx + 28, cy + 36), big_val, font=F_BIG, fill=col)
        draw_wrapped(d, desc, cx + 28, cy + 120, card_w - 56, F_BODY, TEXT_WHITE, line_h=34)

    d.text((96, 920), "Reproducible Proof Script: github.com/mrshumphrey3251-ai/hvf-media-matrix-public", font=F_H2, fill=TEXT_MUTED)

    out_priv = PRIV_OUT / "Thumbnail_11_26_4349_Project_EBONY.png"
    out_pub  = PUB_OUT / "Thumbnail_11_26_4349_Project_EBONY.png"
    img.save(out_priv, format="PNG")
    img.save(out_pub, format="PNG")
    return out_pub


def build_slide_1() -> Path:
    img, d = base_canvas(
        "1 / 5",
        "00:00 - 00:35",
        "EXECUTIVE IDENTITY & VERIFICATION ANCHOR",
        "Project E.B.O.N.Y. v8.0.0: Zero-Cloud OT/SCADA Interlock Architecture",
        "Reproducible Bare-Metal Proof for DoD Installation Microgrid Resilience (Docket 11-26-4349)",
    )
    boxes = [
        ("PRIME CONTRACTOR IDENTITY", [
            "Humphrey Virtual Farms LLC (Oklahoma, USA)",
            "CAGE: 1AHA8  |  SAM.gov UEI: S1M4ENLHTDH5",
            "Non-Traditional Small Business (10 U.S.C. Sec. 3014)",
            "Jeffery Humphrey, Founder & CEO",
        ], ACCENT_CYAN),
        ("VERIFIED TRL 4 BARE-METAL BASELINE", [
            "5,577,006 Sequential WORM SHA-256 Merkle Blocks",
            "59 Empirical Bare-Metal Stress Arenas (Integrity: OK)",
            "1,024-Writer OS Concurrency & 2.0 GB Block Scaling",
            "NIST SP 800-171 Rev. 2 Self-Assessment (SPRS: 110/110)",
        ], ACCENT_GRN),
        ("THREE-PLANE SOVEREIGN ARCHITECTURE", [
            "1. Deterministic <16.0 ms Sub-Cycle Interlock Kernel",
            "2. Read-Only Offline AI + Deception Tarpit (0 Bleeds)",
            "3. WORM SHA-256 Ledger + Out-of-Band Tamper Anchor",
            "100% Air-Gapped Execution (28-45 W Enclave Draw)",
        ], ACCENT_GOLD),
    ]
    for i, (hdr, items, col) in enumerate(boxes):
        x0 = 64 + i * 608
        d.rounded_rectangle([x0, 310, x0 + 576, 950], radius=14, fill=PANEL_BG, outline=col, width=3)
        d.text((x0 + 30, 342), hdr, font=F_CARD_T, fill=col)
        d.line([(x0 + 30, 388), (x0 + 546, 388)], fill=BORDER, width=2)
        y = 420
        for it in items:
            y = draw_wrapped(d, "•  " + it, x0 + 30, y, 516, F_BODY, TEXT_WHITE, line_h=34) + 22

    out_priv = PRIV_OUT / "Slide_01_Title_Verification_Anchor.png"
    out_pub  = PUB_OUT / "Slide_01_Title_Verification_Anchor.png"
    img.save(out_priv, format="PNG")
    img.save(out_pub, format="PNG")
    return out_pub


def build_slide_2() -> Path:
    img, d = base_canvas(
        "2 / 5",
        "00:35 - 01:45",
        "CRITERION 1: DEFINING THE PROBLEM",
        "Closing the 70-150+ ms Supervisory SCADA Control Gap on Microgrids",
        "Representative 13.8 kV / 480 V Substation Topology, Shared Root Cause & IEEE 1584 / I^2t Impact",
    )
    # Left panel: Topology & Shared Root Cause
    d.rounded_rectangle([64, 304, 1080, 960], radius=14, fill=PANEL_BG, outline=ACCENT_CYAN, width=3)
    d.text((96, 332), "REPRESENTATIVE DOD SUBSTATION & SHARED ROOT CAUSE", font=F_CARD_T, fill=ACCENT_CYAN)
    d.line([(96, 376), (1048, 376)], fill=BORDER, width=2)

    pts = [
        ("Dedicated Local Relays (SEL-751):", "Clear local hardwired overcurrent faults in 40-58 ms when uncompromised. Project E.B.O.N.Y. does NOT replace local overcurrent relays."),
        ("The Supervisory SCADA Blind Spot:", "Multi-source microgrids (Utility + Solar PV + BESS + Diesel) coordinate islanding and load-shedding via polled Modbus TCP / DNP3 buses (70-150+ ms) lacking per-frame cryptographic authentication."),
        ("Single Shared Operational Root Cause:", "Unauthenticated trust in supervisory SCADA telemetry/commands across shared OT buses + >16.0 ms latency gap drives cyber spoofing, arc-flash escalation, and thermal excursions (GAO-21-81, GAO-24-106137, CISA AA24-038A Volt Typhoon)."),
        ("Substation Blueprint:", "13.8 kV Utility PCC -> 5 MVA Transformer (13.8 kV / 480 V, Z = 5.75%) -> 104,606 A maximum bolted 3-phase fault current at 480 V bus."),
    ]
    y = 402
    for lbl, body in pts:
        d.text((96, y), lbl, font=F_CARD_T, fill=ACCENT_GOLD)
        y = draw_wrapped(d, body, 96, y + 34, 952, F_BODY, TEXT_WHITE, line_h=31) + 18

    # Right panels: Quantitative IEEE 1584 & I^2t reductions
    d.rounded_rectangle([1116, 304, 1856, 616], radius=14, fill=PANEL_BG, outline=ACCENT_GRN, width=3)
    d.text((1148, 334), "IEEE STD 1584-2018 ARC-FLASH REDUCTION", font=F_CARD_T, fill=ACCENT_GRN)
    d.text((1148, 392), "84.0% Duration Cut", font=F_BIG, fill=TEXT_WHITE)
    draw_wrapped(d, "Cutting supervisory trip assertion from 100 ms (6 cycles) to <16.0 ms (1 cycle) reduces supervisory arc-flash incident energy contribution by 84.0% (E proportional to I_arc x t_arc).", 1148, 466, 676, F_BODY, TEXT_MUTED, line_h=32)

    d.rounded_rectangle([1116, 648, 1856, 960], radius=14, fill=PANEL_BG, outline=ACCENT_GOLD, width=3)
    d.text((1148, 678), "IEEE C57.91 ADIABATIC THERMAL I^2t CUT", font=F_CARD_T, fill=ACCENT_GOLD)
    d.text((1148, 736), "6.25x Thermal Reduction", font=F_BIG, fill=TEXT_WHITE)
    draw_wrapped(d, "Limiting supervisory fault persistence from 100 ms to 16.0 ms cuts conductor/busbar thermal let-through energy by 6.25x (Integral of i(t)^2 dt).", 1148, 810, 676, F_BODY, TEXT_MUTED, line_h=32)

    out_priv = PRIV_OUT / "Slide_02_Criterion1_Problem_Microgrid.png"
    out_pub  = PUB_OUT / "Slide_02_Criterion1_Problem_Microgrid.png"
    img.save(out_priv, format="PNG")
    img.save(out_pub, format="PNG")
    return out_pub


def build_slide_3() -> Path:
    img, d = base_canvas(
        "3 / 5",
        "01:45 - 03:00",
        "CRITERION 2: ACCELERATING THE MISSION",
        "5-Stage Bare-Metal Proof, Fail-Safe Integration & 180-Day HIL Plan",
        "Separating Verified TRL 4 Software (Stress Arena 59) From Funded Phase I Hardware Deliverables",
    )
    # Left panel: 5-Stage Pipeline Benchmark Table
    d.rounded_rectangle([64, 304, 1110, 960], radius=14, fill=PANEL_BG, outline=ACCENT_GRN, width=3)
    d.text((96, 332), "COMPLETE 5-STAGE PROTECTIVE PIPELINE (ARENA 59: 10,000 TRIALS)", font=F_CARD_T, fill=ACCENT_GRN)
    d.line([(96, 376), (1078, 376)], fill=BORDER, width=2)

    stages = [
        ("Stages 1-4 Fast Control Loop (Verified TRL 4)", "p50 = 2.60 us  |  p99 = 4.50 us", "Telemetry parse -> HMAC-SHA256 verify -> Interlock decision -> Trip register (0xAA55)."),
        ("400% CPU Core Oversubscription (Arena 57)", "max = 117.10 us  |  0 Breaches", "64 spin processes pinning all 16 logical cores across 50,000 cycles (<16,000 us ceiling)."),
        ("Stage 5 Immutable Audit Seal (Verified TRL 4)", "p50 = 6.04 ms (500 Trials)", "Append-only WORM SHA-256 Merkle commit (5/5 SQL rewrite/upsert attacks blocked)."),
        ("Privileged-Admin Root Tamper Guard (Arena 59)", "100% Replacement Detected", "Detached out-of-band HMAC-SHA256 anchor catches root/admin DB file swap on disk."),
        ("Stage 6 Physical Switch / Breaker (Phase I HIL)", "36.75 ns MOSFET Spec + Breaker", "Explicitly scoped as funded TRL 5 -> TRL 6 Hardware-in-the-Loop deliverable."),
    ]
    y = 398
    for st_name, metric, desc in stages:
        d.text((96, y), st_name, font=F_CARD_T, fill=TEXT_WHITE)
        d.text((710, y), metric, font=F_CARD_T, fill=ACCENT_CYAN)
        y = draw_wrapped(d, desc, 96, y + 32, 982, F_BODY, TEXT_MUTED, line_h=28) + 18

    # Right panel: Plan of Inclusion & 180-Day HIL Maturation
    d.rounded_rectangle([1142, 304, 1856, 960], radius=14, fill=PANEL_BG, outline=ACCENT_GOLD, width=3)
    d.text((1174, 332), "PLAN OF INCLUSION & 180-DAY HIL ROADMAP", font=F_CARD_T, fill=ACCENT_GOLD)
    d.line([(1174, 376), (1824, 376)], fill=BORDER, width=2)

    hil_items = [
        ("Parallel Relay Integration (Zero SPOF):", "Installs alongside SEL-751/351 relays with IEC 61508 fail-safe de-energize-to-trip watchdog fallback; never disables local relay trips."),
        ("Milestone 1 (Days 1-45 | TRL 4 -> 5):", "Wire bare-metal edge node to CT/PT sensors, SEL-751 relay, and OPAL-RT / 480 V benchtop HIL simulator (<1.0 ms wire-to-coil pulse)."),
        ("Milestone 2 (Days 46-120 | TRL 5):", "Execute 500+ 480 V undervoltage, phase-loss, and live HMAC-spoof injection tests under resistive/inductive loads."),
        ("Milestone 3 (Days 121-180 | TRL 6):", "Independent DoD witness certification (<16.0 ms solid-state / <50 ms breaker clearing) + RMF ATO inheritance package."),
    ]
    y = 402
    for h_lbl, h_txt in hil_items:
        d.text((1174, y), h_lbl, font=F_CARD_T, fill=ACCENT_CYAN)
        y = draw_wrapped(d, h_txt, 1174, y + 34, 650, F_BODY, TEXT_WHITE, line_h=30) + 20

    out_priv = PRIV_OUT / "Slide_03_Criterion2_Mission_HIL_Plan.png"
    out_pub  = PUB_OUT / "Slide_03_Criterion2_Mission_HIL_Plan.png"
    img.save(out_priv, format="PNG")
    img.save(out_pub, format="PNG")
    return out_pub


def build_slide_4() -> Path:
    img, d = base_canvas(
        "4 / 5",
        "03:00 - 03:55",
        "CRITERION 3: ADVANCING THE STATE OF THE ART",
        "Equivalent-Condition Benchmark & 28-45 W Enclave Power Budget",
        "1,000-Trial Air-Gapped Undervoltage Fault + Spoofed Breaker Override Storm (Stress Arena 59)",
    )
    # Table container
    d.rounded_rectangle([64, 304, 1856, 770], radius=14, fill=PANEL_BG, outline=ACCENT_CYAN, width=3)
    headers = ["ARCHITECTURE", "AIR-GAPPED OPS", "SPOOF REJECTION (1,000 PROBES)", "DECISION-TO-TRIP LATENCY", "TAMPER-EVIDENT AUDIT"]
    col_x = [92, 540, 820, 1210, 1540]
    for hx, htxt in zip(col_x, headers):
        d.text((hx, 334), htxt, font=F_TAG, fill=ACCENT_GOLD)
    d.line([(84, 376), (1836, 376)], fill=BORDER, width=2)

    rows = [
        ("Conventional Polled PLC\n(Modbus TCP / IEC 61131-3)", "Local only\n(no AI)", "0% (unauthenticated\ncleartext coils)", "70 - 150+ ms\n(poll + scan cycle)", "Mutable local\ncontroller logs", TEXT_MUTED),
        ("Passive OT Network IDS\n(NIST SP 800-82 Span)", "Local span\nport", "Alert-only (0 inline\nblocking authority)", "N/A (cannot trip\nphysical actuators)", "Mutable SIEM\ndatabase", TEXT_MUTED),
        ("Cloud Energy / SIEM\nMiddleware Platform", "FAILS when\nWAN severed", "Fails on WAN\ndisconnect", "250 - 2,000+ ms\n(WAN round-trip)", "External cloud\ndependency", TEXT_MUTED),
        ("PROJECT E.B.O.N.Y. v8.0.0\n(Verified TRL 4 Bare-Metal)", "100% Air-Gapped\n(Read-Only AI)", "1,000 / 1,000 (100%)\nTrapped (0 Bleeds)", "p50 = 5.40 us\n(max = 117.10 us)", "WORM SHA-256 +\nOOB HMAC Anchor", ACCENT_GRN),
    ]
    ry = 398
    for idx, (c0, c1, c2, c3, c4, rcol) in enumerate(rows):
        if idx == 3:
            d.rounded_rectangle([80, ry - 10, 1840, ry + 76], radius=10, fill=PANEL_ALT, outline=ACCENT_GRN, width=2)
        for cx, val in zip(col_x, [c0, c1, c2, c3, c4]):
            d.text((cx, ry), val, font=F_BODY, fill=rcol)
        ry += 92

    # Bottom wall-plug power budget bar
    d.rounded_rectangle([64, 800, 1856, 960], radius=14, fill=PANEL_BG, outline=ACCENT_GOLD, width=3)
    d.text((96, 826), "FULL-SYSTEM WALL-PLUG POWER BUDGET: 28 - 45 W CONTINUOUS ENCLAVE DRAW", font=F_CARD_T, fill=ACCENT_GOLD)
    draw_wrapped(
        d,
        "Accounts for all supporting enclave hardware (not bare processor TDP): Ruggedized DIN-rail industrial compute node (15 W) + Dual optically isolated NICs & one-way OOB anchor diode (8 W) + Industrial AC/DC PSU & transducer conditioning (5-12 W) = 28-45 W total (<0.045 kW) vs. multi-kilowatt rack/cloud stacks.",
        96, 868, 1728, F_BODY, TEXT_WHITE, line_h=32,
    )

    out_priv = PRIV_OUT / "Slide_04_Criterion3_Equivalent_Benchmark.png"
    out_pub  = PUB_OUT / "Slide_04_Criterion3_Equivalent_Benchmark.png"
    img.save(out_priv, format="PNG")
    img.save(out_pub, format="PNG")
    return out_pub


def build_slide_5() -> Path:
    img, d = base_canvas(
        "5 / 5",
        "03:55 - 04:55",
        "CRITERION 4: BUSINESS MODEL & ACQUISITION PATHWAY",
        "Milestone-Gated Proposed CLINs, DFARS Rights & Dual-Use Demand",
        "Explicit Disclosure: $0 Current Federal Awards — Proposed Prototype OT / FAR Options (10 U.S.C. Sec. 4022)",
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
        d.rounded_rectangle([x0, 304, x0 + 576, 756], radius=14, fill=PANEL_BG, outline=col, width=3)
        d.text((x0 + 28, 330), ctitle, font=F_TAG, fill=col)
        d.text((x0 + 28, 366), cprice, font=F_H2, fill=TEXT_WHITE)
        d.line([(x0 + 28, 412), (x0 + 548, 412)], fill=BORDER, width=2)
        y = 434
        for cit in citems:
            y = draw_wrapped(d, "•  " + cit, x0 + 28, y, 520, F_BODY, TEXT_WHITE, line_h=30) + 14

    # Bottom panel: DFARS Data Rights & Customer Discovery
    d.rounded_rectangle([64, 784, 1856, 960], radius=14, fill=PANEL_BG, outline=ACCENT_CYAN, width=3)
    d.text((96, 810), "DFARS 252.227-7013 / 7014 DATA RIGHTS & CUSTOMER DISCOVERY PIPELINE", font=F_CARD_T, fill=ACCENT_CYAN)
    draw_wrapped(
        d,
        "Government Purpose Rights (GPR) on all site HIL adapters, substation profiles, RMF/ATO artifacts, and 100% of WORM audit logs (zero vendor lock-in); Restricted Rights retained on core proprietary engines. Originally proven in zero-connectivity bridge/structural diagnostics; executive scoping scheduled Dec 8-10, 2026 with Oklahoma Dept. of Commerce CTO Rob Teel.",
        96, 852, 1728, F_BODY, TEXT_WHITE, line_h=32,
    )

    out_priv = PRIV_OUT / "Slide_05_Criterion4_Business_CLINs_DFARS.png"
    out_pub  = PUB_OUT / "Slide_05_Criterion4_Business_CLINs_DFARS.png"
    img.save(out_priv, format="PNG")
    img.save(out_pub, format="PNG")
    return out_pub


def main() -> None:
    files = [
        build_thumbnail(),
        build_slide_1(),
        build_slide_2(),
        build_slide_3(),
        build_slide_4(),
        build_slide_5(),
    ]
    print("\n================================================================================================")
    print("  5 PRESENTATION SLIDES + VIDEO THUMBNAIL (1920x1080 PNG) GENERATED & DUAL-REPO SYNCED!")
    print("================================================================================================")
    for f in files:
        digest = hashlib.sha256(f.read_bytes()).hexdigest()
        print(f"  [OK] {f.name:<48} | SHA-256: {digest[:24]}...")
    print(f"  Output Folder: {PUB_OUT}")
    print("================================================================================================")


if __name__ == "__main__":
    main()