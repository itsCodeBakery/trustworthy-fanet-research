# UAV/FANET public datasets — selection and acceptance

**Step 7 status (18 October 2026):** the researcher ran Google Colab integrity/shape checks for the original UAVIDS-2025 CSV and supplied matching output; see [the reported Colab verification record](../evidence/uavids_2025_colab_integrity_2026-10-18.json). The remote notebook was not independently run by the assistant. **FAN-GHETS24 v2 raw samples and underlying mission grouping remain unverified.**

Read the [five-fold Colab validation](../docs/uavids_group_split_decision.md), [frozen auxiliary benchmark](../docs/uavids_group_split_decision.md), [Colab leakage screening](../docs/uavids_split_audit.md), [recorded diagnostic outputs](../evidence/uavids_2025_leakage_screen_2026-10-18.json), [source-based feasibility audit](../docs/dataset_feasibility.md), [machine-readable source records](source_records.json), [feature readiness matrix](../evidence/dataset_feature_feasibility.csv) and [offline audit utility](../scripts/verify_public_data.py) before writing model code.

| Dataset | Appropriate role | Evidence boundary |
| --- | --- | --- |
| [FAN-GHETS24 **v2**](https://zenodo.org/records/13692267) | Main **public early temporal grey-hole benchmark** | Source paper gives 31,910 sequences; 25 features per timestep; 12 classes. The versioned v2 Zenodo inventory lists 72 files / 18,648,943,241 bytes. **No archive samples downloaded here; mission family IDs and complete monitor gate features not verified.** |
| [UAVIDS-2025 v1](https://zenodo.org/records/15336998) | Auxiliary **offline flow intrusion classification** | Single 20,054,667-byte CSV. Original user-operated Colab run reports verified original-file MD5 and SHA-256; 122,171 rows, 22 non-label columns, no missing cells, no duplicate complete rows. **Identity/grouping leakage still needs auditing.** |
| **New ns-3 FANET traces** | Required **primary local-monitoring, mission-level calibration and causal network-recovery evidence** | Not generated yet. Must have distinct local observable events, evaluator-only attacker/drop logs, mission/run provenance and closed-loop policy variants. |

The 2025 FAN-GHETS24 paper explicitly describes **promiscuous witness logging from local benign evaluation nodes**, so local monitoring by itself is **not novel**. Its processed Parquet/JSON files must be inspected before assuming the proposed handoff success, observation gate and independent mission calibration can be reproduced.

The **published FAN-GHETS24 descriptor links to v1 (13315419)**, whereas this project pins **v2 (13692267)**. Do not mix their file sizes, hashes or feature assumptions.

Both archived Zenodo inventory JSON records list **CC BY 4.0**. Respect the exact original license and citation. Raw archives, passwords, model checkpoints and huge packet traces must not be committed to Git. Save SHA-256, original MD5, source version, download date and audit output with external data.

Use `scripts/verify_public_data.py inventory ...` for inventory consistency and optional actual downloaded-file checks. Use `csv` mode on the original UAVIDS file. The script's **three smoke tests passed with synthetic fixtures only**, not public research data.

Never infer mission independent samples, causal prediction timestamps, or attack-drop truth from absent fields. See the audit for acceptance gates and exact commands.
