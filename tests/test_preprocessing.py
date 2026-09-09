import json

from src.preprocessing import build_annotated_corpus, load_manual_corpus, tag_lexicon_fields

ALLOWED_URGENCY = {"low", "medium", "high", "critical"}
ALLOWED_TYPE = {"medical", "accident", "fire", "crime", "other"}
ALLOWED_SPEECH_ACT = {"request", "information", "warning", "distress", "command"}
ALLOWED_PERSON_REF = {"first", "third", "both", "none"}
REQUIRED_FIELDS = {
    "id",
    "emergency_type",
    "urgency",
    "text",
    "english_gloss",
    "speech_act",
    "person_reference",
    "repetition",
}


def test_manual_corpus_has_sixty_records():
    records = load_manual_corpus()
    assert len(records) == 60


def test_manual_corpus_ids_are_unique():
    records = load_manual_corpus()
    ids = [r["id"] for r in records]
    assert len(ids) == len(set(ids))


def test_manual_corpus_fields_present_and_valid():
    records = load_manual_corpus()
    for r in records:
        assert REQUIRED_FIELDS.issubset(r.keys())
        assert r["urgency"] in ALLOWED_URGENCY
        assert r["emergency_type"] in ALLOWED_TYPE
        assert r["speech_act"] in ALLOWED_SPEECH_ACT
        assert r["person_reference"] in ALLOWED_PERSON_REF
        assert isinstance(r["repetition"], bool)
        assert len(r["text"]) > 0
        assert len(r["english_gloss"]) > 0


def test_manual_corpus_is_balanced_by_urgency():
    records = load_manual_corpus()
    counts = {}
    for r in records:
        counts[r["urgency"]] = counts.get(r["urgency"], 0) + 1
    assert counts == {"low": 15, "medium": 15, "high": 15, "critical": 15}


def test_tag_lexicon_fields_detects_temporal_expression():
    tags = tag_lexicon_fields("فوراً مدد بھیجیں")
    assert tags["temporal_expression"]["present"] is True
    assert "فوراً" in tags["temporal_expression"]["matches"]


def test_tag_lexicon_fields_no_false_positive_on_low_urgency_text():
    tags = tag_lexicon_fields("مجھے ہلکا سا سر درد ہے")
    assert tags["temporal_expression"]["present"] is False
    assert tags["distress_marker"]["present"] is False


def test_build_annotated_corpus_writes_valid_jsonl(tmp_path):
    output_path = tmp_path / "corpus.jsonl"
    corpus = build_annotated_corpus(output_path=output_path)
    assert len(corpus) == 60

    with output_path.open(encoding="utf-8") as f:
        lines = [json.loads(line) for line in f]
    assert len(lines) == 60
    for record in lines:
        for field in ["temporal_expression", "distress_marker", "intensifier", "negation"]:
            assert "present" in record[field]
            assert "matches" in record[field]
