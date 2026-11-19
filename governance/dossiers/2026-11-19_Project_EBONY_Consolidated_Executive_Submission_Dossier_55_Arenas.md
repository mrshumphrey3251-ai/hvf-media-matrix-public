# PROJECT E.B.O.N.Y. — CONSOLIDATED EXECUTIVE SUBMISSION DOSSIER & SHA-256 CHECKSUM MANIFEST
## Sovereign Air-Gapped Deterministic Control Plane for Defense & Critical Infrastructure

* **Prime Contractor:** Humphrey Virtual Farms LLC (`CAGE: 1AHA8` | `SAM.gov UEI: S1M4ENLHTDH5`)
* **Chief Executive Officer & Principal Architect:** Jeffery Humphrey
* **Federal Procurement Docket:** DoD Tradewinds Solutions Marketplace (`Docket 10-26-4046`) | AFWERX | DIU | Oklahoma Department of Commerce
* **Dossier Compilation Timestamp (UTC):** `2026-11-19T16:16:50Z`
* **Public Verification Mirror:** `https://github.com/mrshumphrey3251-ai/hvf-media-matrix-public`
* **Cybersecurity Compliance Posture:** NIST SP 800-171 Rev. 2 / DFARS 252.204-7012 (`SPRS Score: 110 / 110`)

---

### 1. Executive Summary & Architectural Value Proposition

**Project E.B.O.N.Y.** eliminates the single largest failure mode in autonomous AI and critical infrastructure control: granting probabilistic software agents shared credentials, network reachability, or physical actuator authority. Engineered from bare metal upward for air-gapped defense installations, microgrids, and industrial control environments, Project E.B.O.N.Y. enforces three non-negotiable deterministic invariants:

1. **Zero Shared Credentials & Read-Only AI Isolation:** Offline advisory models execute strictly read-only with zero internet connectivity, zero shared secrets, and zero actuator bindings. Unauthorized override attempts are automatically diverted into `SovereignDeceptionTarpit`—a deterministic read-only mirror maze that traps hostile reconnaissance while maintaining **zero physical actuator bleed**.
2. **Deterministic Sub-Cycle Hardware & Cryptographic Interlocks:** Every state transition requires per-epoch `HMAC-SHA256` cryptographic authentication and enforces deterministic sub-cycle grid-collapse islanding cutoffs well below the **16.0 ms (`16,000 µs`)** single-cycle 60 Hz statutory/engineering threshold (Oklahoma HB 2992 & IEEE 1547 alignment).
3. **Immutable WORM-Protected SHA-256 Merkle Audit Trail:** Every authenticated telemetry frame, policy state, and human out-of-band override seals atomically into an append-only, trigger-enforced Write-Once-Read-Many (`WORM`) SQLite SHA-256 Merkle ledger (`SovereignMerkleLedger`), protected against `UPDATE`, `DELETE`, and `REPLACE/OVERWRITE` tampering, serialized across concurrent OS writers via `BEGIN IMMEDIATE`, and bounded on disk by a hard **256.00 MB (`268,435,456` bytes)** `WAL` size cap (`PRAGMA journal_size_limit`).

---

### 2. Empirical Bare-Metal Verification Summary (`55` Stress Arenas | `5,577,003` WORM Blocks)

All claims in this dossier are backed by **55 empirical Stress Arenas** (`54` archived cryptographic receipts) executed directly on bare-metal hardware with full genesis-to-head mathematical verification:

| Empirical Verification Metric | Verified Bare-Metal Result |
| :--- | :--- |
| **Sequential WORM SHA-256 Merkle Chain Height** | **`5,577,003` sequential blocks** (`Valid: True` verified genesis-to-head @ `210,220 blocks/sec`) |
| **Live Merkle Head (`Block #5,577,003`)** | `e20a16b7af91510a6ac5217a950eabf6f683f683636517712b3bba93c803d49b` |
| **Historic `Block #1,000,000` `SHA-256` Hash** | `0236b82ec965146931cde942733b7dffbdc2f58ecc95b2812552b0f3e5de5361` (`2026-11-19T01:10:08.056322Z`) |
| **SQLite WORM Database Integrity** | `PRAGMA integrity_check = OK` (`3/3` tamper vectors blocked: `UPDATE`, `DELETE`, `REPLACE`) |
| **Multi-Process Write Concurrency (Arenas 53–54)** | **`16` simultaneous OS writers** (`265.1 blk/s` sustained, `286.3 blk/s` peak, `0` WORM collisions) |
| **Overnight Unattended Endurance Soak (Arena 55)** | **`6.41 hours` (`23,084.5s`)** across `8` concurrent writers (`+4,576,961` blocks @ `198.3 blk/s` sustained, `0` failures) |
| **Adversarial Cyber-Deception Tarpit Defense** | **`36,615,688 / 36,615,688` (`100.00%`)** spoofs trapped in Arena 55 alone (`41.5M+` cumulative \| **`0` actuator bleeds**) |
| **Sub-Cycle Grid Islanding Latency (`< 16.0 ms`)** | **`1,144,243` cycles** in Arena 55 (`max = 8.29 ms` / `8,292.20 µs` under full 8-writer saturation \| **`0` breaches**) |
| **Bounded Multi-Day Storage Architecture** | **`PRAGMA journal_size_limit = 268,435,456` (`256.00 MB` hard WAL cap)** + bounded `TRUNCATE` checkpointing |

