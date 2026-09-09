---
pretty_name: Urdu Emergency Communication Corpus (UEC)
license: mit
language:
  - ur
task_categories:
  - text-classification
  - other
tags:
  - corpus-linguistics
  - urdu
  - emergency-communication
  - discourse-analysis
  - linguistic-annotation
  - low-resource
size_categories:
  - n<1K
configs:
  - config_name: default
    data_files:
      - split: corpus
        path: corpus.jsonl
---

# Urdu Emergency Communication Corpus (UEC)

A small, balanced, annotated pilot corpus of simulated Urdu
emergency-communication utterances, built to study which linguistic
features distinguish low- from high-urgency communication using
corpus-linguistic methods (frequency, keyness, collocation analysis).

**Full project, code, executed analysis notebooks, and research report:**
[github.com/abeeranajam31/urdu-emergency-corpus](https://github.com/abeeranajam31/urdu-emergency-corpus)

## ⚠️ Important: this is a simulated, researcher-constructed corpus

**Not real emergency-call transcripts.** All 60 utterances were authored
by the researcher to be typologically representative of Urdu emergency
communication, balanced across 5 situation types and 4 urgency levels.
Real emergency-call data raises consent and privacy issues out of scope
for this pilot — see the [research report](https://github.com/abeeranajam31/urdu-emergency-corpus/blob/main/paper/research_report.md#4-dataset)
for the full rationale. Do not cite this as a naturalistic-speech corpus.

## Composition

60 utterances, perfectly balanced: 15 per urgency level (low/medium/high/
critical) × 12 per emergency type (medical/accident/fire/crime/other), 3
per (type × urgency) cell.

## Schema

| Field | Type | Description |
|---|---|---|
| `id` | string | `UEC-###` |
| `text` | string | Urdu utterance |
| `english_gloss` | string | Rough English gloss (not a certified translation) |
| `emergency_type` | string | `medical`, `accident`, `fire`, `crime`, `other` |
| `urgency` | string | `low`, `medium`, `high`, `critical` — manually annotated |
| `speech_act` | string | `request`, `information`, `warning`, `distress`, `command` |
| `person_reference` | string | `first`, `third`, `both`, `none` |
| `repetition` | bool | Manually annotated: is a word/phrase repeated for emphasis (e.g. `جلدی جلدی`)? |
| `temporal_expression` | object | `{present, matches}` — lexicon-tagged (ابھی، فوراً، جلدی، کل، کچھ دیر پہلے) |
| `distress_marker` | object | `{present, matches}` — lexicon-tagged (خدا، پلیز، مدد، بچاؤ، بچائیں) |
| `intensifier` | object | `{present, matches}` — lexicon-tagged (بہت، انتہائی، بالکل، فوراً) |
| `negation` | object | `{present, matches}` — lexicon-tagged (نہیں، نہ) |

Full annotation methodology: [`data/annotation_schema.md`](https://github.com/abeeranajam31/urdu-emergency-corpus/blob/main/data/annotation_schema.md)
in the GitHub repo.

## Loading

```python
from datasets import load_dataset

ds = load_dataset("abeeranajam31/urdu-emergency-corpus", split="corpus")
print(ds[0])
```

## Key finding (see full report for details)

Lexical repetition (e.g. `جلدی جلدی` "quickly quickly") is exclusive to
high/critical-urgency utterances (0% at low/medium, 40% at critical) — an
emergent pattern the annotation scheme did not assume in advance.

## Limitations

Simulated (not real) data; single annotator, no inter-annotator agreement
measured; small sample (n=60). Full discussion:
[research report §8](https://github.com/abeeranajam31/urdu-emergency-corpus/blob/main/paper/research_report.md#8-limitations).

## Citation

```bibtex
@misc{uec_corpus_2026,
  author = {Najam, Abeera},
  title = {Linguistic Signals of Urgency in Urdu Emergency Communication: A Corpus-Based and Computational Study},
  year = {2026},
  howpublished = {Independent research project},
  url = {https://github.com/abeeranajam31/urdu-emergency-corpus}
}
```

## License

MIT

## Contact

Abeera Najam — abeeranajam@gmail.com
