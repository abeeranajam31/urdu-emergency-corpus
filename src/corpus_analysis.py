"""Core corpus-linguistic analysis functions: tokenization, frequency,
keyness, and collocation.

Tokenization here is a simple whitespace/punctuation split. This is a
known simplification for Urdu (ligatures, clitics, and orthographic
variation are not handled) and is documented as a limitation in
paper/research_report.md — it's adequate for a pilot corpus at this size,
not a production Urdu tokenizer.
"""

from __future__ import annotations

import re
from collections import Counter

import pandas as pd

_PUNCT_RE = re.compile(r"[،۔!؟?,.!؛;:\"'،؟]")


def shape_for_display(text: str) -> str:
    """Reshape + reorder Urdu/Arabic-script text for correct rendering in
    matplotlib, which does not do Arabic text shaping/bidi on its own
    (unlike a browser or a proper text layout engine). Only needed for
    chart labels — plain print()/DataFrame output in a notebook renders
    correctly via the browser without this.
    """
    import arabic_reshaper
    from bidi.algorithm import get_display

    return get_display(arabic_reshaper.reshape(text))


def tokenize(text: str) -> list[str]:
    cleaned = _PUNCT_RE.sub(" ", text)
    return [tok for tok in cleaned.split() if tok]


def corpus_to_dataframe(records: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(records)
    df["tokens"] = df["text"].apply(tokenize)
    df["token_count"] = df["tokens"].apply(len)
    return df


def word_frequencies(df: pd.DataFrame, subset: pd.Series | None = None) -> Counter:
    rows = df[subset] if subset is not None else df
    counter: Counter = Counter()
    for tokens in rows["tokens"]:
        counter.update(tokens)
    return counter


def keyness_table(
    df: pd.DataFrame, group_field: str, target_value, reference_values=None, smoothing: float = 0.5
) -> pd.DataFrame:
    """Simple relative-frequency keyness: ratio of a word's normalized
    frequency (per 1,000 tokens) in the target group vs. the reference
    group(s), with additive smoothing on the per-1,000 rates. This is a
    deliberately simple keyness measure (not log-likelihood / LL-BIC) —
    appropriate for a pilot corpus of this size, documented as a
    simplification in the limitations section.

    `smoothing` is added to both the target and reference per-1,000 rates
    before dividing, so a word absent from the reference group produces a
    large-but-bounded ratio rather than an artifact of dividing by ~zero.
    """
    target_mask = df[group_field] == target_value
    if reference_values is None:
        reference_mask = ~target_mask
    else:
        reference_mask = df[group_field].isin(reference_values)

    target_counts = word_frequencies(df, target_mask)
    reference_counts = word_frequencies(df, reference_mask)

    target_total = sum(target_counts.values()) or 1
    reference_total = sum(reference_counts.values()) or 1

    rows = []
    vocab = set(target_counts) | set(reference_counts)
    for word in vocab:
        target_rate = target_counts.get(word, 0) / target_total * 1000
        reference_rate = reference_counts.get(word, 0) / reference_total * 1000
        keyness = (target_rate + smoothing) / (reference_rate + smoothing)
        rows.append(
            {
                "word": word,
                "target_count": target_counts.get(word, 0),
                "reference_count": reference_counts.get(word, 0),
                "keyness_ratio": round(keyness, 2),
            }
        )

    return pd.DataFrame(rows).sort_values("keyness_ratio", ascending=False).reset_index(drop=True)


def collocates(df: pd.DataFrame, node_word: str, window: int = 3) -> Counter:
    """Word co-occurrence counts within `window` tokens of `node_word`,
    across the whole corpus (or a pre-filtered subset of df).
    """
    counter: Counter = Counter()
    for tokens in df["tokens"]:
        for i, tok in enumerate(tokens):
            if tok != node_word:
                continue
            start = max(0, i - window)
            end = min(len(tokens), i + window + 1)
            for j in range(start, end):
                if j != i:
                    counter[tokens[j]] += 1
    return counter
