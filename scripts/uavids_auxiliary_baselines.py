#!/usr/bin/env python3
"""CPU-only, source-group-disjoint UAVIDS-2025 offline classification baselines.

Produces descriptive offline *full-flow* results; never call this a FANET
packet-level, mission-independent, or early-detection benchmark.
"""
import argparse
import hashlib
import json
import platform
import time
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix, f1_score, recall_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

DROP = {"FlowID", "SrcAddr", "DstAddr", "SrcPort", "DstPort", "Protocol", "label"}
EXPECTED_SHA256 = "d50d339f68be7b23f0bf089dd438b20a1835c13182d8641220538121440164d0"


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def measures(y, pred, classes):
    return {
        "accuracy": float(accuracy_score(y, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y, pred)),
        "macro_f1": float(f1_score(y, pred, labels=classes, average="macro", zero_division=0)),
        "recall_by_class": {cl: float(v) for cl, v in zip(
            classes, recall_score(y, pred, labels=classes, average=None, zero_division=0))},
        "confusion_matrix_true_rows_pred_columns": confusion_matrix(y, pred, labels=classes).tolist(),
        "n": len(y),
    }


def run(csv_path, out_dir):
    if out_dir.exists():
        raise FileExistsError(f"Output directory already exists: {out_dir}; select a new run directory")
    actual_hash = sha256(csv_path)
    if actual_hash != EXPECTED_SHA256:
        raise ValueError(f"Original UAVIDS CSV SHA-256 mismatch: {actual_hash}")
    frame = pd.read_csv(csv_path)
    if len(frame) != 122171:
        raise ValueError(f"Unexpected row count: {len(frame)}")
    if frame.isna().to_numpy().any():
        raise ValueError("Unexpected missing cells")
    if frame["Protocol"].nunique(dropna=False) != 1:
        raise ValueError("Protocol not constant; review feature contract")
    columns = [c for c in frame.columns if c not in DROP]
    if len(columns) != 16 or not all(pd.api.types.is_numeric_dtype(frame[c]) for c in columns):
        raise ValueError(f"Unexpected feature schema: {columns}")
    x = frame[columns].to_numpy(dtype=np.float32)
    if not np.isfinite(x).all():
        raise ValueError("Nonfinite numeric predictor: inspect before training")
    y = frame["label"].astype(str).to_numpy()
    groups = frame["SrcAddr"].astype(str).to_numpy()
    classes = sorted(set(y))
    hashes = pd.util.hash_pandas_object(frame[columns], index=False).to_numpy()
    oof = []
    records = []
    folds = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
    model_builders = {
        "prior_dummy": lambda: DummyClassifier(strategy="prior"),
        "balanced_logistic": lambda: make_pipeline(
            StandardScaler(), LogisticRegression(max_iter=700, class_weight="balanced", random_state=42)),
        "hist_gradient_boosting": lambda: HistGradientBoostingClassifier(
            max_iter=70, max_leaf_nodes=15, learning_rate=0.1, random_state=42)
    }
    for i, (train, test) in enumerate(folds.split(x, y, groups), start=1):
        if set(groups[train]).intersection(groups[test]):
            raise AssertionError("Source address overlap across folds")
        n_classes = set(y[train]), set(y[test])
        if any(set(classes) != s for s in n_classes):
            raise ValueError(f"Fold {i} has incomplete class support")
        seen = set(hashes[train])
        no_overlap = ~np.isin(hashes[test], list(seen))
        print(f"Fold {i}: train={len(train)} test={len(test)} "
              f"exact-hash-overlap-test-rows={(~no_overlap).sum()}", flush=True)
        for name, constructor in model_builders.items():
            model = constructor()
            t0 = time.perf_counter()
            model.fit(x[train], y[train])
            pred = model.predict(x[test])
            seconds = time.perf_counter() - t0
            scores = measures(y[test], pred, classes)
            clean_scores = measures(y[test][no_overlap], pred[no_overlap], classes)
            record = {"fold": i, "model": name, "fit_and_predict_wall_seconds": seconds,
                      "source_overlap_groups": 0, "exact_hash_overlap_test_rows": int((~no_overlap).sum()),
                      "metrics": scores, "excluding_exact_hash_overlap_metrics": clean_scores,
                      "test_class_counts": {c: int(sum(y[test] == c)) for c in classes}}
            records.append(record)
            oof.append(pd.DataFrame({"row_index": test, "fold": i, "model": name,
                                     "true_label": y[test], "predicted_label": pred,
                                     "feature_hash_seen_in_training": ~no_overlap}))
            print(f"  {name}: macro-F1={scores['macro_f1']:.4f} "
                  f"balanced_acc={scores['balanced_accuracy']:.4f} "
                  f"seconds={seconds:.1f}", flush=True)
    oof_df = pd.concat(oof, ignore_index=True)
    for name in model_builders:
        m = oof_df[oof_df["model"] == name]
        assert m["row_index"].is_unique and len(m) == len(frame)
    report = {"status": "OFFLINE_COMPLETED_FLOW_AUXILIARY_ONLY",
              "data_sha256": actual_hash, "row_count": len(frame),
              "features": columns, "dropped": sorted(DROP),
              "folds": "StratifiedGroupKFold(5, shuffle=True, random_state=42) by SrcAddr",
              "split_limitations": "Source-disjoint does not prove independent simulation/mission grouping; some feature hash matches cross folds.",
              "versions": {"python": platform.python_version(), "pandas": pd.__version__,
                           "numpy": np.__version__, "scikit_learn": sklearn.__version__},
              "classes": classes, "fold_results": records}
    out_dir.mkdir(parents=True, exist_ok=False)
    with (out_dir / "offline_fivefold_metrics.json").open("x", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    oof_df.to_csv(out_dir / "offline_out_of_fold_predictions.csv", index=False)
    print("Saved:", out_dir, flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data", type=Path, default=Path("/content/UAVIDS-2025.csv"))
    p.add_argument("--output", type=Path, default=Path("/content/uavids_offline_baselines_run1"))
    a = p.parse_args()
    run(a.data, a.output)
