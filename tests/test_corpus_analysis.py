import pandas as pd

from src.corpus_analysis import collocates, corpus_to_dataframe, keyness_table, tokenize, word_frequencies


def test_tokenize_splits_on_whitespace_and_punctuation():
    tokens = tokenize("فوراً مدد بھیجیں، جلدی کریں!")
    assert tokens == ["فوراً", "مدد", "بھیجیں", "جلدی", "کریں"]


def test_tokenize_handles_empty_string():
    assert tokenize("") == []


def _sample_records():
    return [
        {"id": "T1", "text": "فوراً مدد بھیجیں", "urgency": "critical"},
        {"id": "T2", "text": "فوراً ایمبولینس بھیجیں", "urgency": "critical"},
        {"id": "T3", "text": "کیا حال ہے آج", "urgency": "low"},
        {"id": "T4", "text": "موسم آج اچھا ہے", "urgency": "low"},
    ]


def test_corpus_to_dataframe_adds_token_columns():
    df = corpus_to_dataframe(_sample_records())
    assert "tokens" in df.columns
    assert "token_count" in df.columns
    assert df.loc[df["id"] == "T1", "token_count"].iloc[0] == 3


def test_word_frequencies_counts_across_corpus():
    df = corpus_to_dataframe(_sample_records())
    freq = word_frequencies(df)
    assert freq["فوراً"] == 2
    assert freq["بھیجیں"] == 2
    assert freq["ہے"] == 2


def test_word_frequencies_respects_subset_mask():
    df = corpus_to_dataframe(_sample_records())
    mask = df["urgency"] == "critical"
    freq = word_frequencies(df, mask)
    assert freq["فوراً"] == 2
    assert "کیا" not in freq


def test_keyness_table_ranks_target_exclusive_word_highest():
    df = corpus_to_dataframe(_sample_records())
    key_df = keyness_table(df, "urgency", "critical", ["low"])
    top_word = key_df.iloc[0]["word"]
    assert top_word in {"فوراً", "بھیجیں"}
    assert key_df.iloc[0]["reference_count"] == 0


def test_keyness_table_does_not_divide_by_zero():
    df = corpus_to_dataframe(_sample_records())
    key_df = keyness_table(df, "urgency", "critical", ["low"])
    assert key_df["keyness_ratio"].isna().sum() == 0
    assert (key_df["keyness_ratio"] < float("inf")).all()


def test_collocates_finds_cooccurring_words_within_window():
    df = corpus_to_dataframe(_sample_records())
    coll = collocates(df, "فوراً", window=2)
    assert coll["بھیجیں"] >= 1
