# Experimental protocol

**Version:** 0.1 (planning draft)  
**Status:** PROTOCOL ONLY — not implemented, reviewed, or executed  
**Last updated:** 2026-10-18  
**Scope:** Trustworthy vehicle-to-everything (V2X) learning experiments on Kaggle GPUs and network evaluation with SUMO and ns-3

This protocol specifies how evidence will be collected and audited. It intentionally does **not** fix an algorithm, claim a research gap has been validated, or report results. The final prediction task, network use case, datasets, and scenario ranges remain decisions to be justified and recorded **before** final evaluation.

## 1. Study definition and decision freeze

Before writing substantive model code or accessing final test labels, register the following decisions in this document (or linked version-controlled configurations):

| Required decision | Status | Record required |
| --- | --- | --- |
| Primary research question and falsifiable hypothesis | OPEN | Concrete intended effect and comparison |
| Unit of prediction and label space | OPEN | E.g., message, flow, vehicle, or time window; ground-truth source |
| Target network operation and threat model | OPEN | Legitimate participants, attacker capabilities, assumptions, constraints |
| Primary dataset(s) and permissible usage | OPEN | Canonical URL, version, license, checksums |
| Primary endpoint and operational threshold | OPEN | Metric, direction, aggregation, decision threshold selection |
| Baseline implementations | OPEN | Relevant published and classical competitors; links and parity rules |
| SUMO/ns-3 coupling strategy and supported protocol stack | OPEN | Standalone mobility trace replay versus verified online co-simulation |
| Scenario parameter grid and exclusion criteria | OPEN | Road network, traffic, radio/channel, load, mobility and failure modes |

A later change affecting these decisions must be justified in Git history. Clearly label exploratory analyses separately from confirmatory evaluations. **Do not select a model using final-test outcomes.**

## 2. Evidence chain

The planned workflow is:

```text
Verified dataset manifests / generated simulation scenario manifests
    -> integrity checks and leakage-controlled splits
    -> feature preparation fit on training data only
    -> baseline + candidate training (Kaggle)
    -> fixed validation-driven model and threshold selection
    -> held-out test predictions + resource measurements
    -> documented SUMO mobility trajectories
    -> ns-3 network conditions and outcomes
    -> run-linked analysis, figures, and manuscript tables
```

Whether ns-3 consumes time-stamped SUMO mobility traces or connects to an online mobility adapter will be established by integration tests. There is no claim that SUMO and ns-3 are already connected, or that Kaggle hosts the simulation stack.

## 3. Data integrity, partitions, and leakage prevention

1. Register canonical source, version/retrieval date, license, file SHA-256, label provenance, and permitted use for each dataset.
2. Check missing/corrupt samples, duplicates or near-duplicates where appropriate, class distributions, and overlaps between partitions.
3. Define the **independence unit** before splitting. For example, packets from one session, sequential windows from one vehicle/trip, or observations from one simulated run may be highly correlated.
4. Split by independent entities and/or chronologically as dictated by the intended deployment. Never randomly split correlated windows or records across training and final test.
5. Fit preprocessing, normalization, feature selectors, calibrators, and thresholds **only on allowed training/validation partitions**.
6. Preserve frozen split manifests with entity IDs (or privacy-preserving hashes), split logic, grouping rules, seed, and SHA-256 checksums.
7. If multiple datasets/scenarios are used, distinguish within-domain, cross-domain, unseen-condition, and temporal evaluations; ensure no overlap in data generation or identities invalidates a transfer claim.
8. Never relabel or synthetically augment the held-out evaluation partition for the purpose of improving its score. Any simulation ground-truth generation must be independently reproducible.

## 4. Training and baseline comparison (Kaggle)

All reported methods should use comparable information access, train/validation/test partitions, and a documented compute budget.

