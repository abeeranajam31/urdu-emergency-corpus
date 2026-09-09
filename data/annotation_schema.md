# Annotation Schema

Each utterance in `corpus.jsonl` carries the following fields. Fields are
split into **manually annotated** (require semantic/pragmatic judgment) and
**lexicon-tagged** (detected automatically against a curated word list, then
spot-checked manually) — this distinction is deliberate and is discussed in
the methodology section of `paper/research_report.md`.

## Core fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Stable identifier, `UEC-###`. |
| `text` | string | The utterance, in Urdu script. |
| `english_gloss` | string | A rough English gloss (not a certified translation) so non-Urdu-reading reviewers can follow the corpus. |

## Manually annotated fields

These require judgment about meaning and context, not just word presence.

| Field | Values | Notes |
|---|---|---|
| `emergency_type` | `medical`, `accident`, `fire`, `crime`, `other` | The situation category. |
| `urgency` | `low`, `medium`, `high`, `critical` | Annotator's judgment of perceived time-pressure and severity, following the working definitions below. |
| `speech_act` | `request`, `information`, `warning`, `distress`, `command` | The dominant speech act of the utterance (Searle-style categories, simplified for this domain). |
| `person_reference` | `first`, `third`, `both`, `none` | Whether the speaker refers to themselves, a third party, both, or neither (impersonal hazard descriptions, e.g. "a pothole has formed on the road"). |
| `repetition` | boolean | Whether a word or short phrase is repeated for emphasis (e.g. "جلدی جلدی"). |

### Working urgency definitions

- **Low** — no immediate danger; informational or minor request.
- **Medium** — a real problem requiring attention soon, not immediately life-threatening.
- **High** — active danger or significant harm; response needed quickly.
- **Critical** — life-threatening, ongoing harm, or imminent danger; response needed immediately.

## Lexicon-tagged fields

Detected by `src/preprocessing.py` via substring match against the lexicons
below, then spot-checked. This is a deliberate methodological choice: it
keeps these four categories reproducible and auditable (anyone can rerun the
tagging), rather than resting entirely on one annotator's judgment.

| Field | Lexicon (Urdu) | Gloss |
|---|---|---|
| `temporal_expression` | ابھی، فوراً، جلدی، کل، کچھ دیر پہلے | now, immediately, quickly, tomorrow/yesterday, a while ago |
| `distress_marker` | خدا، پلیز، مدد، بچاؤ، بچائیں | God (invocation), please, help, save (imperative/noun) |
| `intensifier` | بہت، انتہائی، بالکل، فوراً | very, extremely, completely, immediately |
| `negation` | نہیں، نہ | no/not |

Each of these fields is stored as `{"present": bool, "matches": [tokens]}`.

## Known limitations of this schema

- Urgency and speech-act labels come from a single annotator (the corpus
  author) at this pilot stage — no inter-annotator agreement has been
  computed. See `paper/research_report.md` for the full limitations
  discussion.
- Lexicon-based tagging will miss morphological variants and synonyms not
  in the list; it is a screening tool, not a semantic parser.
- Simple substring matching can over-match inside longer words; this is a
  known simplification at this corpus size and was spot-checked manually
  but not exhaustively verified.
