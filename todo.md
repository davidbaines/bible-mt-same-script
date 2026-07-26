# todo — same-script multi-source series v2

Consult `spec.md` before every change. Mark tasks `[x]` as they complete.
v1 history and scores: `experiments/v1-reference/`.

## 1. Repo on the synoptic toolkit

- [x] pyproject: synoptic as pinned git dependency (+ local path override for dev); train stack as plain dependencies (agents install them)
- [x] Carry over: selections, source-ranking.csv, holdout YAMLs, Genesis-250 list, v1 scores as reference
- [x] Scripts adapted: pools.py (POOLS + CLI), make_configs.py (validation section, companion_ranking), rank_sources.py
- [ ] Regenerate the 22 experiment YAMLs; verify each loads and resolves
- [ ] Repo tests pass (configs load, pools match selections)
- [ ] Code review (both repos) passes with no findings
- [ ] Push synoptic public + tag v0.1.0; push this repo; delete old bible-mt-same-script

## 2. Pilot (gate before the fleet)

- [ ] 3090 smoke run end-to-end (validation set active, all test sets scored)
- [ ] One real run (ms8_arabic_drafting) on cheetah_94gb: chunked upload works, fetch_weights reassembles, model loads and generates
- [ ] Hold here — David reviews before the full re-run

## 3. Full v2 re-run (22 runs, after the pilot gate)

- [ ] Devanagari 4, Arabic 4, Ethiopic 8, Telugu 2, Latin-Bantu 4 — enqueue under the ≥2-effective-free gate
- [ ] Per run: fetch_scores + fetch_weights; weights archived locally (check free disk ≥ 40 GB first)
- [ ] v2 results docs + series summary with v1-vs-v2 comparison
- [ ] Revisit the Gofa NT anomaly with clean checkpoints

## 4. Publishing and follow-ups

- [ ] David picks winners; hf_export/publish (correct source metadata) under cc-by-sa-4.0
- [ ] Add validation-bias note to DavidCBaines/ebible_m2m-ms8-ie-shareable model card (authorized 2026-07-25)
- [ ] Note in bible-mt-family-transfer: synoptic v0.1.0 exists; re-point and drop the vendored copy
