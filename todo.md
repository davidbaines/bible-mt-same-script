# todo — same-script multi-source series v2

Consult `spec.md` before every change. Mark tasks `[x]` as they complete.
v1 history and scores: `experiments/v1-reference/`.

## Done

### Repo + toolkit
- [x] Rebuilt on the shared `synoptic` toolkit (pinned git dependency; local sibling for dev); train stack as plain deps for the ClearML agents.
- [x] Carried over selections, source-ranking, holdout YAMLs, Genesis-250, v1 scores (`experiments/v1-reference/`); scripts adapted (`pools.py`, `make_configs.py`, `rank_sources.py`).
- [x] 22 experiment YAMLs regenerated; repo tests pass (configs load, pools match, regeneration reproduces committed files).
- [x] Code review clean — synoptic 3 rounds, this repo 2 rounds (2026-07-26).
- [x] Old repo deleted (David) + staging renamed to `bible-mt-same-script`; runs store under the clean path.

### Weights transport (synoptic v0.3.1)
- [x] Abandoned ClearML file-server (drops bulk uploads at any chunk size); weights now go to the MinIO store silnlp uses (`~/M/MT/experiments/synoptic/<repo>/<run>/`), addressed by canonical hostname via a worker `--add-host`. Manifest guarantees completeness; preflight; `fetch_weights --run` verifies.
- [x] GATE MET: full-size round-trip verified (837 MB model uploaded complete, downloaded + manifest-verified, loads and generates Central Kurdish Genesis 1:1).

### v2 fleet (all 22 runs COMPLETE)
- [x] `scripts/run_experiments.py` launcher (≥2-free gate, paced, fail-fast, idempotent `experiments/fleet-tasks.csv`); all 22 enqueued, no failures.
- [x] All 22 scores collected (`experiments/scores-*.csv`).
- [x] Results docs + series summary + v1-vs-v2 comparison (`experiments/*-results.md`, `series-summary.md`). Headline: Arabic drafting fusion +3.2–3.8 whole-OT; Gofa target +14–16 NT (reproduced cleanly); single-OT-source pools +0–3; v1→v2 stable within ±1.

### SOTA baselines — built (synoptic.sota + scripts/sota.py)
- [x] Reusable `synoptic.sota`; code review 3 rounds clean; 18 baselines built (extracts in shared `MT/scripture` `_synsota` suffix; per-run donor test sets).
- [x] Exact-test-set mechanism verified locally (silnlp preprocess: test size 24094, byte-identical to our donor).

### SOTA baselines — COMPLETE (18/18)

- [x] All 18 NLLB-1.3B runs enqueued on `jobs_backlog` (≥2-free gate) and terminal (`experiments/sota-tasks.csv`).
- [x] Per-book chrF3 collected + compared (`scripts/sota_compare.py` → `experiments/sota/scores-*.csv`, `all-per-book.csv`, `experiments/sota-comparison.md`). `arabic_drafting_ckb` scored locally (its silnlp scoring step emitted no CSV); metric verified to reproduce silnlp to 0.00 under both sacrebleu 2.4.3 and 2.6.0.
- [x] **Headline: NLLB beats closed-text ms8 on 384/392 book-rows; 0 wins in 320 OT rows; the only 8 wins are Goofa NT (the Ometo anomaly).** The current closed-text method does not replace NLLB for OT drafting.

## Pending / awaiting David

- [ ] Pick winning synoptic models to publish; `hf_export`/`publish` (correct source metadata) under cc-by-sa-4.0.
- [ ] 3090 driver reboot (local training/verification only; not blocking the cluster work).
- [ ] Ethiopic Gofa NT asymmetry (+14–16, Gamo only +2–4) — real under clean methodology; discuss/writeup (Ometo-cluster centrality hypothesis).

## Cross-repo follow-ups

- [ ] Add the validation-bias note to the `DavidCBaines/ebible_m2m-ms8-ie-shareable` HF model card (authorized 2026-07-25).
- [ ] `bible-mt-family-transfer` v2: rebuild on `synoptic` (v1 renamed to `bible-mt-family-transfer-v1`, kept for its data-prep artifacts + code-review-findings doc; it never ran on H100). v2 pins `synoptic` instead of vendoring, and adds its own `scripts/sota.py` building SotaSpecs from its configs (`synoptic.sota` needs no change).
