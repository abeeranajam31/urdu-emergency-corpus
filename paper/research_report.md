# Linguistic Signals of Urgency in Urdu Emergency Communication: A Corpus-Based and Computational Study

**Author:** Abeera Najam
**Status:** Independent research project, pilot scale. Not peer-reviewed.

## Abstract

This report investigates which linguistic features distinguish different
levels of perceived urgency in Urdu emergency communication, using a
researcher-constructed pilot corpus of 60 simulated Urdu emergency
utterances (the Urdu Emergency Communication corpus, UEC), annotated for
emergency type, urgency, speech act, person reference, repetition, and
four lexicon-tagged categories (temporal expressions, distress markers,
intensifiers, negation). Using corpus-linguistic methods — frequency
comparison, a relative-frequency keyness measure, and window-based
collocation — we find that temporal-expression and distress-marker
presence, lexical repetition, and a small set of imperative/distress
vocabulary items increase sharply between `high` and `critical` urgency
utterances, while utterance length does not track urgency in any clear
pattern. These are descriptive, pilot-scale findings, not statistically
validated claims — see Limitations.

## 1. Introduction

AI safety and NLP evaluation for emergency and crisis communication is
overwhelmingly built and tested in English. Urdu — spoken by over 230
million people — has comparatively little public corpus infrastructure
for this domain. This project asks a narrower, tractable question first:
**can we describe, with standard corpus-linguistic methods, what
distinguishes low- from high-urgency Urdu emergency utterances?** Before
any classifier is trained on urgency detection, the linguistic patterns
that would make such a classifier interpretable should be understood on
their own terms.

## 2. Related Work

