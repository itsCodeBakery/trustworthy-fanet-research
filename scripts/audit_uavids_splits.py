#!/usr/bin/env python3
"""Colab-friendly original-file UAVIDS group-split and duplicate-label audit.

Diagnostics only. Does not train any model or claim independent simulations.
"""
import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

ID_COLUMNS = ["FlowID", "SrcAddr", "DstAddr", "SrcPort", "DstPort"]
LABEL = "label"


def audit(path):
    df = pd.read_csv(path)
    required = set(ID_COLUMNS + [LABEL, "Protocol"])
    if not required.issubset(df.columns):
        raise ValueError(f"Missing required columns: {sorted(required-set(df.columns))}")
    # Protocol is constant in the verified source; keep it out of the numeric model matrix.
    feature_cols = [c for c in df.columns if c not in required]
    classes = sorted(df[LABEL].dropna().unique().tolist())
    print("Rows:", len(df), "| classes:", classes)
    print("Predictor columns after removing identifiers and Protocol:", len(feature_cols))
    print("Protocol counts:", df["Protocol"].value_counts(dropna=False).to_dict())

    # Exact dataframe equality, not a synthetic or approximate near-duplicate metric.
    repeated = int(df.duplicated(subset=feature_cols).sum())
    repeated_rows = int(df.duplicated(subset=feature_cols, keep=False).sum())
    conflict = df.groupby(feature_cols, dropna=False, sort=False)[LABEL].transform("nunique") > 1
    conflict_rows = int(conflict.sum())
    conflict_groups = int(df.loc[conflict, feature_cols].drop_duplicates().shape[0])
    print("Repeated feature-row occurrences beyond first:", repeated)
    print("Rows belonging to repeated feature groups:", repeated_rows)
    print("Rows in exact-feature groups with >1 distinct label:", conflict_rows)
    print("Number of exact-feature groups with contradictory labels:", conflict_groups)

    # Stable 64-bit row fingerprints for fast cross-fold overlap screening.
    # Hash collisions are theoretically possible: this is a diagnostic, not cryptographic proof.
    fingerprints = pd.util.hash_pandas_object(df[feature_cols], index=False).to_numpy()
    y = df[LABEL]
    groups = df["SrcAddr"].astype(str)
    kfold = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
    folds = []
    for fold_id, (train_idx, test_idx) in enumerate(
        kfold.split(df[feature_cols], y, groups), start=1
    ):
        train_sources = set(groups.iloc[train_idx])
        test_sources = set(groups.iloc[test_idx])
        source_overlap = len(train_sources.intersection(test_sources))
        train_counts = y.iloc[train_idx].value_counts().reindex(classes, fill_value=0)
        test_counts = y.iloc[test_idx].value_counts().reindex(classes, fill_value=0)
        shared_hashes = set(fingerprints[train_idx]).intersection(fingerprints[test_idx])
        test_overlap_rows = int(pd.Series(fingerprints[test_idx]).isin(shared_hashes).sum())
        result = {
            "fold": fold_id,
            "train_rows": len(train_idx),
            "test_rows": len(test_idx),
            "train_source_groups": len(train_sources),
            "test_source_groups": len(test_sources),
            "source_overlap_groups": source_overlap,
            "test_class_counts": {str(c): int(test_counts[c]) for c in classes},
            "train_class_counts": {str(c): int(train_counts[c]) for c in classes},
            "shared_exact_feature_fingerprint_count": len(shared_hashes),
            "test_rows_with_train_feature_fingerprint": test_overlap_rows,
            "has_all_classes_in_both_sides": bool(
                (train_counts.gt(0).all()) and (test_counts.gt(0).all())
            )
        }
        assert source_overlap == 0
        folds.append(result)
        print(
            f"Fold {fold_id}: train={len(train_idx):,} test={len(test_idx):,} "
            f"source_overlap={source_overlap}, shared_features={len(shared_hashes):,}, "
            f"test_rows_matching_train={test_overlap_rows:,}, all_classes={result['has_all_classes_in_both_sides']}"
        )
        print("  Test labels:", result["test_class_counts"])

    return {
        "source_file": Path(path).name,
        "status": "SPLIT_FEASIBILITY_DIAGNOSTIC_ONLY",
        "feature_columns_after_drops": feature_cols,
        "row_count": len(df),
        "repeat_occurrences_after_identifier_drop": repeated,
        "rows_in_duplicate_feature_groups": repeated_rows,
        "rows_in_cross_label_exact_feature_groups": conflict_rows,
        "cross_label_exact_feature_groups": conflict_groups,
        "split_group":"SrcAddr",
        "split_strategy":"StratifiedGroupKFold(5, shuffle=True, random_state=42)",
        "caveat":"SrcAddr is not an independently verified simulation/mission family; fingerprint overlap is a 64-bit screening estimate",
        "folds": folds
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", nargs="?", default="/content/UAVIDS-2025.csv")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    report = audit(args.csv_path)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        # Do not silently overwrite a previous audit.
        with args.output.open("x", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
            f.write("\n")
        print("Saved diagnostic:", args.output)


if __name__ == "__main__":
    main()
