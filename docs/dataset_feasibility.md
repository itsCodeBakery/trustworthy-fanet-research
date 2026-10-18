# Step 6 — Public-data feasibility and provenance audit

**Date:** 18 October 2026  
**Status:** SOURCE/ARCHIVE METADATA AUDIT + SOFTWARE SMOKE TESTS. **No public dataset archive was downloaded in this session; no classifier or network simulator was executed.**  
**Research scope:** local observation-aware selective-forwarding detection on independent UAV/FANET missions.

## Audit provenance and what was actually checked

Sources inspected:

1. The provided `UAV_FANET_Research_Overleaf_Package.zip` (SHA-256 `6640605e9eb3bd3066b6bfc8e08a40bfa268c0f86e5c4d641b836545eb52891a`). Package inventories `evidence/zenodo_13692267_inventory.json`, `evidence/zenodo_15336998_inventory.json`, `evidence/public_data_audit.json`, `VERIFICATION.md`, and dataset-acquisition scripts were examined. The accompanying PDF was consulted for its planned dataset roles. **Archived assertions are identified as such, not represented as a fresh download.**
2. The [FAN-GHETS24 original 2025 Scientific Data article](https://www.nature.com/articles/s41597-025-05560-1) (including Simulation, Information Logging, Dataset Creation, Data Records and Technical Validation sections).
3. The publisher-hosted [versioned FAN-GHETS24 v2 record](https://zenodo.org/records/13692267) as available via indexed public record (the direct live record API returned access errors in this session). This is deliberately separate from the [v1 record](https://zenodo.org/records/13315419) cited in the journal descriptor.
4. The publisher-hosted [UAVIDS-2025 v1 Zenodo record](https://zenodo.org/records/15336998), including dataset description, original CSV file and its published MD5.
5. A fresh local software verification of our audit utility `scripts/verify_public_data.py`: **3 unittest cases passed**, covering manifest integrity/duplicate keys, altered-file detection, CSV label/missing/duplicate counts and checksum mismatch handling. These used **clearly labelled synthetic test fixtures**, not evaluation data.

The package ZIP contains **no downloaded FAN-GHETS24 Parquet/JSON samples and no original UAVIDS-2025.csv bytes**. This step re-ran *metadata inventory sum checks*, not the previous package author's full CSV audit. The package `VERIFICATION.md` reports that the CSV was downloaded and hashed during its earlier preparation. The original CSV's local bytes were **not independently re-hashed here** because the current downloaded file was unavailable. No public-data performance estimate is made.

## 1. FAN-GHETS24 v2: what the source actually provides

**Bibliography:**

- Hutchins, Aniello, Gerding and Halak, *A flying ad-hoc network dataset for early time series classification of grey hole attacks*, **Scientific Data** 12, article 1431 (2025), DOI [10.1038/s41597-025-05560-1](https://doi.org/10.1038/s41597-025-05560-1).
- **Pinned intended data:** [Zenodo 13692267](https://zenodo.org/records/13692267), DOI [10.5281/zenodo.13692267](https://doi.org/10.5281/zenodo.13692267), labelled **v2** on the public record. The paper's data-availability link instead points to record **13315419 (v1)**. Do not conflate these distinct archives/sizes or assume feature-level version equivalence without sample inspection.
- Archived v2 manifest: **72 entries**, **18,648,943,241 bytes**, declared CC BY 4.0. The 72 sizes sum exactly to the archived total and the keys are unique. Archive manifest SHA-256: `613f7ee80f442d82ff25cecf9df318616cfa4300255dd46c259f5e05951c3c8f`. **Zero downloaded source files checked** in this Step 6 execution.

**Published dataset contents, not our sample-level verification:**

- **31,910 labelled sequences across 12 classes** (benign plus attack type/intensity combinations).
- Each sequence contains **25 engineered features per time step**: **8 continuous and 17 categorical/binary**. The paper explains locally witnessed traffic, time differences, TTL and Packet ID, relative distance/direction, AODV packet type and anonymized addresses.
- Source raw simulation is ns-3 with 24 mobile UAVs plus end components and multiple simulation configurations. Benign **evaluation nodes** collect traffic they sent, received, or *witnessed via promiscuous mode*; each evaluation–subject pair contributes a time series. This receiver-local collection **already exists in prior work**.
- A Parquet sequence `example_host_data_srID.parquet` is paired with `example_host_data_srID.json`. The JSON contains its class, sequence length, feature-type information and **attack-point annotations**. Attack points/privileged class labels are offline evaluation/supervision metadata, not legal deployable predictor inputs.
- The source describes a published **80%/10%/10% sequence-level train/validation/test split**, but the visible article does **not establish that all sequences from the same underlying physical simulation are assigned to the same split**. This is an **unverified grouping property**, not proof of leakage.
- The source explains that its anonymization removes some routing/network-wide context. Packet identity and temporal order are available within the original logged perspective, but the published engineered samples have **not yet been shown to expose a validated MAC handoff-success indicator**, a packet forwarding deadline, monitor transmit-busy fraction, authenticated witness receipt, or independent underlying *mission family* ID.

**Feasibility verdict: CONDITIONAL for the PUBLIC temporal benchmark; NOT READY for the main complete-mission calibration and causal response study.**

Do **not** claim that the public sequences lack forwarding witnesses: the paper explicitly documents witnessed observations. Also do not infer that the 25 features reproduce the new detector's full required monitoring semantics. Inspect at least one real v2 Parquet/JSON pair and any source-run manifest before feature mapping. Use a separately declared reduced common-feature model where any input is absent; never fabricate monitoring signals from attack annotations or simulator truth.

**Resource requirement:** ~18.65 GB *compressed*. Multiple archive parts, repair output, decompressed files and Parquet sharding may coexist. Disk/RAM and extraction needs must be measured before download. Avoid committing archive parts to Git or assuming the dataset fits inside a Kaggle notebook without a prepared source transfer.

## 2. UAVIDS-2025 v1: what the source actually provides

**Original record:** [Zenodo 15336998](https://zenodo.org/records/15336998), DOI [10.5281/zenodo.15336998](https://doi.org/10.5281/zenodo.15336998). The public record describes ns-3.24 simulation, BOID-style UAV motion, AODV, 802.11ac, Nakagami, and five flow-level traffic categories. These source descriptions are **not field validation**.

**File record:** one `UAVIDS-2025.csv`, **20,054,667 bytes**, published `md5:ec84ed5390d5de42b07e8a011709ff82`, archived license **CC BY 4.0**. The research package's *previously executed* audit reports original-file **SHA-256 `d50d339f68be7b23f0bf089dd438b20a1835c13182d8641220538121440164d0`**.

| Label in archived original CSV audit | Number of records |
| --- | ---: |
| Normal Traffic | 26,172 |
| Blackhole Attack | 26,110 |
| Wormhole Attack | 26,086 |
| Sybil Attack | 24,077 |
| Flooding Attack | 19,726 |
| **Total** | **122,171** |

The package records **22 non-label columns** and no missing cells/exact full-row duplicates in the original file. The listed columns are:

`FlowID, FlowDuration/s, SrcAddr, SrcPort, DstAddr, DstPort, Protocol, TxPackets, RxPackets, LostPackets, TxBytes, RxBytes, TxPacketRate/s, RxPacketRate/s, TxByteRate/s, RxByteRate/s, MeanDelay/s, MeanJitter/s, Throughput/Kbps, MeanPacketSize, PacketDropRate, AverageHopCount, label`.

**What is missing for our primary task:** the archived column list has no per-packet event timestamps, MAC handoff success, locally overheard forwarding witness, malicious-vs-radio drop truth or independent mission family ID. Many aggregate columns (e.g., total lost packets, mean delay, throughput and full-flow drop rate) depend on **future information relative to a proposed early packet decision**. They must not be repurposed as causal predictors or as evidence of a 30-second early-detection system.

**Attack alignment:** blackhole is not automatically a labelled *selective-forwarding* episode with known exposure/onset. UAVIDS-2025 is suitable for a clearly identified **offline end-of-flow classification sensitivity benchmark**, preferably after removing source/destination identifiers and auditing identity leakage, but **NOT** the main false-accusation/monitor-deafness/route-avoidance dataset.

**Feasibility verdict: CONDITIONAL GO for an auxiliary Kaggle flow-classification baseline only.** Its raw file must be downloaded, hashed and rerun through the version-controlled audit utility to upgrade archived claims to freshly verified original-file evidence.

## 3. Why new ns-3 traces are scientifically necessary

The *primary* planned detector requires proof of:

1. A successful **local upstream MAC handoff** for each eligible distinct packet, with the forwarding observation deadline allowed to mature;
2. A locally overheard **forwarding witness** (or explicit missing witness, **not** a malicious-drop label);
3. Local route/channel context measured and available **before** each decision;
4. An independent **evaluator-only** true forwarding / malicious-drop / radio loss reason code;
5. Source mission identity, scenario/seed, split and full benign mission horizon sufficient to perform complete-mission false-accusation calibration;
6. **Causal closed-loop** packet delivery, routing changes, false isolation and outages *after* a detector changes its next-hop avoidance policy.

Neither uploaded archive's public-data manifest proves all six. The published FAN-GHETS24 packet witness setup is a valuable reference for our pilot, **not** a substitute for verifying complete-mission calibration and 1–6 with a new ns-3 run.

## 4. Source-to-claim mapping and gating

| Claim or experiment | FAN-GHETS24 v2 | UAVIDS-2025 v1 | New ns-3 |
| --- | --- | --- | --- |
| Public offline early grey-hole time-series classification | **Conditional yes**, after actual sample schema/grouping audit | No | Possible secondary |
| Offline normal vs multiple attack-flow classification | Different task; not direct | **Conditional yes** | Not needed |
| Local packet observation / witnessed packet logs | **Published design exists**; sample-level trace semantics unverified | No | **Must verify in pilot** |
| Receiver-only successful MAC handoff and mature missing witness | Unproven in engineered 25-feature v2 schema | No | **Required** |
| Independent complete-mission benign maxima/calibration | Group identity and mission horizon unverified | No | **Required** |
| Observation-quality gate, wrong-relay deferral and attack exposure | Partial local context; full gate inputs unverified | No | **Required** |
| Causal route avoidance changing delivery and outage | Frozen offline sequences cannot evaluate | Frozen flow rows cannot evaluate | **Required fresh closed-loop runs** |

See machine-readable [dataset feature feasibility matrix](../evidence/dataset_feature_feasibility.csv).

## 5. Exact acquisition and acceptance gates (not yet passed)

### Small UAVIDS file — finish direct original-file audit first

1. Retrieve `UAVIDS-2025.csv` from the pinned [Zenodo release](https://zenodo.org/records/15336998) to external raw-data storage. The file must be 20,054,667 bytes.
2. Execute `python scripts/verify_public_data.py csv /path/to/UAVIDS-2025.csv --expected-md5 ec84ed5390d5de42b07e8a011709ff82 --expected-sha256 d50d339f68be7b23f0bf089dd438b20a1835c13182d8641220538121440164d0 --output /new/path/uavids_original_audit.json`.
3. Verify 122,171 rows, exact 23-column header, no missing cells and label counts; investigate discrepancies rather than silently altering the source.
4. Lock auxiliary task and strip `FlowID`, raw addresses and any identity proxies from predictive feature sets; document why flow-aggregated fields are **not** used in early decisions.
5. Save raw file checksum, download time, source URL, environment and audit JSON; do not commit raw CSV.

### Large FAN-GHETS24 v2 — metadata and sample audit before expensive acquisition

1. Re-inventory [Zenodo 13692267 v2](https://zenodo.org/records/13692267) and compare its 72 names/sizes/checksums with the archived manifest; the source ZIP includes `starter/inspect_zenodo.py` for generating a fresh record inventory when internet access permits.
2. Check available CPU-machine disk space before downloading/repairing the 18.65 GB split archive. Verify MD5 per part, preserve all parts, and repair/extract in a **new** directory using the publisher's documented process.
3. Inspect a **genuine** paired `example_host_data_srID.parquet` and `.json`, using `python scripts/verify_public_data.py fan-pair ...`. Record schema, actual timestamp or interval semantics, sequence identity, label taxonomy, and which fields are available **at prediction time**.
4. Determine whether multiple evaluation-subject sequences share an underlying physical simulation/mission. Group these together when possible. If mapping is impossible, call the experiment **sequence-held-out only** and explicitly restrict mission-transfer claims.
5. Keep `attack_points` and other future/privileged metadata out of feature extraction. Identify any unavailable observation-quality gates explicitly; use only a reduced matched-input public benchmark if needed.

### New ns-3 — primary study

The next implementation milestone must demonstrate **true upstream handoff / witnessed forwarding / benign observer-deafness separation** on a three-hop test, with evaluator-only labels and realistic short message deadlines. Go/no-go before dataset generation and GPU training.

## 6. Audit limitations and next decision

**Status: DATASET SELECTION CONFIRMED; DATA INGESTION NOT YET VERIFIED.** FAN-GHETS24 v2 is the correct public temporal benchmark; UAVIDS-2025 is a separate auxiliary flow benchmark. Neither is a substitute for independent ns-3 monitoring and closed-loop response experiments. No per-sample result was fabricated, and no missing measurement is inferred from a dataset's DOI alone.

**NEXT:** acquire and checksum the small UAVIDS original, inspect a *real* FAN-GHETS24 Parquet/JSON pair and grouping provenance as access allows; then conduct ns-3 observation-semantics pilot before committing major compute.
