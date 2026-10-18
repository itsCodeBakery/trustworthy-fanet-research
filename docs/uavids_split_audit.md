# UAVIDS-2025: identity, duplication, and split-leakage screening

**Evidence date:** 18 October 2026 · **Source:** user-operated Google Colab, output supplied in the conversation. This analysis was **not run remotely by the GitHub assistant**.

**Precondition:** the original CSV in `/content/UAVIDS-2025.csv` matched the Zenodo MD5 and archived SHA-256 and had 122,171 rows, 23 columns, zero missing values and zero exact full-row duplicates.

## Recorded findings

- `FlowID`: **122,171 unique values**, one per row; exclude from all model features. `SrcAddr`: **176** unique; `DstAddr`: **218**; `SrcPort` and `DstPort`: **2** each.
- Excluding `FlowID`, addresses, ports and `label`, pandas found **8,219 repeated feature rows**. This is the **number of repeat occurrences beyond the first**, not 8,219 independent matched pairs. Whether identical feature vectors carry *different labels* or fall on both sides of a proposed test split **remains untested**.
- Source address (`SrcAddr`) grouping: **176 groups**, of which **125 contain multiple classes**. **20,240 rows** occur in source groups carrying just one class; **101,931 rows** occur in multi-class groups. Thus a source address is not generally a perfect class label, but source-label association is a plausible shortcut.
- Destination address (`DstAddr`): **218 groups**, of which **150 are multi-class**. **692 rows** are in pure-class destination groups.
- Source/destination pairs: **16,076 unique groups**, **10,277 multi-class groups**. **29,069 rows** occur in groups with only one label. Adding protocol to the pair grouping changes none of these counts.
- `Protocol` is **UDP for every one of the 122,171 rows**; drop this constant column from predictors.
- `TxPackets == RxPackets + LostPackets` for **0.7990194072243003** of rows (~79.90%). This is a consistency relationship to investigate, not proof of corruption or malicious activity; counts may use different accounting definitions.

## Leakage risk assessment

**Unverified as yet, not a diagnosis of confirmed label leakage.**

A random row split is insufficient as the **primary** evaluation because identical flow-feature values may cross partitions, source identities can correlate with labels, and aggregate flow records may share simulation provenance.

For an *auxiliary offline benchmark*, prefer a **source-address-disjoint** group split as a documented stress test: hold out all records for each selected `SrcAddr` together, preserving five class coverage wherever feasible. The source-address group is **not automatically the physical simulation/mission identity**. Since destinations may be shared and multiple runs may use the same network, even a source-disjoint score cannot establish independent mission transfer.

Do not “deduplicate” away conflicting labels without investigating them. First measure exact feature-vector groups with multiple distinct labels, cross-fold exact feature fingerprint overlaps, and per-class counts for the proposed folds.

A full-flow summary including `MeanDelay/s`, `Throughput/Kbps`, `LostPackets`, and `PacketDropRate` can use measurements made after the first attack. Such fields are permitted *only in a clearly labelled completed-flow classification task*, **not** in the main time-causal FANET detector.

## Next reproducible action

Run [`scripts/audit_uavids_splits.py`](../scripts/audit_uavids_splits.py) in **Colab CPU** against the original file, and report its output.

The script:
1. Measures exact-feature collisions, including groups assigned contradictory class labels.
2. Tries five `StratifiedGroupKFold` partitions that hold entire `SrcAddr` groups together.
3. Reports per-class held-out support, source-group leakage (must be zero) and exact-feature 64-bit hash overlap between train/test.
4. Generates no model scores, trained weights, or paper result.

**Decision gate:** choose/train a baseline only after reviewing class-support feasibility, contradictory-feature labels, and cross-fold duplicate fingerprints. Do not label this source-disjoint evaluation as a validated mission-disjoint benchmark.
