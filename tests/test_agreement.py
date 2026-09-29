import csv

import pytest

from src.agreement import MANUAL_FIELDS, cohen_kappa, export_sheet, score_sheet, weighted_kappa
from src.preprocessing import load_manual_corpus


def test_kappa_perfect_agreement_is_one():
    labels = ["low", "high", "low", "critical"]
    assert cohen_kappa(labels, labels) == pytest.approx(1.0)


def test_kappa_matches_textbook_example():
    # 2x2 table: yes/yes=20, yes/no=5, no/yes=10, no/no=15 -> kappa = 0.4
    a = ["yes"] * 25 + ["no"] * 25
    b = ["yes"] * 20 + ["no"] * 5 + ["yes"] * 10 + ["no"] * 15
    assert cohen_kappa(a, b) == pytest.approx(0.4)


def test_weighted_kappa_penalises_distant_disagreement_more():
    order = ["low", "medium", "high", "critical"]
    gold = ["low", "medium", "high", "critical"] * 5
    near = ["low", "medium", "critical", "critical"] * 5
    far = ["critical", "medium", "high", "critical"] * 5
    assert weighted_kappa(gold, near, order) > weighted_kappa(gold, far, order)


def test_export_is_blind_and_complete(tmp_path):
    out = tmp_path / "sheet.csv"
    n = export_sheet(out)
    with out.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    assert n == len(rows) == len(load_manual_corpus())
    assert all(r[field] == "" for r in rows for field in MANUAL_FIELDS)


def test_score_self_agreement_is_perfect(tmp_path):
    sheet = tmp_path / "sheet.csv"
    records = load_manual_corpus()
    with sheet.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "text", "english_gloss", *MANUAL_FIELDS])
        for r in records:
            writer.writerow([r["id"], r["text"], r["english_gloss"], *[r[k] for k in MANUAL_FIELDS]])
    report = score_sheet(sheet)
    assert report["n_items"] == len(records)
    for entry in report["fields"].values():
        assert entry["percent_agreement"] == 1.0
        assert entry["disagreements"] == []
