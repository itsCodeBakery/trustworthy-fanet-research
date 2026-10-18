# Data sources and provenance — UAV/FANET study

**No raw datasets are committed here.**

| Source | Use | Acquisition boundary |
| --- | --- | --- |
| [FAN-GHETS24 v2](https://zenodo.org/records/13692267) | Public temporal grey-hole benchmark | Research blueprint inventories a 72-part ~18.65 GB archive; full sample-level audit and mission independence remain unverified. |
| New ns-3 FANET experiment traces | Main monitoring/mission calibration and route-response evidence | **Not yet generated.** Separate local observable events, privileged evaluator ground truth and mission manifests. |
| [UAVIDS-2025](https://zenodo.org/records/15336998) | Auxiliary offline flow classification | Blueprint reports 122,171 rows and 22 non-label features; no packet timestamps or mission identity in the inspected CSV. Not a causal early-monitoring benchmark. |

For every source record version, license, exact file hashes, timestamp semantics, feature availability, attack taxonomy, independence unit, acquisition date, split IDs, and any access limitations. Keep full raw files and large checkpoints off Git with versioned download locations and integrity checks.

Train/dev/calibration/test grouping occurs at mission-family level **before window construction**. No model feature may be derived from attack ground truth, future observation events, privileged simulator drop reasons, or synthetic missing public features.
