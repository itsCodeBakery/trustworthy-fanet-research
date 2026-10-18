# M0 scientific novelty audit — FANET selective forwarding

**Audit date:** 18 October 2026  
**Decision:** **CONDITIONAL GO for literature/data/observability pilots; NO GO for a novel-method or performance claim**  
**Scope:** an evidence-bounded audit, **not** a systematic review or completion of every full-method reproduction.

## 1. Evidence reviewed

**Provided by the researcher:** `UAV_FANET_Research_Overleaf_Package.zip` (47 entries; ZIP SHA-256 `6640605e9eb3bd3066b6bfc8e08a40bfa268c0f86e5c4d641b836545eb52891a`; ZIP CRC verification passed in this audit). Its 31-page research blueprint, closest-work reference register, gap traceability table, simulation contract and reporting limitations were inspected. Its `VERIFICATION.md` documents tests carried out when the package was prepared; those archived results were **not** independently rerun in this Step 5 session.

**Independently consulted primary full methods:**

- **Shila et al. 2010**, *IEEE TWC*, DOI [10.1109/TWC.2010.05.090700](https://doi.org/10.1109/TWC.2010.05.090700). Author-hosted [15-page full article](https://www.ece.iit.edu/~yucheng/YCheng_TWC10.pdf) was read for method, channel assumptions, probes and responses.
- **Ren et al. 2016**, *IEEE TWC*, DOI [10.1109/TWC.2016.2526601](https://doi.org/10.1109/TWC.2016.2526601). Waterloo-hosted [14-page full article](https://uwaterloo.ca/scholar/sites/ca.scholar/files/sshen/files/296.pdf) was read for CRS-A, local and shared reputation, routing response and OMNeT++ conditions.
- **Hutchins et al. 2025**, *Scientific Data*, DOI [10.1038/s41597-025-05560-1](https://doi.org/10.1038/s41597-025-05560-1). [Publisher HTML methods](https://www.nature.com/articles/s41597-025-05560-1) were read for ns-3 setup, sequence labels, early classification, three-stage model, confidence-dependent deferral, and the reported 80/10/10 dataset partition.
- **Zeng et al. 2026**, *INFOCOM*, DOI [10.1109/INFOCOM59046.2026.11571676](https://doi.org/10.1109/INFOCOM59046.2026.11571676). [Author-posted full-text transcription](https://www.researchgate.net/publication/408225701_FedGraph-ID_A_Federated_Graph_Learning_Framework_for_Intrusion_Detection_in_UAV_Networks_Under_Adversarial_Settings) was inspected for sliding-window flow graphs, federated GCN and HYDRA aggregation. This is **not** an independent reproduction of that implementation.

**Publisher sections/abstracts:** [Ceviz et al. 2025 FL-IDS](https://www.sciencedirect.com/science/article/pii/S2542660525001052); [Ceviz et al. FSFL-IDS 2026 institutional abstract](https://research.hacettepe.edu.tr/en/publications/distributed-intrusion-detection-indynamic-networks-ofuavs-using-f/); [Hussain and Maseleno 2026 TAR-GHD publisher abstract](https://www.americaspg.com/journal/20/article/4329). TAR-GHD's full downloadable PDF could not be retrieved by the available browsing routes and its detailed splitting, threshold and sensing contracts remain **unverified**. Additional sequential/calibration literature is linked in [closest_work_matrix.csv](../evidence/closest_work_matrix.csv).

**Interpretation rule:** bibliographic metadata, abstract-level descriptions and source author's accuracy claims are **not** equivalent to direct reproduction or proof of an absent method. No quantitative results from these papers will be mixed with our future ns-3 metrics as a common leaderboard without a common-task implementation.

## 2. Specific already-established methods

### 2.1. Normal wireless loss versus malicious drops — already solved *in principle*

Shila et al.'s **CAD** jointly estimates natural channel losses and monitors upstream/downstream forwarding, using probe/ACK exchanges and adaptive decision thresholds. It studies benign collisions and fading rather than assuming a perfect channel. Its original network is a largely static wireless mesh with assumptions and message access different from a monitor using only its own overheard UAV signals. **Our work cannot claim to invent channel-aware filtering**.

Ren et al.'s **CRS-A** goes further: it uses observed-vs-expected losses, **adaptive link thresholds**, first- and second-hand reputation, a sink for malicious-node identification, and a distributed **attack-tolerant forwarding scheme**. Its evaluated OMNeT++ scenario has 100 **stationary** WSN nodes and a Markov channel. **We cannot claim to invent either adaptive loss thresholds or detector-informed forwarding**. A full CRS-A implementation needs extra network reports and a sink; it is not equal-information to our local-only detector.

### 2.2. Early FANET detection *and deferral* — already implemented

Hutchins et al. construct the **FAN-GHETS24** ns-3 temporal dataset and evaluate an early time-series classifier with an autoencoder and CNNs trained for increasing sequence prefixes. Its published technical validation uses a **confidence threshold that defers classification until additional evidence arrives**. Deferral itself is not a new idea. Our plausible distinction must be **deferral based on the monitor's ability to witness forwarding** (observation quality/eligibility), rather than classification confidence alone. The full source describes 80/10/10 train/validation/test *sequence* sets; mission-level separation cannot be inferred from this description. Do not accuse the source of leakage without inspecting its raw simulation grouping.

### 2.3. Link quality, temporal trust and UAV intrusion models — current direct overlap

The 2026 **TAR-GHD** publisher abstract combines link-quality evidence, route stability, packet consistency and temporal trust to detect grey-hole behaviour using FAN-GHETS24-derived data. This strongly undercuts a generic novelty story about “trust and temporal link evidence”; its full decision timing, false-accusation unit and split remain unresolved. It is a **required overlap check**, not a verified numeric baseline yet.

**FL-IDS (2025)**, **FSFL-IDS (2026)** and **FedGraph-ID (INFOCOM 2026)** establish distributed/federated and graph-based UAV IDS under dynamic/adversarial networking. Their information exchange and labels differ from our local next-hop witness task. They cannot fairly be ranked numerically from their published metrics against a new packet-level local experiment.

### 2.4. Calibrated sequential alarms and abstention — generally established

Sequential anomaly detection and conformal thresholding predate this project; for example [Laxhammar & Falkman (TPAMI, 2014)](https://pubmed.ncbi.nlm.nih.gov/26353278/) discusses well-grounded threshold calibration for online trajectories. The mission-maximum rank threshold is a known **split-rank construction**, not a novel theorem, and only has the expected finite-horizon all-benign false-accusation statement for frozen and exchangeable whole missions. We will not advertise generic “distribution-free” validity under channel shift, arbitrary mission duration, or attacked-network honesty.

## 3. Our *bounded* candidate research gap

**Question not resolved by the sources inspected here:** In *mobile* FANETs, at decision time, does explicit separation of **what an upstream UAV actually witnessed** from **what the relay actually forwarded**, combined with evidence-eligible sequential decisions and *complete-mission* benign calibration, offer useful early detection and lower wrong-relay accusation **on fresh independent mission families**? If alarms change AODV next hops, does the full *causal closed-loop* simulation improve timely legitimate packet delivery after measuring false isolation, outage, and route-repair costs?

This is a **joint empirical-evaluation gap in the bounded inspected corpus**, not proof of the absence of an equivalent 2026 method elsewhere. It is distinctive only if all of these are enforced:

1. Receiver-local packet handoff and **overheard forwarding witness** are logged separately from **privileged simulator-only ground truth**; “not overheard” never becomes an automatic malicious-drop label.
2. Poor-monitoring **gate-based abstention** is measured against confidence-only deferral and a no-gate model, with attacker exposure lost to deferral explicitly reported.
3. Thresholds of **every comparable method** are calibrated over *whole benign missions* of a specified horizon, while actual observed held-out false accusations and delay are reported.
4. Training, development, benign calibration, and evaluation use **disjoint mission families**, preserving all run variants and common exogenous mobility/traffic within each family.
5. Network mitigation is measured in **fresh, causal, closed-loop ns-3 runs**; prior evaluation on frozen traces is not relabelled “network recovery.”
6. A strong **equal-information channel-aware statistical** predictor/CUSUM must be competitive; a TCN wins novelty credit **only for a demonstrated incremental operational effect**, not its architecture.

## 4. Testable null hypotheses and minimum evidence

- **H01 (primary):** At fixed **nominal** mission false-accusation calibration alpha=0.05, the evidence-gated procedure has **no higher** probability of correctly flagging an *exposed* attacker within 30 s than the strongest equal-input, mission-calibrated channel-aware statistical comparator. Compare paired independent mission families. Report **both methods' actual held-out mission false-accusation rates** and intervals; matching nominal alpha does **not** mean empirical test FPR is exactly matched.
- **H02:** Observation-quality gating adds **no incremental operational utility** over the same learned/statistical score with no gate and over confidence-only defer, after accounting for useful observation coverage, malicious exposure deferred and wrong-relay flags. Run a factorial gate × model × calibration comparison on independent families.
- **H03:** A causal temporary local next-hop avoidance response does **not** improve timely application delivery over ordinary AODV/no response, when paired against identical exogenous mission inputs and accounting for route repair, false avoidance and outage. Requires **new closed-loop simulations** for each policy, not off-policy replay.

A positive accuracy or F1 result on an offline public sequence split **cannot** alone reject these null hypotheses.

## 5. Threats to construct validity

- **Observability:** MAC handoff success is not guaranteed to imply the relay was able to retransmit; monitor deafness and normal queue drops must be separated. Validate packet identities, timestamp maturity and observation deadlines in a three-hop simulator pilot.
- **Information leakage:** never feed simulator malicious-drop reasons, attacker IDs, “packet would have been observed”, future frames or nonlocal node internals into the detector. Keep feature and evaluator loaders physically separate and test isolation.
- **Attack exposure:** compromised nodes with no forwarded eligible data are not false negatives for the exposed-attack endpoint. Show exposed fraction and inactive compromised nodes separately.
- **Calibration population:** split-rank control is **marginal** for exchangeable all-benign mission draws, not one per arbitrary mission configuration or shift. A balanced cell grid requires declared mixture/weighting for comparisons. Report conditional per-cell failures.
- **Identifiability:** if benign and malicious mechanisms produce the same distribution of local observations, accurate local classification may be impossible; report empirical overlaps and abstention instead of inventing unavailable evidence.
- **Baseline parity:** CAD2010 uses signed probes/ACK; CRS-A uses propagated reputations and a sink; a localised adaptation is **not** an exact reproduction. Measure/control extra bytes, latency and monitoring affordances in any original-protocol reproduction.
- **Sample size:** 199 calibration missions and five training seeds do not mean 995 independent calibration missions; resample at independent mission-family level.
- **Portability:** ns-3 synthetic log-distance/Nakagami channels and simple UAV waypoints are controlled experiments, **not** field validated flying radios, authenticated airborne systems or aircraft flight dynamics. SUMO models ground convoy traffic only.

## 6. Go/no-go verdict and remaining dependencies

**Go for the next small evidence-building stage:** audit dataset fields/rights/mission provenance and implement a *three-hop benign and observer-deafness pilot* once simulator build and callback contracts are verified. Pilot baseline shall be the **channel-aware statistical monitor**; no mandatory GPU model yet.

**Do not freeze a paper novelty claim or run the 2,743-run matrix** until:

- TAR-GHD 2026 exact full method/split/decision timing is checked (PDF/current author version or reproducible code; if inaccessible, keep an explicit limitation).
- The FAN-GHETS24 public task's simulation-family grouping and source-code access status are audited.
- The CAD / CRS-A input/output/sampling equivalence contract is frozen, with transparent **adaptation vs fidelity** tracks.
- Static handoff–witness matching, benign losses and monitor-deafness controls succeed. Otherwise the proposed detector's main measurements do not exist.

**Decision contingency:** if no observation-quality advantage survives equal-input and confidence-defer controls, abandon the TCN-specific claim and retain the simpler statistical detector or pivot to a reproducible *observability and mission-transfer benchmark*. If route avoidance harms delivery, report a detection-only paper rather than inventing mitigation success.

**Next step:** data/source feasibility audit and minimal simulator observability acceptance tests. Keep all current proposed results labelled as pending.
