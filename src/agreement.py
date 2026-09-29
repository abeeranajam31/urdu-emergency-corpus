"""Inter-annotator agreement for the manually annotated fields.

Two steps:

1. ``export`` writes a blind annotation sheet (CSV) for a second
   annotator: utterance text and English gloss only, in shuffled order,
   with empty columns for the five manual fields. The first annotator's
   labels are never included, so the second pass is independent.

2. ``score`` reads the completed sheet back, aligns it with
   data/corpus_manual.jsonl by ``id``, and reports, per field, raw
   percent agreement and Cohen's kappa. Urgency is ordinal, so it also
   gets a quadratic-weighted kappa, which penalises a high/critical
   disagreement less than a low/critical one.

Kappa is implemented here directly (no scikit-learn dependency) so the
calculation stays auditable alongside the rest of the pipeline.

Usage:
    python -m src.agreement export --out data/annotator2_sheet.csv
    python -m src.agreement score --sheet data/annotator2_sheet.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from collections import Counter
from pathlib import Path

from src.preprocessing import MANUAL_CORPUS_PATH, load_manual_corpus

RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"
AGREEMENT_PATH = RESULTS_DIR / "agreement.json"

MANUAL_FIELDS = ["emergency_type", "urgency", "speech_act", "person_reference", "repetition"]
URGENCY_ORDER = ["low", "medium", "high", "critical"]


def cohen_kappa(a: list, b: list) -> float:
    """Unweighted Cohen's kappa for two equal-length label sequences."""
    if len(a) != len(b) or not a:
        raise ValueError("label sequences must be non-empty and of equal length")
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    expected = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    if expected == 1:
        return 1.0
    return (observed - expected) / (1 - expected)


def weighted_kappa(a: list, b: list, order: list) -> float:
    """Quadratic-weighted Cohen's kappa for ordinal labels in ``order``."""
    if len(a) != len(b) or not a:
        raise ValueError("label sequences must be non-empty and of equal length")
    k = len(order)
    idx = {label: i for i, label in enumerate(order)}
    n = len(a)
    obs = [[0.0] * k for _ in range(k)]
    for x, y in zip(a, b):
        obs[idx[x]][idx[y]] += 1
    row = [sum(obs[i]) for i in range(k)]
    col = [sum(obs[i][j] for i in range(k)) for j in range(k)]
    num = den = 0.0
    for i in range(k):
        for j in range(k):
            w = ((i - j) ** 2) / ((k - 1) ** 2)
            num += w * obs[i][j]
            den += w * row[i] * col[j] / n
    if den == 0:
        return 1.0
    return 1 - num / den


def _normalise(field: str, value) -> str:
    value = str(value).strip().lower()
    if field == "repetition":
        return "true" if value in {"true", "1", "yes", "y"} else "false"
    return value


def export_sheet(out_path: Path, manual_path: Path = MANUAL_CORPUS_PATH, seed: int = 13) -> int:
    records = load_manual_corpus(manual_path)
    random.Random(seed).shuffle(records)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "text", "english_gloss", *MANUAL_FIELDS])
        for r in records:
            writer.writerow([r["id"], r["text"], r["english_gloss"], *[""] * len(MANUAL_FIELDS)])
    return len(records)


def score_sheet(sheet_path: Path, manual_path: Path = MANUAL_CORPUS_PATH) -> dict:
    gold = {r["id"]: r for r in load_manual_corpus(manual_path)}
    with sheet_path.open(encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["id"] in gold]

    report: dict = {"n_items": len(rows), "fields": {}}
    for field in MANUAL_FIELDS:
        pairs = [
            (_normalise(field, gold[r["id"]][field]), _normalise(field, r[field]))
            for r in rows
            if str(r.get(field, "")).strip()
        ]
        if not pairs:
            continue
        a, b = [p[0] for p in pairs], [p[1] for p in pairs]
        entry = {
            "n": len(pairs),
            "percent_agreement": round(sum(x == y for x, y in pairs) / len(pairs), 3),
            "cohen_kappa": round(cohen_kappa(a, b), 3),
            "disagreements": [r["id"] for r in rows if str(r.get(field, "")).strip()
                              and _normalise(field, gold[r["id"]][field]) != _normalise(field, r[field])],
        }
        if field == "urgency" and set(a) | set(b) <= set(URGENCY_ORDER):
            entry["quadratic_weighted_kappa"] = round(weighted_kappa(a, b, URGENCY_ORDER), 3)
        report["fields"][field] = entry
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    exp = sub.add_parser("export", help="write a blind sheet for a second annotator")
    exp.add_argument("--out", type=Path, default=Path("data/annotator2_sheet.csv"))
    sc = sub.add_parser("score", help="compute agreement from a completed sheet")
    sc.add_argument("--sheet", type=Path, required=True)
    sc.add_argument("--out", type=Path, default=AGREEMENT_PATH)
    args = parser.parse_args()

    if args.command == "export":
        n = export_sheet(args.out)
        print(f"Wrote {n} items to {args.out}")
    else:
        report = score_sheet(args.sheet)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        for field, e in report["fields"].items():
            extra = f", weighted κ={e['quadratic_weighted_kappa']}" if "quadratic_weighted_kappa" in e else ""
            print(f"{field:17s} n={e['n']:3d}  agreement={e['percent_agreement']:.3f}  κ={e['cohen_kappa']}{extra}")
        print(f"Saved to {args.out}")


if __name__ == "__main__":
    main()
