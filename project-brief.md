# Project brief: same-script multi-source

A follow-on to `bible-interlingua` in the closed-text Bible machine-translation
line (`m2m_bible_mt` → `ebible-mt` → `bible-interlingua` → here). The purpose of
this line of work is machine translation for languages whose only available text
is parts of the Bible. Everything is trained only on the eBible corpus
(`DavidCBaines/ebible_corpus`), so the scores are a from-scratch baseline.

## The question

Can we reproduce the multi-source fusion result from `bible-interlingua` 
in scripts other than Latin script?

The `bible-interlingua` multi-source experiment mixed scripts: the source was
the composite Koine Greek (Greek script) and the targets spanned several
scripts. This series keeps every source and target in one script. That means
Greek can no longer be the source as it is in a different script. We need a
source chosen according to its alignment between the Bibles available in the script.
The question is whether we get better or worse results when working within a single 
script. It won't be possible to hold all the factors the same since there will be
many fewer texts available in each script. We want to discover whether working within
a single script can create a model that is practical for drafting an OT in a 
low-resource language in the script.

## What bible-interlingua established (inherited, do not re-derive)

- **Baselines and method**: single-source `ie_big_shareable` 47.01 / 37.03 /
  43.82 chrF3; multi-source K=8 gains +2.5–2.9; the attach ladder (graft 9.25 /
  single-slot anchor 22.07 / 8-slot anchor 25.09 vs upper bound 42.05).
- **Method finding**: content supplied at inference (multi-source) beats a
  frozen interlingua; the NT→OT vocabulary cap is not the limiter, anchor
  capacity is.
- **Toolkit**: the `samileides` package (multi-source sampler, per-verse
  anchors, attach graft + single/multi-slot decoder, coverage instrumentation)
  and the ClearML H100 recipe. The composite Greek source is built by
  `greek.py`; this series needs a new in-script source instead.

## What to test (each target: multi-source K=8 plus the attach ladder)

1. **Single-script multi-source.** Pick a script with enough shareable
   languages to form a multi-source pool, build a single-script training pool,
   hold out one language's whole OT, and draft it with multi-source fusion.
   Candidate scripts: Latin (many languages), Devanagari (Indic languages such
   as Hindi, Marathi, Nepali, Sanskrit), Arabic (Arabic, Persian, Urdu, Central
   Kurdish). Compare the gain to the mixed-script `bible-interlingua` result.
2. **In-script source by alignment.** No Greek. Choose the source — a single
   best-aligned language, or a composite of in-script languages — using
   alignment scores between the available sources. Reuse the alignment scoring
   from `m2m_bible_mt` (`scripts/alignment`, eflomal).

## Prerequisites

- A **new in-script source** builder to replace the composite Greek in
  `greek.py`, plus a way to rank candidate sources by alignment score.
- A single-script selection: a by-script selector, or reuse the family tooling
  where a script maps cleanly to a family (e.g. Devanagari ≈ Indic).

## To decide in the interview

- Which script (and whether to run more than one).
- The source: one best-aligned language or a composite, and how alignment
  chooses it.
- The held-out target (needs at least 250 verses as a test set to score against).
- We will reduce the test set in order to allow texts that are just the NT to 
  form part of the experiment. Otherwise there may be too few texts available.
- How to score the results.

## Constraints

- Compute: remote H100s via ClearML queue `jobs_backlog`; the A100 for research
  runs; the local 3090 for smoke tests, data prep and alignment scoring.
  ClearML worker recipe is in `../ebible-mt/spec.md` and the vendored
  `train.py`.
- Publishing / licence policy carries over: publishable runs use a
  shareable-only selection; run `data-licence-check` at selection build.
  Aggregate scores and curves are always shareable.

## Data source

Hugging Face dataset `DavidCBaines/ebible_corpus`.

## Reuse

Vendor the `samileides` core from `../bible-interlingua/src/samileides` — it
carries the multi-source and attach toolkit. The new code is the in-script
source builder and the alignment-based source ranking (the latter can be
adapted from `../m2m_bible_mt/scripts/alignment`). Decide during planning and
vendor after the brief is settled rather than before.

## Approach

Run `/interview-and-plan project-brief.md` then write `plan.md` and `todo.md`.
