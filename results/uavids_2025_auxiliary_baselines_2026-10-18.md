# UAVIDS-2025 — audited five-fold auxiliary baselines

**Date:** 2026-10-18. **Execution:** Google Colab run by the researcher; aggregate JSON uploaded to this conversation. **Review:** confusion-matrix arithmetic independently checked here. **Not independently rerun or trained here.**

- Uploaded result file: `offline_fivefold_metrics.json`, SHA-256 `e39cb29c9f43e39a83f35a6f48f0cc35ea64d5b53c3ac86a5313ebf8af2df4f7`.
- Verified original dataset SHA-256: `d50d339f68be7b23f0bf089dd438b20a1835c13182d8641220538121440164d0`.
- Existing script: [`scripts/uavids_auxiliary_baselines.py`](../scripts/uavids_auxiliary_baselines.py), introduced in commit `2a26347c53d1c9e09334c10336973550700131dd`.
- Environment reported by the uploaded output: Python 3.13.16, pandas 2.2.3, numpy 2.1.3, scikit-learn 1.6.1.
- **Scope:** 122,171 completed-flow rows, 5 classes, 16 numeric full-flow features. Not an early/online local UAV forwarding-witness experiment.

## Validations

All **15** model-fold confusion matrices are 5-by-5, their row sums match class supports, totals match the reported fold test sizes, and confusion-matrix accuracy matches the supplied metrics. Five held-out test sizes (22,447; 19,294; 24,491; 25,868; 30,071) sum to 122,171; no source address is shared across train/test within a fold, as reported by the Colab script. The corresponding filtered matrices remove **3/2/6/4/4 = 19** test samples with a feature fingerprint also found in training. This is a 64-bit fingerprint screen, not exhaustive near-duplicate exclusion.

## Results

| Method | Mean fold macro-F1 | Mean fold accuracy | Pooled OOF macro-F1 | Pooled OOF accuracy |
| --- | ---: | ---: | ---: | ---: |
| Majority/prior dummy | 5.56% | 16.46% | 11.22% | 17.00% |
| Balanced logistic regression | 81.00% | 82.05% | 82.35% | 82.08% |
| **Histogram gradient boosting** | **94.15%** | **94.32%** | **94.51%** | **94.35%** |

The unweighted fold mean and pooled out-of-fold metrics answer **different aggregation questions**. Dummy chooses different majority labels in different folds, accounting for the large mean-versus-pooled difference. The HGB fold macro-F1 series was **93.95%, 93.24%, 94.81%, 94.70%, 94.06%**, with a descriptive fold-to-fold standard deviation of **0.64 percentage points**. Five overlapping training folds are not five independent confidence-interval replicates.

## Main error pattern

The pooled HGB confusion matrix (true class rows, predicted class columns) is:

| True \ Predicted | Blackhole | Flooding | Normal | Sybil | Wormhole |
| --- | ---: | ---: | ---: | ---: | ---: |
| Blackhole | 22161 | 13 | 41 | 0 | **3895** |
| Flooding | 2 | 18835 | 1 | 770 | 118 |
| Normal | 25 | 1 | 25858 | 1 | 287 |
| Sybil | 3 | 362 | 2 | 23664 | 46 |
| Wormhole | **853** | 120 | 349 | 8 | 24756 |

HGB correctly classified **115,274/122,171**, leaving **6,897** wrong. The weakest recall is **Blackhole: 22,161/26,110 = 84.88%**. **3,895** Blackhole samples were called Wormhole; **853** Wormhole samples were called Blackhole. Together, these two directions cause **4,748/6,897 = 68.84% of HGB's mistakes**. Other HGB class recalls: Flooding 95.48%, Normal 98.80%, Sybil 98.28%, Wormhole 94.90%.

Removing the 19 test rows with train-set exact feature fingerprints leaves essentially unchanged pooled HGB accuracy (94.35%) and macro-F1 (94.51%). This does **not** rule out other data shortcuts.

## Scientific boundary

Identifiers (`FlowID`, source/destination addresses and ports) and constant `Protocol` were not used. However, `PacketDropRate`, `LostPackets`, throughput and delay are **full-flow statistics** and can contain evidence unavailable at early decision time. The `SrcAddr` split is a grouping **proxy**, not a verified independent simulator/mission ID. It remains possible that multiple addresses share the same simulation environment, attack setup or statistical signature.

**Verdict: PASS as an auxiliary offline, five-class completed-flow benchmark.** It **does not** show a 94% result for the paper's proposed FANET sequential selective-forwarding detector. It cannot establish detection latency, deferral, all-benign mission false-accusation calibration, independent mission transfer, or post-decision route recovery.

**Next research priority:** inspect actual FAN-GHETS24 v2 Parquet/JSON metadata for feature timing and simulation-family provenance; then run the minimal 3-hop ns-3 observer-deafness pilot. This is more informative for the main paper than additional Kaggle model tuning on UAVIDS.
