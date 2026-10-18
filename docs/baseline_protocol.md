# Reproduction and fairness contract — original comparators

**Status:** pre-implementation protocol. No named literature model has yet been reproduced in this repository.

The primary task is **per local-monitor–relay pair** packet-forwarding witness analysis in a mobile FANET. A baseline with an entirely different sensing topology, full-simulation oracle or post-flow labels must not be presented as directly comparable.

## Comparison tracks

### Track A — equal-information, on our newly generated ns-3 local-monitor task

All methods see the **same successful handoffs**, overheard forwarding witnesses, causal route/radio context, times and masks, on identical mission families. Detector-selected thresholds are tuned before independent test. All suitable detectors receive the **same independent whole-benign-mission calibration opportunity**, not only our proposed model.

| ID | Comparator | Required implementation | What it isolates |
| --- | --- | --- | --- |
| A0 | Simple watchdog | Eligible handoffs, missed witnesses, fixed score; mission-calibrated threshold | Naive monitoring |
| A1 | Channel-aware statistical residual + CUSUM **PRIMARY** | GLM and boosted benign-loss models, local context, exact same gating options; frozen residual and one-sided accumulation | Channel-aware non-neural control |
| A2 | CAD-inspired local adaptation | Observable loss correction and threshold based only on the same upstream information; **label adaptation** because original uses probes/ACK and bidirectional observations | Historical channel-aware idea within matched evidence |
| A3 | CRS-A-inspired local adaptation | Channel-corrected reputation scoring without unavailable sink or extra second-hand reputation; **label adaptation** | Historical adaptive reputation idea within matched evidence |
| A4 | Supervised RF / boosted trees | Causal summaries, equal training budgets, mission-max score calibration | Discriminative tabular control |
| A5 | Supervised GRU / TCN | Exact same strictly past-only 16 s observation history; 5 model seeds; mission-calibrated threshold | Temporal neural classifier |
| A6 | Confidence-defer temporal CNN | Prefix-based confidence decision analogous to FAN-GHETS24 technical validation, using our allowed local features; distinguish its deferral from monitoring eligibility | **Must-have:** confidence-only deferral control |
| A7 | Benign TCN + residual CUSUM, no gate | Same model/training/calibration except removed monitoring gate | Gate-specific ablation |
| A8 | Benign TCN + residual CUSUM + observation gate | Candidate full method | Candidate, not automatic winner |
| A9 | Statistical residual + CUSUM + observation gate | Same gate as A8, statistical predictor as A1 | **Must-have:** detect whether gate gains occur without a neural model |

**Explicit fair comparison:** report A1/A7/A8/A9 with their scores, gate coverage, actual test false accusations and exposed attack detection. If A9 matches A8, the innovation is not neural network capacity.

### Track B — faithful original-protocol or public native reproduction

- **CAD2010 full:** channel model, signed PROBE/ACK exchange, upstream/downstream traffic monitoring, threshold, reaction; account for probe bytes, route information and any authentication overhead. Only call it **faithful** after reviewing and implementing those assumptions.
- **CRS-A2016 full:** local and second-hand reputation exchange, collaborative/sink decision, adaptive estimation and routing response, network participation cost; **not** an equal-input competitor unless extra information access is explicitly priced or disabled and the modified method is renamed.
- **FAN-GHETS24 2025 native:** use **versioned v2** dataset and published prefix-based technical validation where its actual features, code and splits permit. Its confidence-only deferral is established prior work.
- **2026 TAR-GHD:** once full method and split are verified, classify as reproducible public sequence baseline or clearly documented local-input adaptation; do not invent benchmark scores when code/data unavailable.
- **FL-IDS/FSFL-IDS/FedGraph-ID:** separate **federated/privacy/Byzantine** comparison track only where the same input/target and transmitted telemetry costs can be meaningfully recreated. Otherwise cite as related original work without cross-protocol numerical ranking.

### Track C — causal response in new ns-3 missions

Compare ordinary AODV/no security response, a matched local statistical alert-and-avoid policy, candidate alert-and-avoid policy, forced/controlled avoidance for testing, and an **explicitly privileged** oracle upper bound. Each method **must change route selection in its own fresh ns-3 run**; do not replay frozen decisions from a different route trajectory.

## Shared calibration and experimental control

1. Hold independent mission-family IDs and split membership fixed across compared methods. Never random-split packet windows across mission families.
2. Use the same permitted observations, preprocessing split, monitoring deadlines, packet header bytes, application loads and inference time limits.
3. Tune model and gate hyperparameters *only* on development. For all suitable methods, fix decision and calculate mission maxima over the **same population** of 199 independent benign calibration missions.
4. Target nominal alpha=0.05. The actual **held-out benign mission false-accusation rate may differ** and must be reported. At equal target, compare correct attacked-relay detection by 30 s, false accusation, delay and coverage jointly.
5. Separate confidence-based defer vs evidence-quality gating. Both may defer, but record the **distinct reasons**, covered eligible handoffs and malicious exposure missed by each.
6. Use original labels, loss mechanisms, and monitors. Never use privileged true drop reasons or future packet observations as input.
7. For 5 neural seeds, report all runs and do not count them as independent physical families. Use independent mission-family confidence intervals (>=2,000 paired/bootstrap replications as specified) and raw denominators.
8. When an original model cannot be faithfully reproduced, identify the missing code, unavailable sensor measurements or version-specific assumptions. **Do not print the source's reported F1 alongside ours as a common leaderboard.**

## Acceptance checks before coding baselines

- [ ] Local event schema and offline evaluator label schema finalized
- [ ] Static three-hop monitor hears and matches forwarding when it should
- [ ] Observation-only missing witness manipulation leaves privileged forward truth intact
- [ ] Confirmed honest wireless loss does not imply a malicious-drop label
- [ ] Labels and attack IDs cannot enter model features
- [ ] Baselines' information, latency and overhead budgets logged
- [ ] Native/public benchmark methodology distinguished from local-data adaptation
- [ ] Current 2026 TAR-GHD method checked or flagged unresolved before paper novelty freeze

Baseline IDs in this contract are **implementation targets only**; no output checkpoints, performance results or source-code parity are asserted.