- Freeze feature definitions, labels, normalization, partitions, and evaluation scripts across methods.
- Record model configuration, optimizer, batch size, learning-rate schedule, early-stopping criteria, checkpoint-selection criterion, and inference-time preprocessing.
- Run a smoke test on a small training subset before extensive training, without reporting it as paper evidence.
- For each principal comparison, use **at least five distinct training seeds** when computationally feasible; if not, disclose the actual count and limit claims accordingly. Repeat baseline runs too, unless stable deterministic evaluation or official reproducible artifacts justify an exception.
- Track GPU type, driver/CUDA/PyTorch versions, runtime, peak GPU memory, hardware-dependent throughput, and inference latency. Do not compare cross-device latency as if it were controlled.
- Save predictions with sample IDs and original ground truth for auditing; save training logs and a per-run manifest. Keep bulky checkpoints outside Git with a content hash and access reference.
- Hyperparameter tuning is performed on train/validation only, under a recorded budget. Repeated inspection of final test data is prohibited.

## 5. Evaluation design

Metrics are **conditional on the actual task**, and must be locked in the study definition before confirmatory evaluation.

| Study layer | Candidate measurements (choose if applicable) | Reporting requirements |
| --- | --- | --- |
| Supervised detection/classification | Macro-F1, class-wise recall, precision, balanced accuracy, AUROC, AUPRC | Include class support, positive-class prevalence, full confusion matrix and threshold selection |
| Rare-event or open-world detection | AUPRC, TPR at fixed FPR, FPR at fixed TPR, unknown-detection performance | Clearly separate known and unseen classes; validation-only threshold selection |
| Trust/risk estimation | Calibration (ECE/Brier), selective risk versus coverage, abstention rate | Define target event, calibration bins, error/risk costs and operational action |
| Network operation | Packet delivery ratio, end-to-end delay, throughput, channel overhead, loss/outage rate | Define denominator, traffic generator, observation window and confidence intervals |
| Runtime/footprint | Training cost, inference latency, memory, model size, transmitted metadata bytes | Record device, batch size, warmup, repetitions and timing boundary |

Do not publish metrics that do not match the implemented task. Under class imbalance, avoid accuracy-only claims.

## 6. Minimum experimental programme

These are **planned experiment families**, not performed experiments. Specific configurations and hypotheses must be defined before running.

| ID | Family | Purpose | Required control |
| --- | --- | --- | --- |
| EXP-00 | Input, split, and environment verification | Detect leakage, invalid labels and runtime mismatch | Checksums and audit logs |
| EXP-01 | Baseline comparisons | Establish improvements relative to relevant competitive approaches | Same data, information access, and fair tuning budget |
| EXP-02 | Core-method evaluation | Estimate the candidate method's primary effect | Frozen endpoint, partitions, thresholds and seeds |
| EXP-03 | Ablations | Attribute effects to individual proposed components | Identical pipeline except the ablated component |
| EXP-04 | Distribution shift | Evaluate unseen traffic, mobility, topology or attack conditions *as relevant* | Shift defined independently of final test performance |
| EXP-05 | Sensitivity and robustness | Study hyperparameter, noise, missingness and resource sensitivity | Predeclared sweep ranges and matched seeds |
| EXP-06 | Cost and scalability | Evaluate GPU and runtime cost and compute / communication footprint | Fixed instrumentation and scaling axes |
| SIM-01 | SUMO mobility validation | Produce reproducible vehicle trajectories | Fixed map, demand, routes, seed and mobility units |
| SIM-02 | ns-3 link/network benchmark | Measure communication outcomes without candidate method | Fixed radio stack, channel, application traffic and seed |
| SIM-03 | Integrated comparison | Compare candidate and baseline decisions under shared mobility/network conditions | Verified mobility import or co-simulation, time synchronization, paired scenarios |
| STAT-01 | Statistical and failure analysis | Assess variation, uncertainty and failure modes | Independent replication units and linked raw measurements |

A study need not include an irrelevant family, but any omitted family or simulation constraint must be disclosed.

## 7. SUMO and ns-3 fidelity requirements

### SUMO

Record: exact SUMO version; road-network source and network hash; coordinate system; route-generation rules; vehicle classes; departures; car-following/lane-change settings; random seed; traffic demand; and time step.

