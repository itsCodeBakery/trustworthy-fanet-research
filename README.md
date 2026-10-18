# Observation-Aware Sequential Detection of Selective Forwarding in UAV Networks

**Reproducible research on selective-forwarding attacks and uncertain local monitoring in flying ad hoc networks (FANETs).**

[Research problem](docs/study_design.md) · [Experimental protocol](docs/experiment_protocol.md) · [Reproducibility](docs/reproducibility.md) · [Data registry](datasets/README.md)

> **Status — design phase, 18 October 2026.** This repository contains the scientific and reproducibility contract for an original experimental study. The supplied Overleaf research blueprint has planning utilities, but no completed ns-3/SUMO experiment campaign, trained detector, or measured performance advantage. All empirical claims await execution and verification.

## Research problem

When a compromised UAV relay selectively drops packets, a nearby honest UAV may fail to overhear legitimate forwarding because of fading, congestion, mobility, or monitoring limitations. **A missed forwarding observation is not proof of a malicious drop.** The research question is whether a local detector can identify *exposed* dropping attacks in time while avoiding false accusations over entire missions and withholding judgment when evidence is insufficient.

## Proposed approach

1. **Local monitoring:** use the upstream UAV's successful MAC handoffs, matching overheard relay transmissions, and causally available radio/route context. Simulator ground truth is accessible only to the evaluator.
2. **Benign observation model:** estimate expected unmatched-forwarding fraction from past-only context with a small temporal model; compare against simple and channel-aware statistical predictors.
3. **Evidence gate:** defer unsupported accusations when packet counts or radio monitoring quality are inadequate.
4. **Sequential evidence:** accumulate positive deviations from expected benign forwarding with a one-sided residual score.
5. **Complete-mission alarm calibration:** calibrate on maxima from independent all-benign missions, using a fixed 600 s horizon and an explicitly stated exchangeability assumption.
6. **Local response study:** measure whether temporary next-hop avoidance actually improves timely delivery after accounting for false isolation, route repairs, latency, and outages.

The central comparison is with a strong, equally informed **channel-aware statistical residual/CUSUM** detector. A new classifier architecture is **not** claimed as the contribution; utility must be demonstrated experimentally.

## Study design

| Element | Proposed configuration | Evidence status |
| --- | --- | --- |
| Network | 25/50 UAVs; 3D patrol and corridor-relay missions | Planned |
| Attacks | Selective packet drops at p=0.1/0.3/0.6, on–off, flow-selective | Planned |
| ns-3 | AODV, ad hoc radio, MAC handoff witnesses, network-layer attacks, closed-loop response | Not implemented |
| SUMO | Ground convoy trajectories for a separate UAV-assisted mission-transfer setting | Not implemented |
| Kaggle | Small TCN/GRU and comparable baseline training | Not run |
| Public data | [FAN-GHETS24 v2](https://zenodo.org/records/13692267) | Inventory described in blueprint; full archive not audited |
| Auxiliary data | [UAVIDS-2025](https://zenodo.org/records/15336998) | Offline flow classification only |
| Main endpoint | Exposed-attack detection within 30 s at 5% *all-benign mission* alarm target | Not measured |

SUMO does **not** supply aircraft flight dynamics. It supplies only the ground convoy trajectories; 3D UAV paths are independently constructed for ns-3. Normal ns-3/SUMO workloads are CPU-based; Kaggle GPUs are reserved for compatible learning workloads.

## Planned experiments

The uploaded blueprint specifies **2,743 simulator runs across 775 independent mission families**: 192 training, 192 development, 199 all-benign calibration, 960 core tests, 240 convoy transfer, and 960 closed-loop network response runs. **These are planned counts, not completed experiments.** A small observability and resource-cost pilot must pass before the large simulation grid.

Major outputs: correct-relay detection within 30 s, complete-mission false accusations, monitoring deferral/coverage, right-censored detection delay, goodput, timely packet delivery, outage, routing overhead, and resource use. Evaluate uncertainty over independent mission families—not packet windows or multiple views of the same run.

## Repository structure

```text
configs/                # Initial settings; freeze after pilot and method audit
datasets/               # Public dataset registry and acquisition manifests
manifests/              # Mission families, seeds, split IDs and checksums
mobility/               # 3D UAV waypoints and SUMO-derived ground tracks
src/                    # Causal features, models, decision and evaluation code
simulations/ns3/        # Packet-level UAV networking and relay attack hooks
simulations/sumo/       # Ground convoy trace export
notebooks/              # Kaggle GPU notebooks (to be implemented)
experiments/            # Per-run metadata, configs and auditable status
results/                # Verified measured outputs only
figures/                # Figures reproducible from verified outputs
statistical_analysis/   # Mission-level effects and intervals
manuscript/             # Research manuscript and supplementary materials
tests/                  # Unit, simulator-semantic and leakage tests
docs/                   # Scientific protocol, limitations and reproducibility
```

Directories may currently contain only placeholders. Their presence is not evidence of implemented code or finished experiments.

## Reproduction and research integrity

Installation and run commands will be provided only when **executed and verified**. Every published number must map to exact source revision, environment versions, independent mission IDs, separate training/development/calibration/test partitions, scenario configuration, random seeds, data hashes, prediction/decision traces and generation script.

Privileged simulated drop logs must never enter the deployable detector. Failed experiments, calibration target violations, harmful mitigation outcomes, and negative results will be reported rather than hidden.

## License

See [LICENSE](LICENSE) for repository licensing. Public datasets and third-party dependencies retain their own attribution and license requirements.
