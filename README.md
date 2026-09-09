# Urdu Emergency Communication Corpus (UEC)

**Linguistic Signals of Urgency in Urdu Emergency Communication: A Corpus-Based and Computational Study**

An independent corpus-linguistics research project: a small, balanced,
annotated pilot corpus of simulated Urdu emergency-communication
utterances, analyzed with standard corpus-linguistic methods (frequency,
keyness, collocation) to identify which linguistic features distinguish
low- from high-urgency communication.

> **Independent research project, not affiliated with any institution.**
> This is a separate project from [VERIAUDIT](https://github.com/abeeranajam31/veriaudit)
> (my AI safety evaluation platform) — different domain, different
> methodology, no shared codebase, kept intentionally as its own repo.

## Research question

Which linguistic features (temporal expressions, distress markers,
intensifiers, negation, repetition, lexical choice) distinguish different
levels of urgency in Urdu emergency communication — and can standard
corpus-linguistic methods surface them without assuming the answer in
advance?

**Full write-up:** [`paper/research_report.md`](paper/research_report.md)

## Key findings (pilot scale, n=60)

- Lexical **repetition** (e.g. `جلدی جلدی` "quickly quickly") is exclusive
  to high/critical urgency utterances (0% at low/medium, 40% at critical)
  — an emergent pattern, not one built into the annotation scheme.
- **Distress markers** appear in 100% of critical-urgency utterances.
- **Utterance length does not track urgency** in any clear direction —
  ruling out a naive "urgent = longer/shorter" heuristic.
- The highest-keyness words distinguishing high/critical from low/medium
  utterances span temporal expressions, imperative verbs, and distress
  invocations together (`جلدی` 106.5x, `فوراً` 56.3x, `آئیں` 51.3x) — no
  single word category alone drives the distinction.

See the [research report](paper/research_report.md) for the full results,
discussion, and — importantly — limitations.

## Repository structure

```
urdu-emergency-corpus/
├── data/
│   ├── corpus_manual.jsonl      manually annotated core fields (60 utterances)
│   ├── corpus.jsonl             + lexicon-tagged fields (generated)
│   └── annotation_schema.md     full schema documentation
├── notebooks/
│   ├── 01_corpus_statistics.ipynb
│   └── 02_keyword_collocation_analysis.ipynb
├── src/
│   ├── preprocessing.py         lexicon-based auto-tagging
│   └── corpus_analysis.py       tokenization, frequency, keyness, collocation
├── results/                     generated charts (PNG)
├── paper/
│   └── research_report.md       full write-up
├── tests/                       pytest suite
└── requirements.txt
```

## Data note

**This is a researcher-constructed, simulated pilot corpus — not real
emergency-call transcripts.** Utterances were authored to be
typologically representative across 5 situation types × 4 urgency levels
× 3 variants, balanced by design. Real emergency-call data raises consent
and privacy issues out of scope for this pilot; see
[`paper/research_report.md`](paper/research_report.md#4-dataset) for the
full rationale and [`data/annotation_schema.md`](data/annotation_schema.md)
for the annotation methodology.

## Reproduce

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Regenerate the lexicon-tagged corpus from the manually annotated source
python -m src.preprocessing

# Run the analysis notebooks
jupyter notebook notebooks/

# Run tests
pytest
```

## Method summary

1. **Corpus construction** — 60 utterances, balanced across emergency
   type (medical/accident/fire/crime/other) and urgency (low/medium/
   high/critical).
2. **Manual annotation** — emergency type, urgency, speech act, person
   reference, repetition (single annotator; see limitations).
3. **Lexicon-based tagging** — temporal expressions, distress markers,
   intensifiers, negation, tagged reproducibly via `src/preprocessing.py`.
4. **Corpus-linguistic analysis** — frequency, keyness (relative-frequency
   ratio with smoothing), and window-based collocation
   (`src/corpus_analysis.py`).

## Limitations (short version)

Simulated (not real) data; single annotator with no inter-annotator
agreement measured; small sample (n=60); simple keyness/tokenization
methods appropriate to pilot scale, not production-grade. Full discussion:
[`paper/research_report.md`](paper/research_report.md#8-limitations).

## License

[MIT](LICENSE)

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

## Contact

Abeera Najam — [abeeranajam@gmail.com](mailto:abeeranajam@gmail.com)
