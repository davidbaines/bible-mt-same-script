# Spec: same-script multi-source series (v2)

Follow-on to `bible-interlingua` in the closed-text Bible-MT line
(`m2m_bible_mt` → `ebible-mt` → `bible-interlingua` → here). Everything trains
only on the eBible corpus (`DavidCBaines/ebible_corpus`), shareable licences
only. Design settled in the 2026-07-23 interview; v2 (this repo) re-runs the
whole series on the shared `synoptic` toolkit after a code review found
defects live during v1 (see `experiments/v1-reference/README.md`). The
toolkit is a pinned git dependency — see `pyproject.toml`; local dev uses the
sibling `../synoptic` checkout via `[tool.uv.sources]`.

v2 methodology changes against v1:

- **Validation set** (the early-stopping set; v1 called it a "probe") is 250
  random verses per target language, disjoint from BOTH training and test
  material; silnlp early stopping (chrF3 every 1000 steps, stop when no +0.2
  gain within 4000 steps).
- Test sets no longer shrink to the source translation's coverage; `<range>`
  markers cannot feed the source side; verse-level holdouts are validated;
  source-side leakage is asserted; `companion_ranking: coverage` is explicit
  in every config (v1's implicit behaviour).
- Weights: chunked artifact upload (150 MB parts + sha256 manifest;
  `python -m synoptic.fetch_weights` reassembles). Every run's weights get
  downloaded and kept locally; only winners are published.

## Question

Does the multi-source fusion gain (+2.5–2.9 chrF3 at K=8 in the mixed-script
Indo-European pool) reproduce when every source and target shares one script,
and is a single-script model practical for drafting scripture in a low-resource
target language of that script?

## Design

### Scripts and pools

Pool criterion: shareable licence (Public Domain / by / by-sa — by-nc unlocks
no extra scripts) and ≥7000 total verses per text. Full Bibles are not
required; that is what makes Ethiopic and Telugu viable.

| Script | Pool (translationIds) | Target languages | Source | Notes |
|---|---|---|---|---|
| Devanagari | hin2017, hne, mar, goj, gok, hlb, sandev, thr | **hne** (Chhattisgarhi), **mar** (Marathi) | hin2017 (alignment-confirmed) | `marc` excluded: duplicate Marathi would leak into mar's test sets |
| Arabic | arbnav, arb-vd, ckb, pesOPV, urdoucv, sanurd | **ckb** (Central Kurdish), **urd** (Urdu) | pesOPV (Persian; eflomal winner for both targets) | |
| Ethiopic | gmve, gofe, gyl, jnje, oyde | **gmv** (Gamo), **gof** (Goofa) | the other OT text per run | Drafting condition: one target per run (only two OT texts exist) |
| Telugu | tel2017, nit, santel, vgr | **nit**, **vgr** (NT-only) | tel2017 (forced: only OT text) | Conditions collapse (targets have no OT); NT test sets only; minimum-pool stress test |
| Latin (Bantu control) | kik, lin, lug, nde, nya, sna, swh (one text per language) | **nde** (Ndebele), **nya** (Chichewa) | sna (chiShona; both scorers agree) | Non-source pool OTs truncated to NT so the pool structure (1 full-OT source + NT-only rest + 2 full-OT targets) mirrors Devanagari |

The Latin control is family-coherent and profile-matched to Devanagari to
separate the script effect from pool size, coverage mix, and relatedness.

### Conditions

- **Drafting**: the target language trains on its NT only, minus the NT test
  sets. Its whole available OT is generated and scored — per book and as a
  whole-OT aggregate.
- **Gap-filling**: the target language trains on everything it has minus the
  test sets (NT test sets plus Genesis-250 where the language has Genesis).

### Test sets (identical across all experiments)

- **Mark-678**: the whole book of Mark. Partial-book training would be an
  unusual real case; whole-Mark is the NT upper-bound score.
- **Epistles-274**: all of James + 1 Peter + 2 Peter (108 + 105 + 61).
- **Drafting only**: whole available OT, scored per book plus aggregate (to
  learn which OT books are easiest).
- **Gap-filling only**: Genesis-250, a fixed random 250-verse selection from
  Genesis (committed at `configs/test-verses-gen250.txt`, fixed seed), where
  the target language has Genesis.

### Source

The composite Greek of the previous series is replaced by the **best-aligned
single full-coverage language** in each script pool, ranked with IBM-1
alignability (`samileides.align_score`) and cross-checked with eflomal.
Decided 2026-07-23 (`experiments/source-ranking.csv`): Devanagari hin2017
(both scorers agree), Arabic pesOPV (eflomal winner on both targets; IBM-1
mildly preferred arb-vd), Latin control sna (both agree), Telugu tel2017
(forced). Ethiopic is forced per run. The
source is forced first in every multi-source line and is the source of the
single-source baseline. The source language cannot be a target.

### Runs

Per script × condition: one K=8 multi-source run + one single-source baseline
run, both target languages held out together. Exceptions:

- Ethiopic runs one target at a time in BOTH conditions (the other OT text is
  the source): gmve and gofe are the only OT texts, so a packed run would
  leave the held-out OT — or the shared Genesis-250 — with zero source
  renderings at inference.
- Telugu: one condition only (2 runs total).

≈ 22 H100 runs: Devanagari 4, Arabic 4, Ethiopic 8, Telugu 2, Latin 4.

Sampling: K=8 with k_min=1, source forced first, as in `ms8_ie_shareable`; the
sampler caps at the renderings actually available. Model/training hyperparams
inherit from bible-interlingua's `ms8_ie_shareable.yaml` (210M transformer,
32k vocab, max_src_len 640).

### Known structural caveats (record in the writeup)

- Drafting-condition OT source coverage is thin: Devanagari OT verses have
  only Hindi as source; Ethiopic only one text.
