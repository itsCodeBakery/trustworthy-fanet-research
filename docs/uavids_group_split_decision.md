# UAVIDS-2025: grouped-fold audit and auxiliary benchmark decision

**Date:** 18 October 2026  
**Evidence:** The researcher ran our exact `scripts/audit_uavids_splits.py` in Google Colab and supplied its full `uavids_split_audit.json`. The uploaded JSON's SHA-256 is `35c600442dcaab8fc3abb5af58c13c1d5d8779585a1e5baf6f14c16d725e865e`. Counts were independently checked for internal consistency; the underlying 122,171-row CSV was **not** executed or uploaded into this repository. Machine-readable record: [uavids_group_split_colab_2026-10-18.json](../evidence/uavids_group_split_colab_2026-10-18.json).

## Verified from user-supplied Colab output

| Quantity | Value |
| --- | ---: |
| Source CSV | Original UAVIDS-2025; previously matched MD5 and SHA-256 |
| Rows, numeric predictors retained | 122,171, 16 |
| Exact repeated **feature** occurrences beyond first | 8,219 |
| Rows belonging to repeated-feature groups | 10,774 |
| Exact feature groups containing conflicting labels | **0** |
| Fold generator | StratifiedGroupKFold(5, shuffle=True, random_state=42) |
| All 5-class labels in every fold's training and test | **Yes** |
| Source addresses present on *both* sides of a fold | **0** |
| Test sample sizes | 22,447; 19,294; 24,491; 25,868; 30,071 |
| Held-out rows with feature fingerprint also present in training | 3; 2; 6; 4; 4 (**19 total**) |
| Smallest class count in any test fold | **793** (Flooding, fold 1) |

All five held-out fold sizes sum to **122,171**, meaning each row is tested once in this 5-fold plan. The 19 cross-fold fingerprint-matched **test rows** correspond to approximately **0.016%** of all held-out rows. The file uses a 64-bit Pandas fingerprint, **not** a cryptographic equality proof; approximate duplicates and other forms of dataset leakage were not tested.

The fold-class mix is visibly uneven (e.g., Flooding test support 793 in fold 1 and 5,962 in fold 3). Aggregate accuracy alone would conceal this; use **per-fold macro-F1, balanced accuracy, per-class recall and raw confusion matrices**, plus pooled out-of-fold summaries.

## Decision

**GO for an *auxiliary*, completed-flow, source-address-disjoint, five-class classification baseline on Colab CPU.**

**NO GO for claiming** independent underlying simulation missions, early attack detection, grey-hole monitoring sufficiency, mission-level false-accusation control or closed-loop route repair from these data. `SrcAddr` is only a **proxy** for provenance grouping. Whole-flow statistics contain later events relative to an early detector. A zero contradictory-label collision count does **not** show causal validity or independent sampling.

## Prespecified auxiliary evaluation contract

- Raw original CSV must match pinned SHA-256 `d50d339f68be7b23f0bf089dd438b20a1835c13182d8641220538121440164d0` before model fitting.
- Drop `FlowID`, `SrcAddr`, `DstAddr`, `SrcPort`, `DstPort` and constant `Protocol` **from every predictor**. The `label` column is prediction target only. The remaining **16 numeric flow-summary fields** are explicitly **post-flow features**.
- Fix **five outer folds**: `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)`, grouped by `SrcAddr`. Split before fitting scales or classifiers. There is **no** hidden development/test reuse for hyperparameter tuning.
- Start with three **predeclared CPU baselines**: majority/prior dummy; standardized class-weighted logistic regression; histogram gradient boosting (fixed 70 iterations, 15 leaves, learning rate 0.1). This is a lightweight feasibility benchmark, not a completed broad SOTA comparison.
- Collect all out-of-fold row predictions, per-fold confusion matrices, macro-F1 and class recall. Report also predictions restricted to test rows whose feature fingerprint does **not** occur in the corresponding train fold, but retain full-fold metrics as primary descriptive offline results. **Do not delete conflicting rows or choose a favorable fold post hoc**.
- Preserve all model and environment versions, execution duration, original dataset hash, label order, and row index/fold assignment.
- No early-detection accuracy or publication performance claim can be made from this auxiliary experiment; the main paper continues to require genuine FAN-GHETS24 sequence inspection and new ns-3 local-observation runs.

## Next command (Google Colab CPU)

```bash
wget -q -O /content/uavids_auxiliary_baselines.py \
  https://raw.githubusercontent.com/itsCodeBakery/trustworthy-fanet-research/main/scripts/uavids_auxiliary_baselines.py
python /content/uavids_auxiliary_baselines.py \
  --data /content/UAVIDS-2025.csv \
  --output /content/uavids_offline_baselines_run1
```

**This step only prepared and smoke-tested the code using synthetic fixtures; no actual UAVIDS model has been trained by the assistant.** The command above is the next optional user-side Colab execution. Results should be shared in full for evidence-based review before further training.