---

### 3. Human Out-of-Band Override & Governance Architecture

Project E.B.O.N.Y. never "unlocks" an AI agent to act on a human operator's behalf; advisory AI models remain permanently read-only. When emergency operational intervention is required, named human operators bypass the AI entirely via a separate, out-of-band physical and cryptographic control plane governed by:

1. **Dual-Operator / Role-Bound Cryptographic Authority:** Critical state overrides require named operator authentication using hardware-bound per-epoch keys—never an AI session token.
2. **Deterministic Hardware Safety Ceilings:** Out-of-band human commands remain subject to deterministic `< 16.0 ms` physical hardware interlocks.
3. **Non-Repudiable WORM Attribution:** Every manual override command, operator identity, UTC timestamp, and pre/post telemetry state seals permanently into the SHA-256 Merkle ledger.

---

### 4. Consolidated `SHA-256` Cryptographic Checksum Manifest (`126` Archived Governance Artifacts)

Every governance brief, compliance package, SBIR volume, and empirical Stress Arena receipt listed below is archived in `governance/` and verifiable against its exact `SHA-256` digest:

| Repository Relative Artifact Path | File Size | Verified `SHA-256` Cryptographic Digest |
| :--- | :--- | :--- |
| `governance/architecture/ACTION_ITEMS.json` | `1.0 KB` | `3c9bdd786a31190b85073d0f8b6d90b9254735a2c3483f0109f30d55e544e437` |
| `governance/architecture/BATCH_PATCH_LOG.json` | `14.4 KB` | `1df046003d8ea02a9d36fdbaca179fa54e733141fea35b45e8a225c3aeb95a4d` |
| `governance/architecture/DEEP_AUDIT_REPORT.json` | `141.0 KB` | `889b99ada8f6906583ec7005ca597a61f8ec56e60a32271997101e46ebf0e0e0` |
| `governance/architecture/DOCKET_REGISTRY.json` | `0.8 KB` | `c350144a47ee7e1415e8310c1dcba166cfea161f6fb2e3d196b45f991fd7e4f6` |
| `governance/architecture/EBONY_COMMAND_REGISTRY.json` | `2.0 KB` | `f9278d09fac2fd7df873a615c61e6cba25dd7b1cc92274700c9ac570bec7f697` |
| `governance/architecture/ENGINEERING_CODEX.md` | `1.6 KB` | `f630e1daa276110cf3238c68897dd488973711cbbe49eb1cc76d8ac67b27ac11` |
| `governance/architecture/EXTERNAL_ENGAGEMENTS.json` | `1.5 KB` | `6f724e6b66b0da99a8f1c1da7cd033705b2bc68636ac34cadc063eb077bf0e58` |
| `governance/architecture/MERKLE_AUDIT_LEDGER.json` | `1.5 KB` | `2bd5606246ea4b16f194f37d2de8a6481d81f7a6bf39837b7be6484ee1d01f5f` |
| `governance/architecture/MERKLE_AUTHORIZATION_LEDGER.json` | `10.1 KB` | `f7fb7e7434737343b8c707709304b19426eefb7aa4ee7049d2fb0dc148e9d357` |
| `governance/architecture/SIDEBAR_MODULES.json` | `1.1 KB` | `1217a5aad860497e0c72d75c0f10d58b160af664e93a663ec88131c12118cfb5` |
| `governance/architecture/SOVEREIGN_PARTITION_SPEC.md` | `1.3 KB` | `ef8a2e21fa805e81468cdc2e384f06c5aad65019cb40e4dabcebacef35e1df31` |
| `governance/articles/2026-09-25_sovereign_resilience.md` | `5.2 KB` | `c52743c6a54583eef9d48da0c2ecbee453528a63f0373330b3bd0f736fb4d93f` |
| `governance/audits/2026-11-14_EBONY_System_Hardening_Audit_Certificate.md` | `1.8 KB` | `ebd798ccd84eba0e5b34d41598a881ba6e60620c9b8a560a2f13456dcf24cb86` |
| `governance/audits/2026-11-14_Stress_Arena_10_Master_Certification.md` | `2.3 KB` | `1187cf9ce408f55022f33fa078d89c378f18cdad75fb864848423b9954943789` |
| `governance/audits/2026-11-14_Stress_Arena_11_30Min_Endurance_Certificate.md` | `1.7 KB` | `df0aa5fdf2ce97a77402d6730cda96d72427cfe85bc4743b752502633738ba7e` |
| `governance/audits/2026-11-14_Stress_Arena_12_Real_Modules_Vector_Receipt.md` | `1.0 KB` | `7b75a89d2e4479a11685bb201d3e90fb87acf06b3370752a19c036ae8195e71c` |
| `governance/audits/2026-11-14_Stress_Arena_13_Deep_Import_Sweep_Receipt.md` | `1.0 KB` | `e5efc31b925a6474f516f3424a995c15eacdf2a0c010b8fe23dd526fc1a70262` |
| `governance/audits/2026-11-14_Stress_Arena_14_API_Perimeter_E2E_Receipt.md` | `1.0 KB` | `364ea0aa81d18fdcfd01311aa4f25de90e0e9d7035bc6a2ffb7bd349864f60c3` |
| `governance/audits/2026-11-14_Stress_Arena_1_WAL_WORM_Receipt.md` | `1.0 KB` | `f9b189c82cad8e6a797737048b83e724f24fc12e5b3b0bac2daba62e20836607` |
| `governance/audits/2026-11-14_Stress_Arena_2_Import_Sweep_Receipt.md` | `0.6 KB` | `8ac8fab6e98ff9bdd627f8b5f24529a634cc815eb78def3dd74e702aa3ca068a` |
| `governance/audits/2026-11-14_Stress_Arena_3_Fuzzing_Receipt.md` | `0.7 KB` | `4dc0efaf05ff91b4a7c646e766eefbb773d0544340fa6e5a4748e3d0dc693ec8` |
| `governance/audits/2026-11-14_Stress_Arena_4_Master_Stress_Certificate.md` | `1.1 KB` | `a6f0d96766ff7230b1d1a542e6512cf5e184edbae197ef088557686640e3e5d7` |
| `governance/audits/2026-11-14_Stress_Arena_5_Protocol_Endurance_Receipt.md` | `1.1 KB` | `5c12f13b45192d0eabf9ba97f307e316f2ace56b9f74c292bb0fe36c06395165` |
| `governance/audits/2026-11-14_Stress_Arena_6_Master_Certification.md` | `1.6 KB` | `665b1a8a0426f2ebd32921f9351da8d783872f8b11a994778cc6bb2806991050` |
| `governance/audits/2026-11-14_Stress_Arena_7_MultiProcess_Watchdog_Receipt.md` | `0.8 KB` | `eb68b99a196270e182d80d534e49f5af14176b267e2e4d0e3fec5e417222771b` |
| `governance/audits/2026-11-14_Stress_Arena_8_Complete_Master_Certification.md` | `1.9 KB` | `6fabe20888c794e83fbfd299c7bea52f32ee8233ce026bd3602f15d810233049` |
| `governance/audits/2026-11-14_Stress_Arena_9_Crypto_Parity_Receipt.md` | `1.0 KB` | `08d16fcb2b69d5ee263ef4ef197fecc1dc20c7b6f9ff91d5c597b642db67938d` |
| `governance/audits/2026-11-15_Stress_Arena_16_Overnight_Endurance_Certificate.md` | `2.0 KB` | `a449bc496f4d125994600ece4bcffcf3800def460c71e86df25858081ee6ba56` |
| `governance/audits/2026-11-16_Master_Sovereign_Stress_Verification_Index.md` | `17.1 KB` | `b34ddb50aa9aed024b2eca839796f2e27e11427be5b44aa861b0bbca160655dc` |
| `governance/audits/2026-11-16_Milestone_8f_Sovereign_Architecture_Hardening_Receipt.md` | `1.6 KB` | `f14befe5b4063a3f5be0c8c7af16f03f26b86dfeb8a7b257d9ba8018e2617095` |
| `governance/audits/2026-11-16_Milestone_9_WORM_Merkle_Ingest_C2_HUD_Receipt.md` | `1.4 KB` | `a229ac4916ac2fb81d7a4ddc22a52b42603225a45258c53bb502c902667c788a` |
| `governance/audits/2026-11-16_Stress_Arena_17_UI_Buttons_Callbacks_Receipt.md` | `1.2 KB` | `aa2a721e1242b23e529c5f3d017e977232c3ab17c24c9b0aaf4eff1523d109d9` |
| `governance/audits/2026-11-16_Stress_Arena_18_Concurrent_WORM_Merkle_Cache_Receipt.md` | `1.3 KB` | `0bfa50f83d6d87e3b917abdf596a7445223151f74dfad116e11454011c923978` |
| `governance/audits/2026-11-16_Stress_Arena_19_Live_HTTP_Ingest_Merkle_Burst_Receipt.md` | `1.0 KB` | `6f86497b313323951d9dc9e9ab2e6e9b54bd265522f83bcb062ccf91efabb301` |
| `governance/audits/2026-11-16_Stress_Arena_20_Fault_Injection_Self_Healing_Receipt.md` | `1.0 KB` | `f00d58a37768f4d86cb0fee1aecbd58a68a1e350feb86341e5cac0ecd4e7e576` |
| `governance/audits/2026-11-16_Stress_Arena_21_Adversarial_Fuzzing_SQLi_Receipt.md` | `1.0 KB` | `c60f0506c230c0674e49ad6823e53e98129c8449d14d97280e717d688b2524b0` |
| `governance/audits/2026-11-16_Stress_Arena_22_Closed_Loop_API_C2_HUD_Sync_Receipt.md` | `1.0 KB` | `d7cb806d2715b55c410f433ef2275d7286c6663cc3861ebccc3b0bec282e13aa` |
| `governance/audits/2026-11-16_Stress_Arena_23_8Node_HIL_5000_Block_Scaling_Receipt.md` | `1.0 KB` | `23c751d81f5862f6925434280cde2de4f0b8123f9e25833a3e9be2a61d0e59d7` |
| `governance/audits/2026-11-16_Stress_Arena_24_Dual_Service_Chaos_Recovery_Receipt.md` | `1.0 KB` | `d323ae8392c03d729bbbc1b38320626922188cb66703dc5f06aad8015953fd67` |
| `governance/audits/2026-11-16_Stress_Arena_25_10000_Block_WORM_Merkle_Certification_Receipt.md` | `1.0 KB` | `b411cc0f52cffb391de311dd23e630b1e42a2c84a30878486af7796d31070c6f` |
| `governance/audits/2026-11-16_Stress_Arena_26_Concurrent_WORM_Tamper_Torture_Receipt.md` | `1.2 KB` | `7387879382c92b39535c518c0d25b03fa4c78a8ec130b6350ac67de44e6e64a3` |
| `governance/audits/2026-11-16_Stress_Arena_27_WAL_Checkpoint_LRU_Eviction_Receipt.md` | `1.0 KB` | `53dc116b565da97b741542b8f944a515dca79c540da15563fd54ca5ebf4e33ab` |
| `governance/audits/2026-11-16_Stress_Arena_28_Token_Window_Replay_Defense_Receipt.md` | `0.9 KB` | `739c537f796b9f7e45805e9015f9019f4593d3af29fd1a9d399a532f5bdb93cc` |
| `governance/audits/2026-11-16_Stress_Arena_29_OPSEC_Gatekeeper_13000_Block_Receipt.md` | `1.0 KB` | `cdaef1fd36881feae4fa383cff270971e57e406da04d53182c0520d84a2345e4` |
| `governance/audits/2026-11-16_Stress_Arena_30_Capstone_15000_Block_Gauntlet_Receipt.md` | `1.1 KB` | `e98a56550c3e1c2aaafcd62f6cae19d569b471081894401ecd9e633be6cc1a87` |
| `governance/audits/2026-11-16_Stress_Arena_31_20000_Block_WORM_Merkle_Scaling_Receipt.md` | `1.0 KB` | `f28d328ba9e6d1551209384951c79c99c272f8bef2fc3f6e7b0aac8598672096` |
| `governance/audits/2026-11-16_Stress_Arena_32_MultiProcess_OS_Contention_Receipt.md` | `1.0 KB` | `21ce5f2ba2d24e7159c8c7dd6772904b448d95a7280e3ae5e781b7dcd61e195c` |
| `governance/audits/2026-11-16_Stress_Arena_33_25000_Block_WORM_Merkle_Milestone_Receipt.md` | `1.0 KB` | `e111bf5a02d8ca4478c7693ddc979fad39195038c45d49bbb783a8f3a0b0ee13` |
| `governance/audits/2026-11-16_Stress_Arena_34_MultiKB_Payload_HTTP_Torture_Receipt.md` | `1.0 KB` | `5dcac0874b31bbf99d04b4827ef167223de28c12bab86ae72adf39fc76b46138` |
| `governance/audits/2026-11-16_Stress_Arena_35_30000_Block_WORM_Merkle_Milestone_Receipt.md` | `1.0 KB` | `6d03dc667b98c0e872ecd0397a987a87d30c156824f1d8a93deaedad2d010a71` |
| `governance/audits/2026-11-16_Stress_Arena_36_Master_Verification_Rollup_Receipt.md` | `1.0 KB` | `97cda148f1044ab6a08650d37b178af45f16f6cee264b8905bd6f2d23884831d` |
| `governance/audits/2026-11-16_Stress_Arena_37_40000_Block_WORM_Merkle_Scaling_Receipt.md` | `1.1 KB` | `1d225057e6c0884712548fd4d429daa3dfa65bc4376464336d1e99cb365aeb88` |
| `governance/audits/2026-11-16_Stress_Arena_38_60Min_Full_Stack_Endurance_Soak_Receipt.md` | `1.2 KB` | `4a560514b0c3c929161cd878cf000d18baef72a555394fbadc398698b95d202b` |
| `governance/audits/2026-11-17_Stress_Arena_39_125K_WORM_Ledger_Scaling.md` | `2.3 KB` | `c2d5e974995b279d31e0bc63e8d75434b3c2092fa347b46a1a9529e67108e3ac` |
| `governance/audits/2026-11-17_Stress_Arena_40_Hard_Blackout_WAL_Crash_Recovery.md` | `2.2 KB` | `f9b687709a30e9ca2e1961eed7192f777cd9353e194a8d1c4d63330b8c02fb15` |
| `governance/audits/2026-11-17_Stress_Arena_41_FAA_Telemetry_Tsunami_Rogue_AI_Flood.md` | `2.0 KB` | `b3ca7b1d4cdfddf9cf333c6242e4e0ccae9141f297011501e172853d853bd483` |
| `governance/audits/2026-11-17_Stress_Arena_42_HB2992_Grid_Collapse_BlackStart_Islanding.md` | `1.7 KB` | `4da2ae538804383db0e38617611e7529ea0b9f18983219898c9dc167198afff3` |
| `governance/audits/2026-11-17_Stress_Arena_43_Supply_Chain_AST_Poison_Siege.md` | `1.9 KB` | `2078404f663f50525fa0c4551d6d94287426d8b4ce6b57229e4859cb3cd3deae` |
| `governance/audits/2026-11-17_Stress_Arena_44_EW_Clock_Spoof_Nonce_Replay.md` | `1.9 KB` | `ff934ca9139f44e56aee42ed405db3c225efa174be11f9b4355eb311aac7e5bb` |
| `governance/audits/2026-11-17_Stress_Arena_45_Dual_Service_CrashLoop_Watchdog.md` | `1.5 KB` | `b04b4f96914e5d009811725d42040d8368b03230014bbd77fbc14df9aef8fa70` |
| `governance/audits/2026-11-17_Stress_Arena_46_Active_Cyber_Deception_Tarpit.md` | `2.0 KB` | `f2f61ef9a8949aa34d628764706b7afde88581b2f747f15ca7435c57eaf6fec8` |
| `governance/audits/2026-11-18_Oklahoma_Commerce_Executive_Outreach_Dispatch_Log.md` | `2.6 KB` | `afa71a60e957c7d6c2eaa8b6970341f0f1da79dab6686e63ad77d056b493e553` |
| `governance/audits/2026-11-18_Stress_Arena_47_Cascading_Grid_Collapse_Black_Start.md` | `1.6 KB` | `d44f594dd981853b8f10ab59db51dd3619eeef35ee3e834bb7fc3b1d5c21e1ca` |
| `governance/audits/2026-11-18_Stress_Arena_48_Sustained_10K_WORM_Endurance.md` | `1.7 KB` | `06edbdf0a29991a459b2a6a264327ac7afd5c8ac8014e22c4ae14a74f4a5d49e` |
| `governance/audits/2026-11-18_Stress_Arena_49_Cryptographic_Key_Rotation.md` | `1.6 KB` | `65e7f8befc02c825e4ecebab45644230b718f8deda2ec39c6d1680c310694de4` |
| `governance/audits/2026-11-18_Stress_Arena_50_Forensic_Merkle_Inclusion_Tamper_Audit.md` | `1.6 KB` | `0632ce130d2ac2cf04948fbe88da52cbf239ce6c0748c3ea980364107552f19b` |
| `governance/audits/2026-11-18_Stress_Arena_51_90Min_Redline_Breaking_Point_Siege.md` | `3.3 KB` | `52a9435787bdbddb67bf02ec696813cc47b7c75155d2e6dc107315899e442bb6` |
| `governance/audits/2026-11-18_Stress_Arena_52_Unbounded_MultiProcess_Break_Siege.md` | `1.6 KB` | `eb454123ae6704d387b0237d6cb3281a2af51cdba42bf1beeadc92fe8f76e78e` |
| `governance/audits/2026-11-18_Stress_Arena_53_Hardened_MultiProcess_16_Writer_Siege.md` | `1.5 KB` | `af608b73a816a87fb6a29a7a1b9531824eeb9f66668a9500204daf0e3575e1eb` |
| `governance/audits/2026-11-18_Stress_Arena_54_One_Million_Block_WORM_Milestone.md` | `2.9 KB` | `5cb3300086c0b442d431e996f1182bae57ccbdaa6a3ff38e55288e3da1968ea0` |
| `governance/audits/2026-11-19_Stress_Arena_55_Overnight_0800_Endurance_Soak.md` | `4.6 KB` | `f02ee9bbab1ad172655ed06e5302d60683f9ba3c323a5d67a19ca835d0a1a691` |
| `governance/audits/preflight_full_regression.py` | `1.5 KB` | `f1912400df8e8a2a264fb11bd4600ccd037215b477c4f98e723a5e7b59117994` |
| `governance/briefings/2026-09-25_executive_speaker_track_and_qa_matrix.md` | `14.3 KB` | `d910f1beb70603752cb79fed3518b90b64b32fcd3e51b326be9bbe2b7e488653` |
| `governance/briefings/2026-09-25_oklahoma_commerce_executive_briefing.html` | `17.8 KB` | `5a5d9d5a653a88d7a6d6886b811d06e97efb66c633de0bf5002208d147980f38` |
| `governance/briefings/2026-09-25_oklahoma_commerce_executive_briefing.md` | `6.3 KB` | `cd74be74bb77e151e0ecfeb5fe9dc18d573d17aa8c25740bec07c7dd2af465d5` |
| `governance/briefings/build_briefing_html.py` | `12.8 KB` | `fe07620add3864b30513e3d370609b796d7d12b99e9cbce592e92669746298e9` |
| `governance/briefings/OK_COMMERCE_EXECUTIVE_BRIEFING_2026.md` | `1.2 KB` | `e96429d2f5aa92b84188c5089d48c040173e20e6a976f71a367a268e452e799b` |
| `governance/briefings/OK_COMMERCE_SLIDE_OUTLINE.md` | `1.5 KB` | `a973631d556464cf2e53fbe4713f155c441996a38c290537b0f50136b50d6e78` |
| `governance/briefs/2026-11-17_AFWERX_DIU_Tradewinds_Executive_Transmittal_Letter.md` | `8.3 KB` | `2904eb82a3b87f1fddc787abb372f6adb3a57e98f1bc507791fd6dc94bc77e04` |
| `governance/briefs/2026-11-17_DoD_AFWERX_DIU_Tradewinds_Executive_Capabilities_Brief.md` | `9.3 KB` | `6da0e72675913855a80b393256322e2ad42e2e2d3458839cf5459d69d894dbb3` |
| `governance/briefs/2026-11-17_Oklahoma_Commerce_15Min_Pilot_Scoping_Agenda.md` | `4.5 KB` | `1416c12889435e166410325fc058bc9a7220feffcb48f8258cf8cda52c8df106` |
| `governance/comms/2026-11-14_LinkedIn_TOCTOU_Comment.md` | `0.9 KB` | `f27ce5d81a1690b7df4b58a8720eeff9de81592e4cdd3bc8ec615eba6e2092bf` |
| `governance/compliance/2026-11-16_NIST_SP_800_171_DFARS_252_204_7012_SPRS_110_Evidence_Package.md` | `13.0 KB` | `f2d4cbb7bc6ec21bf415b2c5bd53544d299cba71aff9ea4befe4f6343bba8c14` |
| `governance/contracts/Definitive_LOI_HVF_SignalLink_Executed.md` | `3.2 KB` | `f4ddd48ecff96ddec7c34147ac49b6c1430e237b6d79186f9f4066d39b5b645a` |
| `governance/contracts/SIGNALLINK_INTEGRATION_CONTRACT.md` | `1.2 KB` | `02b78ac6bd05bb5ad98d204ee2de1d38edfce60891bc99a7a1e8ff055fe9da0b` |
| `governance/contracts/SignalLink_Sandbox_Transmission.md` | `0.6 KB` | `55757c0e67ce9e18ce57f3130214870b84a27dc5117bbb460a637f3cac70529e` |
| `governance/Document_Execution_Ledger.md` | `0.6 KB` | `b57aaf3ac201c394ea7fb57b7dfe4de8a472daa5d768d49cff809bceb9e97a8a` |
| `governance/dossiers/2026-11-17_CEO_Level5_Operational_Readiness_Certificate_Master_Dossier_Index.md` | `8.2 KB` | `a0d9451648dfa9a0aa55a3133340b035e4f41441e3e2d402a5fd4ac9e855036f` |
| `governance/evidence/conversation_log.txt` | `35.8 KB` | `8e5f7356513f0df158203bdd0a990136dbe746962f803781c72e403f8fcdc578` |
| `governance/Executive_Communications_Log.md` | `6.9 KB` | `21d4a26726a42dc712c5bd3eb3d18ac44eef1d7406acfd1a8d60d7e82b937eac` |
| `governance/EXECUTIVE_LEDGER_2026.md` | `1.0 KB` | `4a57d4501a4d832e452dcdd6b26dceed98bee6c098279d041f68a9e3226b120b` |
| `governance/Federal_Compliance_Ledger.md` | `0.6 KB` | `45091f91b235c136641813a5e60be67dc34027618db8839d9755a9ad1fa256a6` |
| `governance/generate_fs288_compliance.py` | `6.2 KB` | `fc31f22644e0db35bd04bb8108b1c94e1cbe966b4a256187aca96f5820a448a6` |
| `governance/hvf_financial_doctrine.md` | `0.7 KB` | `0df3f386974f9437ab20f5e3632c84c41948024255f1b7abec22fa917ab68fd6` |
| `governance/ingest_drew_phillips.py` | `3.2 KB` | `ec2588d35149f2baa7dd70f18d1154a051ef6e9c44894bd3dc1b3a177678508c` |
| `governance/legal/MUTUAL_NDA_VANDERPOOL_ENERGY_DESIGN.pdf` | `71.5 KB` | `6060b5263d218997fcaf148c555b172b6614ad999bfe0d407584e869fcbfef1c` |
| `governance/legal/MUTUAL_NDA_VANDERPOOL_ENERGY_DESIGN_FINAL.md` | `3.9 KB` | `7bcea0d4ae87859d1133ef6e70d7c5efb258372c3f3c9aa4631292b2dfb7486f` |
| `governance/legal/temp_nda.html` | `4.3 KB` | `32d9df3ec7e53c9c603ca369da461522bc811a268de9f401d59519a9834c59fb` |
| `governance/record_breach_dossier.py` | `5.1 KB` | `f807f705dd5ff795d4e8cff9d265e8a8935c944f720aff5f645fad433e4a5ed3` |
| `governance/record_compliance_extension.py` | `4.7 KB` | `c97d4674205ff8b10206a40588c024608b1cd1b2c61f970dc16e7053c4bc02e0` |
| `governance/record_final_legal_demand.py` | `4.7 KB` | `4b053d211d478f26b069fa5a007e095ca4373271cd0a6692d8a9d88508135a5e` |
| `governance/sbir/2026-11-16_SBIR_Volume_5_Technical_Empirical_Verification_Appendix.md` | `12.8 KB` | `88381d64aece6396def861f351881c74d709f6291287ad959d31c4dea0f5b414` |
| `governance/security/__pycache__/hvf_security_gateway.cpython-311.pyc` | `3.7 KB` | `f2759fcccc31493852df45312065aa57ba92acc4a76281965f94784e1d30d773` |
| `governance/security/check_keys.py` | `2.2 KB` | `0851ef5952822429de7d5aa96cef2ea4e2531060ef051d6b7fa76c489a2b410c` |
| `governance/security/deploy_blocklist.py` | `16.3 KB` | `b1308049b0cb6d787011e87ef10abe7ea4585f80796ac7c266a32fe3a8a1dc1b` |
| `governance/security/forge_matrix_ssl.py` | `7.2 KB` | `ab4b63ec6cf1f9d71a92cd442cd6f63e6682a776d4d675fa737b20e484ce9c70` |
| `governance/security/gen_pilot_keys.py` | `1.9 KB` | `c62e83d2eb0a54606aede579a5242e26eda95e1e7b44888935cb1051883d4b7d` |
| `governance/security/hvf_cipher_audit.py` | `3.0 KB` | `60fd5360b1dda064cadcf67df59520e2abe98046f80f9e694448980abda35971` |
| `governance/security/hvf_compliance_guard.py` | `3.1 KB` | `6399e136a0613d18b576cc5308f00daa4019143610b44bdbdb0b9d44e8642009` |
| `governance/security/hvf_penetration_test.py` | `2.6 KB` | `89eafa085304855edcce57d681f15e2939bcdb67b3aa049ff9e82787efd60af3` |
| `governance/security/hvf_security.py` | `2.4 KB` | `6c07cde80f9d11cb41fc545bced62c8d7b7ad9b1553c4ad260d4746afd54ef05` |
| `governance/security/hvf_security_audit.py` | `3.5 KB` | `d933388efb5653d139d4dd00bce023c4115bef03ea6f4ddf30b5ba3aef9388bc` |
| `governance/security/hvf_security_gateway.py` | `2.8 KB` | `cd1f75ef79fc276e26ae568c816e66a305fcc76919962acfaa0076d6cde3d89d` |
| `governance/security/hvf_shell_bouncer.ps1` | `0.5 KB` | `c010b2442a8ba8a5a7c29482ffc6da351507afa1c8ef8d5c6e957473a702c0de` |
| `governance/security/hvf_shell_override.ps1` | `5.0 KB` | `6d32bb21012db823463df5df5a8e038c7a708d11c2268a85f170dbf055d81213` |
| `governance/security/kinetic_guillotine_enforcer.py` | `3.9 KB` | `46ad9e6222cbda6a0d7e18bc9695f830e33e11a29eb616df06f9457063a24d31` |
| `governance/security/protocol_lambda_diode.py` | `4.0 KB` | `f509c0f34ed83ec4b748ce27a287c7d279509aa7444463740f5492d691012e38` |
| `governance/security/Sandbox_Credentials_Vault.md` | `0.4 KB` | `6ecaef1410de8db182f458d77348f454d243ed6526c3ae5ac0cea06fdabfdaad` |
| `governance/security/SECURITY_PERIMETER_SPEC.md` | `1.1 KB` | `4fb95db60b265a9dde31680ddf5b48c0d1467287d3d5574cad85fd55f1faf8a4` |
| `governance/security/sovereign_sentinel.py` | `2.6 KB` | `2bf9e74c5f966c9281fc1df0d8fddcbd081c1adf26e73c63515d2a5edef23aa4` |
| `governance/security/tapo_credentials.json` | `0.2 KB` | `a9c39ac3463ee26edd154e047b5ae351184ae32d890f1ffd5482b8d292c45696` |
| `governance/security/test_cleanroom_provenance.py` | `3.0 KB` | `a868f0b949669d6790ef73c2a26d084be39343c114f9b1bf6de4be6d9ae716e8` |
| `governance/security/test_sanitizer.py` | `3.3 KB` | `92a1c3aee9f26d89315a6f500aaf3063533317c830c8536df545a02506708943` |
| `governance/statutes/OK_HB_2992_STATUTORY_DIGEST.md` | `2.0 KB` | `d0dbf26f3fee74ac5490301953135cf714903d6a3edf5f339652b4b31ef052ad` |
| `governance/Strategic_Directive_Federal_Hold.md` | `0.6 KB` | `b1260e2021de2c7a9f9b9fe3dea1f25972435a3c6d60adb4ed9d29738b955d0d` |
| `governance/Treasury_Matrix_SOP.md` | `1.7 KB` | `32778caf85c8f833f612ce42e12da5ab26ed1f72a11a19643719a28a2a0d90f9` |
