"""
MLflow-tracked corpus analysis runner.

Reproduces the analysis from notebooks/01_corpus_statistics.ipynb and
notebooks/02_keyword_collocation_analysis.ipynb as a single scriptable,
trackable pipeline stage: utterance-length by urgency, lexicon-tagged
feature presence by urgency, and a keyness comparison of high/critical vs.
low/medium urgency utterances. Notebooks remain the primary place to read
and explore the analysis interactively; this script is the reproducible,
non-interactive entry point for CI, DVC, and Docker.

Usage:
    python scripts/run_analysis.py --corpus data/corpus.jsonl --results-dir results
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mlflow

from src.corpus_analysis import corpus_to_dataframe, keyness_table, shape_for_display

logger = logging.getLogger(__name__)

URGENCY_ORDER = ["low", "medium", "high", "critical"]
FEATURE_COLS = [
    "temporal_expression_present",
    "distress_marker_present",
    "intensifier_present",
    "negation_present",
    "repetition",
]


def load_corpus(corpus_path: str) -> list[dict]:
    with open(corpus_path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def run_analysis(corpus_path: str, results_dir: str, experiment_name: str = "uec-corpus-analysis") -> dict:
    mlflow.set_experiment(experiment_name)

    records = load_corpus(corpus_path)
    df = corpus_to_dataframe(records)
    for field in ["temporal_expression", "distress_marker", "intensifier", "negation"]:
        df[f"{field}_present"] = df[field].apply(lambda x: x["present"])
    df["repetition"] = df["repetition"].astype(bool)
    df["urgency_band"] = df["urgency"].map(
        {"low": "low_medium", "medium": "low_medium", "high": "high_critical", "critical": "high_critical"}
    )

    results_path = Path(results_dir)
    results_path.mkdir(parents=True, exist_ok=True)

    with mlflow.start_run(run_name="corpus-analysis"):
        mlflow.log_param("corpus_path", str(corpus_path))
        mlflow.log_param("n_utterances", len(df))

        # 1. Average utterance length by urgency
        length_by_urgency = df.groupby("urgency")["token_count"].mean().reindex(URGENCY_ORDER)
        fig, ax = plt.subplots(figsize=(6, 4))
        length_by_urgency.plot(kind="bar", ax=ax, color="#0f6b52")
        ax.set_ylabel("Average token count")
        ax.set_xlabel("Urgency")
        ax.set_title("Average utterance length by urgency")
        plt.xticks(rotation=0)
        plt.tight_layout()
        length_chart = results_path / "length_by_urgency.png"
        plt.savefig(length_chart, dpi=150)
        plt.close(fig)
        mlflow.log_artifact(str(length_chart))
        for urgency, val in length_by_urgency.items():
            if val == val:  # skip NaN (urgency levels absent from this pilot corpus)
                mlflow.log_metric(f"avg_token_count.{urgency}", float(val))

        # 2. Lexicon-tagged feature presence by urgency
        summary = df.groupby("urgency")[FEATURE_COLS].mean().reindex(URGENCY_ORDER)
        summary.columns = ["temporal", "distress", "intensifier", "negation", "repetition"]
        fig, ax = plt.subplots(figsize=(8, 5))
        summary.plot(kind="bar", ax=ax)
        ax.set_ylabel("Proportion of utterances")
        ax.set_xlabel("Urgency")
        ax.set_title("Lexicon-tagged feature presence by urgency level")
        ax.legend(loc="upper left", fontsize=8)
        plt.xticks(rotation=0)
        plt.tight_layout()
        feature_chart = results_path / "lexicon_features_by_urgency.png"
        plt.savefig(feature_chart, dpi=150)
        plt.close(fig)
        mlflow.log_artifact(str(feature_chart))
        for urgency, row in summary.iterrows():
            for feat, val in row.items():
                if val == val:
                    mlflow.log_metric(f"feature_rate.{urgency}.{feat}", float(val))

        # 3. Keyness: high/critical vs. low/medium urgency
        key_df = keyness_table(df, "urgency_band", "high_critical", ["low_medium"])
        top_key = key_df[key_df["target_count"] >= 3].head(12)
        shaped_labels = [shape_for_display(w) for w in top_key["word"][::-1]]
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.barh(shaped_labels, top_key["keyness_ratio"][::-1], color="#0f6b52")
        ax.set_yticklabels(shaped_labels, fontname="Geeza Pro", fontsize=13)
        ax.set_xlabel("Keyness ratio (high/critical vs. low/medium)")
        ax.set_title("Words characteristic of high-urgency utterances\n(min. 3 occurrences in high/critical)")
        plt.tight_layout()
        keyness_chart = results_path / "keyness_high_vs_low.png"
        plt.savefig(keyness_chart, dpi=150)
        plt.close(fig)
        mlflow.log_artifact(str(keyness_chart))

        metrics_summary = {
            "n_utterances": len(df),
            "vocab_size": len(set(tok for tokens in df["tokens"] for tok in tokens)),
            "top_keyness_words": [
                {"word": row["word"], "keyness_ratio": row["keyness_ratio"], "target_count": int(row["target_count"])}
                for _, row in top_key.head(5).iterrows()
            ],
            "avg_token_count_by_urgency": {
                k: (round(v, 2) if v == v else None) for k, v in length_by_urgency.to_dict().items()
            },
        }
        mlflow.log_metric("vocab_size", metrics_summary["vocab_size"])

        metrics_path = results_path / "metrics.json"
        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump(metrics_summary, f, indent=2, ensure_ascii=False)
        mlflow.log_artifact(str(metrics_path))

        print(f"Analyzed {len(df)} utterances — vocab size {metrics_summary['vocab_size']}")
        print(f"Top keyness words: {[w['word'] for w in metrics_summary['top_keyness_words']]}")

    return metrics_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="MLflow-tracked UEC corpus analysis runner")
    parser.add_argument("--corpus", default="data/corpus.jsonl", help="Path to corpus JSONL file")
    parser.add_argument("--results-dir", default="results", help="Directory to write charts and metrics")
    parser.add_argument("--experiment-name", default="uec-corpus-analysis", help="MLflow experiment name")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    run_analysis(args.corpus, args.results_dir, args.experiment_name)


if __name__ == "__main__":
    main()
