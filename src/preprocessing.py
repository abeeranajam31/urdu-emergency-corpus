"""Loads the manually annotated corpus and applies lexicon-based tagging
for temporal expressions, distress markers, intensifiers, and negation.

This split is deliberate: urgency, emergency type, speech act, person
reference, and repetition require semantic/pragmatic judgment and are
annotated manually (data/corpus_manual.jsonl). Temporal expressions,
distress markers, intensifiers, and negation are lexicon-detectable, so
they're tagged programmatically here — reproducible and auditable by
anyone who reruns this script, rather than resting entirely on one
annotator's by-hand tagging of every field.

See data/annotation_schema.md for the full schema and known limitations.
"""

from __future__ import annotations

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
MANUAL_CORPUS_PATH = DATA_DIR / "corpus_manual.jsonl"
OUTPUT_CORPUS_PATH = DATA_DIR / "corpus.jsonl"

LEXICONS: dict[str, list[str]] = {
    "temporal_expression": ["ابھی", "فوراً", "جلدی", "کل", "کچھ دیر پہلے"],
    "distress_marker": ["خدا", "پلیز", "مدد", "بچاؤ", "بچائیں"],
    "intensifier": ["بہت", "انتہائی", "بالکل", "فوراً"],
    "negation": ["نہیں", "نہ"],
}


def load_manual_corpus(path: Path = MANUAL_CORPUS_PATH) -> list[dict]:
    records = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def tag_lexicon_fields(text: str) -> dict:
    tags = {}
    for field, lexicon in LEXICONS.items():
        matches = [word for word in lexicon if word in text]
        tags[field] = {"present": len(matches) > 0, "matches": matches}
    return tags


def build_annotated_corpus(
    manual_path: Path = MANUAL_CORPUS_PATH, output_path: Path = OUTPUT_CORPUS_PATH
) -> list[dict]:
    records = load_manual_corpus(manual_path)
    annotated = []
    for record in records:
        record = {**record, **tag_lexicon_fields(record["text"])}
        annotated.append(record)

    with output_path.open("w", encoding="utf-8") as f:
        for record in annotated:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return annotated


if __name__ == "__main__":
    corpus = build_annotated_corpus()
    print(f"Wrote {len(corpus)} annotated records to {OUTPUT_CORPUS_PATH}")
