# FANET experimental protocol

**Protocol:** 0.1 · **State:** proposed, not yet executed  
**System:** UAV/FANET selective-forwarding and grey-hole attacks  
**Mathematical contract:** [study_design.md](study_design.md)

This file supersedes the earlier generic V2X experiment protocol. It follows the supplied UAV research blueprint; parameters are proposed development choices, not validated optima.

## 1. Study controls and separation

Prespecify the primary false-alarm endpoint: fraction of **all-benign held-out missions** containing at least one wrong accusation during H=600 s. Primary alarm-budget target alpha=0.05, subject to frozen-detector and exchangeable benign-calibration assumptions. Main detection endpoint: **exposed attacker episodes** detected within 30 s of first eligible malicious drop, with non-detections and remaining follow-up handled explicitly. A compromised node that never drops an eligible packet is not counted as an exposed detection failure.

Split data **by independent mission family before constructing windows**. Keep benign/attack/channel/policy variants of the same family in the same split. No training, model selection, feature normalization or gate tuning on final test missions. Calibration missions must be separate all-benign families. Use separate local-observation data versus privileged evaluator-only attack truth.

## 2. Simulator settings: pilot candidate

| Parameter | Initial scope |
| --- | --- |
| Mission | M1 3D patrol/search and M2 UAV corridor; M3 ground convoy transfer |
| UAV count | 25 / 50 |
| Nominal speed | 5 / 20 m/s; 35 m/s held-out stress |
| Core traffic | Five UDP flows at 5 / 20 packets/s per flow; 512-byte payload |
| Routing | AODV |
| Radio | Candidate ns-3.43; ad hoc 802.11a 6 Mbit/s, 20 MHz, 16 dBm |
| Channel | Log-distance versus log-distance + Nakagami |
| Attack | 10% eligible relays; onset 120 s; p=0.1/0.3/0.6, 5 s on/15 s off, flow-selective |
| Horizon | 600 s with 30 s route-initialization stage |
| SUMO | M3 *ground vehicle* trajectories only; UAV 3D waypoints independently generated for ns-3 |

The radio defaults and simulator version must be pinned after a successful build. These are synthetic experiment settings, not validated real-world UAV radio models. Use SUMO's correctly projected metre coordinates; never claim SUMO supplies aircraft dynamics.

## 3. Before launching a large simulation run

Acceptance tests must show: (i) a static three-hop line forwards unique application packets, (ii) attack probability 0 has benign forwarding semantics, (iii) deterministic attack correctly drops only eligible network-layer data packets, (iv) natural radio loss is never logged as malicious drop, (v) observer deafness removes witnesses without changing true forwarding, (vi) header matching deduplicates retransmissions and respects observation deadlines, (vii) local avoidance changes next hop only with a valid alternative, and (viii) UAV/SUMO timestamps, coordinates and altitude constraints are coherent.

Run a **small eight-family observability and cost pilot** first. Do not assume a 2,743-run experiment fits CPU budget until runtime/storage is measured.

## 4. Source-derived planned run matrix

| Partition | Design | Runs |
| --- | --- | ---: |
| Train | 32 core cells × 6 benign families | 192 |
| Development | 32 cells × 2 families × 3 states | 192 |
| Calibration | 199 independent all-benign missions | 199 |
| Core test | 32 cells × 5 families × 6 states | 960 |
| Convoy transfer | 16 M3 cells × 5 families × 3 states | 240 |
| Closed-loop | 8 cells × 10 families × 2 states × 6 response policies | 960 |
| **Total planned** | **775 independent mission families** | **2,743** |

A core cell is mission(M1/M2) × UAV count(25/50) × speed(5/20) × load(5/20 packets/s/flow) × channel(C1/C2). These counts are **planned simulator runs**, not GPU training sessions or completed measurements.

## 5. Model comparisons

At minimum compare a fixed watchdog, channel-aware GLM/boosted benign-loss predictor + CUSUM, supervised RF/boosting, supervised GRU/TCN, benign TCN + CUSUM **without** observation gate, and the full observation-aware detector. Audit closest original channel-aware work before claiming exact reimplementation; adaptations must be labelled.

Hold local input availability, train/dev splits, monitoring deadline, resource budget and mission-threshold calibration opportunities comparable. Use five neural training seeds (42–46), and keep independent mission seeds distinct. Do not choose the best trained seed using test outcomes.

## 6. Experiment families

- **E01:** FAN-GHETS24 v2 public temporal benchmark, after true metadata/split/feature audit.
- **E02–E03:** independent core detection and all-benign fading/congestion false accusations.
- **E04–E06:** held-out convoy mission transfer, new attack schedules and 0/10/30/50% *observation-only* witness suppression.
- **E07:** causal closed-loop AODV route-avoidance simulation on fresh trajectories.
- **E08–E10:** model/history/gate/CUSUM/mission-calibration ablations, CPU/monitoring cost, and benign/attack observational ambiguity.
- **E11:** clearly separate UAVIDS-2025 **offline flow** classification, without causal local-monitor or mission-transfer claims.

The primary contrast is the full detector versus **equal-information channel-aware statistical residual CUSUM** at the same complete-mission alarm target. Main outputs: correct-relay exposed detection by 30 s, false accusations per all-benign mission, right-censored delay, gate-open handoff coverage, attack exposure deferred, goodput, timely delivery, outage, route repair, inference latency and memory.

## 7. Calibration and uncertainty

Freeze model, scaler, monitoring gate, deadline, reset rule and CUSUM parameters on train/development data. Score **199 new all-benign calibration missions**; choose mission-max rank threshold at alpha=0.05, with 0.01/0.10 sensitivity. An unattainable finite quantile returns infinity. Do not repair thresholds on shifted test populations; report failures honestly.

Report effect sizes and 95% intervals from at least **2,000 independent mission-family bootstrap draws**, stratified by cell where appropriate and preserving paired variants. Do not count repeated packets, windows, or five model seeds as independent missions. Publish raw numerator/denominator, unobserved attackers, deferral and negative outcomes.

## 8. Milestone gates

**M0:** full-method novelty and observability contract audit → **M1:** public data inventories → **M2–M3:** benign ns-3, 3D/SUMO mobility and correct attack/monitor hooks → **M4:** 8-family pilot → **M5:** leakage-controlled causal features → **M6:** comparators/Kaggle models → **M7:** locked mission calibration → **M8:** independent test/transfer/ablations → **M9:** *fresh* closed-loop evaluation → **M10:** statistical reporting and paper.

No paper-ready performance claim is warranted before these gates. No base-study presentation is required in the repository README.
