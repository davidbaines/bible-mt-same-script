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
| Latin (Bantu control) | kik, lin, lug, nde, nya, sna, swhonen (one text per language) | **nde** (Ndebele), **nya** (Chichewa) | sna (chiShona; both scorers agree) | Non-source pool OTs truncated to NT so the pool structure (1 full-OT source + NT-only rest + 2 full-OT targets) mirrors Devanagari |

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

## Implementation (v2)

The toolkit is the `synoptic` package (sibling repo / pinned git dependency);
this repo holds only experiment material:

- `scripts/pools.py` — the five PoolSpec definitions + CLI over
  `synoptic.script_pool` (selections in `experiments/selection-*.csv`).
- `scripts/alignment/rank_sources.py` — IBM-1 + eflomal source ranking
  (`experiments/source-ranking.csv`). Needs a local eflomal venv:
  `uv venv .venv-eflomal && uv pip install --python .venv-eflomal/bin/python
  eflomal`. eflomal occasionally emits `inf` scores; the winner computation
  drops those rows with a note.
- `scripts/make_configs.py` — regenerates every holdout and experiment YAML
  from the ranking winners (Ethiopic sources are forced per run, never
  ranked). Deterministic: regeneration must reproduce the committed files
  (tested).
- `scripts/train.py` / `scripts/generate.py` — thin wrappers over the
  synoptic entry points, so ClearML remote execution captures THIS repo.
- Remote recipe: ClearML H100 queue `jobs_backlog` (custom docker image;
  agents install the requirements captured at enqueue plus the git-pinned
  synoptic). Weights come back as chunked artifacts
  (`python -m synoptic.fetch_weights`); scores echo to the console
  (`python -m synoptic.fetch_scores`). Enqueue only when
  `~/Documents/Github/clearml_status.py --json` shows effective_free >= 2.

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
