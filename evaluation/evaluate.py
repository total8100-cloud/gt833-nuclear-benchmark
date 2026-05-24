"""
GT-833 Benchmark Evaluation Script
Computes precision, recall, F1 for constraint extraction predictions.

Usage:
    python evaluate.py --data ../data/public/gt833_nrc_public_v3.json
    python evaluate.py --data ../data/public/gt833_nrc_public_v3.json \
                       --predictions predictions.json
"""
import argparse
import json


def load_ground_truth(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return {req["id"]: req["constraints"] for req in data["requirements"]}


def load_predictions(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def constraint_match(pred: dict, gold: dict, strict: bool = False) -> bool:
    if pred.get("constraint_type") != gold.get("constraint_type"):
        return False
    if pred.get("variable", "").lower() != gold.get("variable", "").lower():
        return False
    if strict:
        return (pred.get("operator") == gold.get("operator") and
                pred.get("value") == gold.get("value"))
    return True


def evaluate(gt: dict, preds: dict, strict: bool = False) -> dict:
    tp = fp = fn = 0
    for req_id, gold_constraints in gt.items():
        pred_constraints = preds.get(req_id, [])
        matched_gold = set()
        for pred in pred_constraints:
            matched = any(
                i not in matched_gold and constraint_match(pred, g, strict)
                for i, g in enumerate(gold_constraints)
            )
            if matched:
                tp += 1
                # mark first unmatched gold as matched
                for i, g in enumerate(gold_constraints):
                    if i not in matched_gold and constraint_match(pred, g, strict):
                        matched_gold.add(i)
                        break
            else:
                fp += 1
        fn += len(gold_constraints) - len(matched_gold)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)
          if (precision + recall) > 0 else 0.0)
    return {"precision": round(precision, 4), "recall": round(recall, 4),
            "f1": round(f1, 4), "tp": tp, "fp": fp, "fn": fn}


def main():
    parser = argparse.ArgumentParser(description="GT-833 benchmark evaluation")
    parser.add_argument("--data", required=True, help="GT-833 JSON path")
    parser.add_argument("--predictions", default=None,
                        help="Predictions JSON (req_id -> list of constraint dicts)")
    parser.add_argument("--strict", action="store_true",
                        help="Strict match: operator+value must also match")
    args = parser.parse_args()

    gt = load_ground_truth(args.data)
    print(f"Loaded {len(gt)} requirements from {args.data}")

    if args.predictions is None:
        total = sum(len(v) for v in gt.values())
        types: dict = {}
        for cs in gt.values():
            for c in cs:
                t = c.get("constraint_type", "unknown")
                types[t] = types.get(t, 0) + 1
        print(f"\nDataset statistics — {total} total constraints")
        for t, cnt in sorted(types.items(), key=lambda x: -x[1]):
            print(f"  {t:12s}: {cnt:4d}  ({100*cnt/total:5.1f}%)")
        return

    preds = load_predictions(args.predictions)
    results = evaluate(gt, preds, args.strict)
    mode = "strict" if args.strict else "relaxed"
    print(f"\n=== Results ({mode} matching) ===")
    print(f"Precision : {results['precision']:.4f}")
    print(f"Recall    : {results['recall']:.4f}")
    print(f"F1        : {results['f1']:.4f}")
    print(f"TP={results['tp']}  FP={results['fp']}  FN={results['fn']}")


if __name__ == "__main__":
    main()