Validate: nonempty trajectories, vehicle counts, vehicle entry/exit times, spatial bounds, and exported timestamps. Retain mobility scenario manifests and hashes for generated maps/routes (not large trace files in Git).

### ns-3

Record: exact ns-3 release/commit and build flags; mobility configuration; communication standard and protocol stack; PHY/MAC and channel configuration; propagation/loss models; transmission power; packet generation; congestion/load; seeds/run indices; warmup and observation duration; and packet-trace settings.

Validate independently: packet generation/reception counts, timestamp alignment, units, route continuity, and accounting for dropped messages. Do not label a generic wireless configuration as a particular V2X radio standard without implementing and verifying the corresponding stack.

### Integration gate

Before SIM-03, create a small end-to-end integration test proving that the intended vehicle IDs, coordinate transforms, timestamps, and mobility updates are interpreted correctly. Document any differences between offline trace replay and online coupling. **An integration that has not passed this gate cannot support cross-layer performance claims.**

## 8. Statistical plan

- Experimental replication must use **independent training runs** and/or **independent simulation seeds/scenarios**. Packets within one run and consecutive frames from the same trip are not independent samples.
- Report per-run values and mean/standard deviation when appropriate, plus a 95% confidence interval computed at the correct independent unit (e.g., seed or scenario, or a clustered bootstrap).
- Prefer **paired comparisons** when methods are evaluated on identical split IDs, mobility traces, network scenarios and seeds. Preserve paired difference arrays.
- Choose a comparison test and multiple-testing correction *before* the confirmatory analysis. Check assumptions; do not substitute packet-level pseudo-replication for independent scenario replication.
- Report effect sizes and uncertainty, including negative results, not just p-values. Keep exploratory visualizations identified as exploratory.
- Provide per-class failures, adverse network conditions, and limits to external validity; simulated improvements do not establish on-road deployment performance.

## 9. Per-run manifest specification

Every executed run will require a machine-readable record using the following fields (the executable validator and schema will be added with implementation code):

```yaml
run_id: "<unique run identifier>"
status: "planned | running | completed | failed | invalid"
experiment_id: "EXP-xx | SIM-xx | STAT-xx"
git_commit: "<full commit SHA>"
script_or_notebook_revision: "<revision/path>"
utc_started_at: "<ISO-8601 UTC timestamp>"
utc_finished_at: "<ISO-8601 UTC timestamp or null>"
dataset_manifest: "<path and SHA-256>"
split_manifest: "<path and SHA-256>"
config_path: "<versioned config path>"
random_seeds: {}
environment:
  platform: "<Kaggle / local / other>"
  hardware: "<exact host or GPU>"
  dependencies: "<lockfile / versions>"
  sumo_version: "<if used>"
  ns3_revision: "<if used>"
execution_command: "<exact invocation>"
inputs: []
outputs: []
metrics_file: "<path or URI and SHA-256>"
warnings: []
notes: "<limitations and deviations>"
```

This example is a specification, **not a real experiment record**. The schema will become strict and validated in the next implementation phase; fields irrelevant to a run type may be explicitly null.

## 10. Release / reporting checklist

A result may be cited in the manuscript only when:

- [ ] Its exact input partition, scenario/configuration, seed(s) and commit are recorded.
- [ ] Executed source matches the repository version, and any notebook edits are archived.
- [ ] It passed integrity checks for labels, partition overlap, and metric computation.
- [ ] Its run manifests and raw predictions or network event summaries can be retrieved.
- [ ] Figures/tables derive from recorded values; no hand-edited or fabricated numbers.
- [ ] Statistical intervals, experimental counts, and aggregation units are stated.
- [ ] The repository provides verified instructions to rerun the associated analysis.
- [ ] Limitations, failures, and unperformed experiments are reported transparently.

## 11. Open decisions for the next stage

Before experiments are coded, explicitly settle: **the exact research question**, outcome label/decision, verified dataset availability, benchmark comparisons, primary statistical endpoint, and network simulator integration mode. This document is a reproducibility contract, not evidence of a finished methodology.
