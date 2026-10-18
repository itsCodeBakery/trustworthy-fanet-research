# UAV/FANET public datasets — selection and acceptance

**Step 6 status:** dataset roles confirmed; **raw-data ingestion and per-sample integrity pending**.

Read the [source-based feasibility audit](../docs/dataset_feasibility.md), [machine-readable source records](source_records.json), [feature readiness matrix](../evidence/dataset_feature_feasibility.csv) and [offline audit utility](../scripts/verify_public_data.py) before writing model code.

| Dataset | Appropriate role | Evidence boundary |
| --- | --- | --- |
| [FAN-GHETS24 **v2**](https://zenodo.org/records/13692267) | Main **public early temporal grey-hole benchmark** | Source paper gives 31,910 sequences; 25 features per timestep; 12 classes. The versioned v2 Zenodo inventory lists 72 files / 18,648,943,241 bytes. **No archive samples downloaded here; mission family IDs and complete monitor gate features not verified.** |
| [UAVIDS-2025 v1](https://zenodo.org/records/15336998) | Auxiliary **offline flow intrusion classification** | Single 20,054,667-byte CSV. Earlier uploaded package audit reports 122,171 rows, 22 non-label columns, no missing data; original bytes not independently re-hashed in Step 6. |
| **New ns-3 FANET traces** | Required **primary local-monitoring, mission-level calibration and causal network-recovery evidence** | Not generated yet. Must have distinct local observable events, evaluator-only attacker/drop logs, mission/run provenance and closed-loop policy variants. |

The 2025 FAN-GHETS24 paper explicitly describes **promiscuous witness logging from local benign evaluation nodes**, so local monitoring by itself is **not novel**. Its processed Parquet/JSON files must be inspected before assuming the proposed handoff success, observation gate and independent mission calibration can be reproduced.

The **published FAN-GHETS24 descriptor links to v1 (13315419)**, whereas this project pins **v2 (13692267)**. Do not mix their file sizes, hashes or feature assumptions.

Both archived Zenodo inventory JSON records list **CC BY 4.0**. Respect the exact original license and citation. Raw archives, passwords, model checkpoints and huge packet traces must not be committed to Git. Save SHA-256, original MD5, source version, download date and audit output with external data.

Use `scripts/verify_public_data.py inventory ...` for inventory consistency and optional actual downloaded-file checks. Use `csv` mode on the original UAVIDS file. The script's **three smoke tests passed with synthetic fixtures only**, not public research data.

Never infer mission independent samples, causal prediction timestamps, or attack-drop truth from absent fields. See the audit for acceptance gates and exact commands.