- Ethiopic drafting has zero OT training pairs — its OT score measures
  cross-testament generalisation from NT-only training.
- Telugu can never form OT training pairs; it answers the NT-only fusion
  question at minimum pool size.

## Implementation

New code lives in this repo; `samileides` is vendored from
`../bible-interlingua/src/samileides` (plus `align_score.py` from
`../m2m_bible_mt`). Dropped modules: `greek.py`, `anchors.py`, `attach.py`,
`train_attach.py`, `coverage.py` (attach track skipped this series).

1. **Scaffold**: `pyproject.toml` copied from bible-interlingua — keep the
   torch `>=2.4,<2.7` cu124 cap and train deps as a default group (ClearML
   poetry agents).
2. **`script_pool.py`** (analogue of `family.py`): select shareable texts with
   ≥7000 total verses by the metadata `script` column; support excluded ids
   (marc, duplicate swh texts), per-text NT-truncation (Bantu control), forced
   target inclusion. Emits `experiments/selection-<script>.csv`. Run the
   `data-licence-check` skill at selection build; expected model licence
   cc-by-sa-4.0.
3. **`scripts/alignment/rank_sources.py`**: for each script pool, score every
   full-coverage candidate against the pool's target languages with IBM-1
   `alignability` and the eflomal helper (adapted from
   `m2m_bible_mt/scripts/alignment/run_eflomal.py`; its hardcoded venv paths
   must be re-pointed — new eflomal venv on the 3090). Output
   `experiments/source-ranking.csv`. The eflomal winner (IBM-1 sanity
   cross-check) becomes the script's source.
4. **`source.py`** replaces `greek.py`: the source is the chosen translation's
   verse series (vref-indexed, empty where absent). Rewire
   `data_pipeline.prepare` and `multisource.py` — the `GREEK_CODE`
   special-casing becomes a configurable source translation id.
5. **Verse-level holdouts**: extend `holdouts.py`/`splits.py` from
   per-translation whole-OT holdouts to holdout sets — (whole OT ∪ Mark ∪
   Epistles) for drafting targets, (Mark ∪ Epistles ∪ Genesis-250) for
   gap-filling targets. The leakage rule (`present_by_vref`: held-out cells
   never feed the source side) extends unchanged. The dev/probe split must
   exclude test-set verses for target languages.
6. **Configs**: one YAML per run under `configs/experiments/`, holdout YAMLs
   per script × condition.
7. **Evaluation**: `evaluate.py` (chrF3 headline — CHRF char_order=6 beta=3 —
   plus chrF3++/spBLEU/BLEU, copy and best-other-copy baselines), extended
   with per-test-set and per-OT-book reporting. Qualitative sheets via
   `sheets.py`.
8. **Run order**: smoke run on the 3090 first (tiny pool, few steps,
   exercises the new holdout and source paths end-to-end), then per script on
   ClearML H100 queue `jobs_backlog` (custom docker image, `--remote-queue`;
   artifact uploads have failed on SSL before — keep scores in console logs).
   Devanagari → Arabic → Ethiopic → Telugu → Latin control.
   **Submission limit**: enqueue a job only when a free worker exists —
   check with `~/Documents/Github/clearml_status.py` (exit 0 = safe to
   enqueue; capacity is shared with other agents' sessions). Jobs run
   ~90 minutes; poll adaptively. Git operations always via `git -C`
   this repo.
9. **Results**: `experiments/<script>-results.md` per script + a series
   summary comparing gains with the mixed-script +2.5–2.9 reference; publish
   the best per-script models to HF (cc-by-sa-4.0) as in prior series.

## Series v2 (pending)

The 2026-07-25 code review (written up in
`../bible-mt-family-transfer/experiments/code-review-findings.md`) confirmed
defects that were live during the 22 v1 runs: checkpoint selection used
verses drawn from the test sets (gap-filling scores most biased, ~21%
overlap); test sets silently shrank to the source translation's coverage
(Ethiopic "whole OT" especially); `<range>` markers passed through as source
text (Telugu/Ethiopic baselines); `hf_export` still writes Greek source
metadata. v1 numbers stay in `experiments/` as-is, marked by these caveats.

Agreed for v2 (2026-07-25): the early-stopping set is called the
**validation set** (not "probe") and must be disjoint from BOTH training and
test sets — 250 random verses per target language, withheld from training.
Exact patience/min-gain to be set when the re-run starts (silnlp reference:
improve by 0.2 within 4000 steps, computed every 1000). Full 22-run re-run
on fixed code; blocked until the family-transfer review fixes land in the
shared code, and the repo-versioning question (tag v1 in place vs new repo)
is settled. Weights: chunked artifacts (size threshold being probed); every
v2 model gets downloaded and kept locally while disk allows; only models
worth publishing are published.

## Verification

- **Selection**: selections match the pool table above exactly; licence check
  passes with no offenders; Bantu truncation leaves only the source with OT
  verses among non-target pool members.
- **Holdouts/leakage**: an automated check asserts no held-out
  (vref, translation) cell ever appears on the source side of any training or
  inference pair; test-set verses are absent from the target's train and dev
  splits. Genesis-250 list is stable (fixed seed, committed file).
- **Alignment ranking**: IBM-1 and eflomal rankings both reported; sanity —
  hin2017 must win Devanagari; tel2017 is forced in Telugu.
- **Smoke run**: a tiny 3090 run trains, generates, and scores every test set
  end-to-end before any H100 spend.
- **Per-run**: probe curves early-stop as in prior series; every chrF3 is
  compared against its copy baselines — fusion must clear the copy floor to
  count as a result.
- **Series answer**: per script, K=8 minus baseline gain on each test set,
  side by side with the mixed-script +2.5–2.9 reference.
