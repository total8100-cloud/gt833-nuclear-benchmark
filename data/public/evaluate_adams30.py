"""
ADAMS-30 Evaluation Script
===========================
Evaluates any constraint extraction system against the ADAMS-30 public benchmark.

Usage:
    python evaluate_adams30.py predictions.json

Input format (predictions.json):
    A list of objects, one per requirement:
    [
        {
            "id": "GT-002",
            "predicted_constraints": [
                {
                    "constraint_type": "temporal",
                    "variable": "recovery_time",
                    "operator": "<=",
                    "value": 24,
                    "unit": "hours"
                }
            ]
        },
        ...
    ]

Output:
    Precision, Recall, F1 on the ADAMS-30 benchmark.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


ADAMS30_PATH = Path(__file__).parent / "adams30.json"
NUM_TOL = 0.10   # 10% tolerance for numeric/temporal value matching


def load_ground_truth() -> Dict[str, List[dict]]:
    with open(ADAMS30_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return {r["id"]: r["constraints"] for r in data["requirements"]}


def constraint_matches(gt: dict, pred: dict, tol: float = NUM_TOL) -> bool:
    """Return True if pred matches gt constraint."""
    if gt.get("constraint_type") != pred.get("constraint_type"):
        return False
    ct = gt["constraint_type"]
    if ct == "boolean":
        # Variable name match (case-insensitive, ignore underscores/spaces)
        def norm(s: str) -> str:
            return s.lower().replace("_", " ").replace("-", " ").strip()
        return norm(gt.get("variable", "")) == norm(pred.get("variable", ""))
    else:
        # Numeric / Temporal: operator + value within tolerance + unit family
        if gt.get("operator") != pred.get("operator"):
            return False
        gt_val = float(gt.get("value", 0))
        pred_val = float(pred.get("value", 0))
        if gt_val == 0:
            return pred_val == 0
        if abs(gt_val - pred_val) / abs(gt_val) > tol:
            return False
        return True


def evaluate(gt_map: Dict[str, List[dict]],
             preds_map: Dict[str, List[dict]]) -> Tuple[float, float, float]:
    tp = fp = fn = 0
    for req_id, gt_constraints in gt_map.items():
        preds = preds_map.get(req_id, [])
        matched_pred = set()
        for gt_c in gt_constraints:
            found = False
            for j, pred_c in enumerate(preds):
                if j in matched_pred:
                    continue
                if constraint_matches(gt_c, pred_c):
                    tp += 1
                    matched_pred.add(j)
                    found = True
                    break
            if not found:
                fn += 1
        fp += len(preds) - len(matched_pred)

    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec  = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1   = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    return prec, rec, f1


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nNo predictions file provided. Running self-test with perfect predictions.")
        # Self-test: perfect predictions
        gt_map = load_ground_truth()
        preds_map = gt_map.copy()
    else:
        pred_path = Path(sys.argv[1])
        if not pred_path.exists():
            print(f"ERROR: File not found: {pred_path}")
            sys.exit(1)
        with open(pred_path, encoding="utf-8") as f:
            preds_raw = json.load(f)
        gt_map = load_ground_truth()
        preds_map = {r["id"]: r.get("predicted_constraints", []) for r in preds_raw}

    prec, rec, f1 = evaluate(gt_map, preds_map)
    print(f"\nADAMS-30 Evaluation Results")
    print(f"{'=' * 35}")
    print(f"  Precision : {prec:.4f}  ({prec*100:.1f}%)")
    print(f"  Recall    : {rec:.4f}  ({rec*100:.1f}%)")
    print(f"  F1        : {f1:.4f}  ({f1*100:.1f}%)")
    print(f"{'=' * 35}")
    print(f"  Requirements evaluated: {len(gt_map)}")


if __name__ == "__main__":
    main()