This project sits between three literatures it does not attempt to
survey exhaustively: corpus linguistics and keyness/collocation methods
(e.g. the mixed quantitative/qualitative approach taught in courses such
as the University of Southampton NCRM's *"Meaning extraction from large
text data: Thematic analysis via corpus linguistics"*); emergency/crisis
NLP (typically framed as urgency or triage classification, usually in
English); and low-resource/multilingual NLP, which motivates working in
Urdu specifically rather than defaulting to English.

## 3. Research Questions

- **RQ1.** Which linguistic features (temporal expressions, distress
  markers, intensifiers, negation, repetition) distinguish different
  levels of urgency in the UEC corpus?
- **RQ2.** Which lexical items are disproportionately (keyness)
  associated with high/critical- vs. low/medium-urgency utterances?
- **RQ3.** What do the collocates of core urgency-signaling words
  (`فوراً` "immediately", `جلدی` "quickly"/"hurry") reveal about how
  urgency is linguistically constructed in this domain?

## 4. Dataset

**The UEC corpus is a researcher-constructed, simulated pilot corpus — not
a collection of real emergency-call transcripts.** Utterances were
authored by the researcher to be typologically representative of Urdu
emergency communication across five situation types (medical, accident,
fire, crime, other) and four urgency levels (low, medium, high, critical),
balanced at 3 utterances × 5 types × 4 levels = 60 utterances. This design
choice is deliberate and disclosed rather than incidental: real emergency-
call data raises non-trivial consent, privacy, and access issues that are
out of scope for a pilot project, and a balanced constructed corpus is
more appropriate for a first methodological pass than a small, unbalanced
sample of real (and harder to ethically source) data.

Each utterance carries an English gloss for non-Urdu-reading readers. Full
schema: [`data/annotation_schema.md`](../data/annotation_schema.md).

Annotation approach: `emergency_type`, `urgency`, `speech_act`,
`person_reference`, and `repetition` were manually annotated by the
researcher (single annotator — see Limitations). `temporal_expression`,
`distress_marker`, `intensifier`, and `negation` were tagged automatically
via a curated Urdu lexicon (`src/preprocessing.py`), making that portion
of the annotation reproducible by rerunning the script against the raw
corpus.

## 5. Corpus Methodology

- **Frequency**: token counts overall and by group (`src/corpus_analysis.py::word_frequencies`).
- **Keyness**: relative-frequency ratio (per 1,000 tokens, with additive
  smoothing) between high/critical and low/medium urgency bands
  (`keyness_table`). This is a simple measure, not log-likelihood/LL-BIC —
  appropriate at this corpus size, not a substitute for a validated
  statistical keyness test at larger scale.
- **Collocation**: window-based (±3 token) co-occurrence counts around a
  node word (`collocates`).
- **Tokenization**: whitespace/punctuation split — a known simplification
  for Urdu (clitics, ligatures, and orthographic variation are not
  handled); adequate at pilot scale, not production-grade.

## 6. Results

### 6.1 Corpus composition

60 utterances, perfectly balanced: 15 per urgency level, 12 per emergency
type, 3 per (type × urgency) cell (`notebooks/01_corpus_statistics.ipynb`).

### 6.2 Utterance length by urgency

| Urgency | Mean tokens |
|---|---|
| low | 12.47 |
| medium | 13.13 |
| high | 12.20 |
| critical | 14.33 |

Length does **not** increase monotonically with urgency — critical
utterances are longest on average, but high-urgency utterances are
shortest, comparable to low. This argues against "longer = more urgent"
as a naive heuristic, and toward the lexical/structural features examined
below.

### 6.3 Lexicon-tagged feature presence by urgency

| Urgency | Temporal | Distress | Intensifier | Negation | Repetition |
|---|---|---|---|---|---|
| low | 0.47 | 0.00 | 0.00 | 0.00 | 0.00 |
| medium | 0.40 | 0.07 | 0.07 | 0.13 | 0.00 |
| high | 0.80 | 0.27 | 0.60 | 0.07 | 0.00 |
| critical | 0.93 | **1.00** | 0.40 | 0.27 | 0.40 |

Distress markers appear in **100%** of critical utterances and roughly a
quarter of high-urgency ones, essentially never in low/medium — expected
given the lexicon's composition (خدا، پلیز، مدد، بچاؤ), but confirms these
items function as strong urgency signals rather than being noise.
Repetition (e.g. `جلدی جلدی`) is exclusive to high/critical (peaking at
40% of critical utterances) and absent from low/medium — a genuinely
interesting emergent pattern the annotation scheme did not force. Temporal
expressions climb from ~40-47% (low/medium) to 93% (critical). Intensifier
presence peaks at `high` (0.60) rather than `critical` (0.40) — a
non-monotonic pattern worth noting rather than smoothing over; a plausible
reading is that critical utterances lean on distress markers and
repetition instead of intensifying adverbs, but this is speculative at
n=15 per group.

### 6.4 Keyness (high/critical vs. low/medium)

Top keyness items (minimum 3 occurrences in the high/critical band; full
table in `notebooks/02_keyword_collocation_analysis.ipynb`):

| Word | Gloss | High/critical count | Low/medium count | Keyness ratio |
|---|---|---|---|---|
| جلدی | quickly / hurry | 21 | 0 | 106.5 |
| فوراً | immediately | 11 | 0 | 56.3 |
| آئیں | come (imperative) | 10 | 0 | 51.3 |
| بھیجیں | send (imperative) | 8 | 0 | 41.2 |
| کریں | do (imperative) | 7 | 0 | 36.2 |
| خدا | God (invocation) | 5 | 0 | 26.1 |
| سانس | breath | 5 | 0 | 26.1 |
| بچاؤ | help / save | 5 | 0 | 26.1 |
| ایمبولینس | ambulance | 4 | 0 | 21.1 |

All top items are exclusive to the high/critical band in this corpus (0
occurrences in low/medium) — consistent with a domain where temporal
urgency, imperative commands, and distress invocation cluster together
linguistically, rather than any one category alone driving the effect.

### 6.5 Collocates

`فوراً` ("immediately") collocates most with آئیں "come" (5), بھیجیں
"send" (4), مدد "help" (2), پلیز "please" (2) — clustering around
imperative requests for action. `جلدی` collocates most with its own
reduplicated form جلدی (12; i.e. `جلدی جلدی`), آئیں "come" (9), بھیجیں
"send" (5), ایمبولینس "ambulance" (3) — again clustering around commands,
plus its own reduplication, directly linking §6.3's repetition finding to
a specific lexical trigger.

## 7. Discussion

Three findings stand out as the most linguistically interesting, in that
none were assumed in advance by the annotation scheme's design:

1. **Repetition is an emergent, not designed-in, urgency signal.** The
   annotation scheme flagged repetition as a category to track, but did
   not predict it would correlate this cleanly with urgency (0% at
   low/medium, 40% at critical) or that it would center almost entirely
   on one lexical item (`جلدی جلدی`).
2. **Length is a poor urgency proxy.** A naive "urgent messages are
   shorter/more clipped" or "urgent messages are longer/more elaborated"
   hypothesis is not supported — length is roughly flat across urgency
   bands.
3. **Urgency is constructed compositionally, not by any single marker
   class.** The highest-keyness items span temporal expressions,
   imperative verbs, and distress invocations together — no single
   lexical category alone accounts for the high/critical vs. low/medium
   distinction.

## 8. Limitations

- **Simulated, not real, data.** This corpus was constructed by the
  researcher for methodological demonstration. It should not be treated
  as representative of authentic Urdu emergency-call register, which real
  callers under genuine stress would likely realize differently (disfluency,
  code-switching, incomplete utterances) — the natural next step for this
  line of work, not attempted here.
- **Single annotator.** Urgency, emergency type, speech act, person
  reference, and repetition were all annotated by one person (the
  researcher). No inter-annotator agreement was computed. This is the
  single biggest limitation for any claim beyond "these are the patterns
  in this specific constructed corpus."
- **Small sample (n=60, 15 per urgency level).** Sufficient to surface
  descriptive patterns, not to support inferential statistical claims.
  Keyness ratios for low-count words should be read cautiously.
- **Simple methods by design.** Keyness here is a smoothed relative-
  frequency ratio, not log-likelihood/LL-BIC; tokenization is
  whitespace/punctuation-based, not a linguistically informed Urdu
  tokenizer. Both are documented, deliberate simplifications appropriate
  to a pilot, not claims of methodological completeness.
- **No computational/ML component in this pilot.** This report
  deliberately stops at corpus-linguistic description (frequency,
  keyness, collocation) rather than also training and comparing
  classifiers, to keep the project's distinct contribution
  linguistics-first rather than duplicating ML-evaluation work done
  elsewhere. A natural extension: test whether these corpus-derived
  features (temporal/distress/intensifier presence, repetition) predict
  urgency competitively against a transformer baseline.

## 9. Conclusion

On a small, balanced, researcher-constructed pilot corpus, standard
corpus-linguistic methods (frequency, keyness, collocation) surface
specific, non-obvious linguistic patterns distinguishing high- from
low-urgency Urdu emergency communication — most notably lexical
repetition and the compositional clustering of temporal, imperative, and
distress vocabulary. These findings motivate, but do not yet justify, a
larger, multi-annotator, real-register follow-up corpus.

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
