# todo — same-script multi-source series v2

Consult `spec.md` before every change. Mark tasks `[x]` as they complete.
v1 history and scores: `experiments/v1-reference/`.

## 1. Repo on the synoptic toolkit

- [x] pyproject: synoptic as pinned git dependency (+ local path override for dev); train stack as plain dependencies (agents install them)
- [x] Carry over: selections, source-ranking.csv, holdout YAMLs, Genesis-250 list, v1 scores as reference
- [x] Scripts adapted: pools.py (POOLS + CLI), make_configs.py (validation section, companion_ranking), rank_sources.py
- [x] Regenerate the 22 experiment YAMLs; verify each loads and resolves
- [x] Repo tests pass (configs load, pools match selections; regeneration reproduces committed files)
- [x] Code review (both repos) passes with no findings (3 rounds on synoptic, 2 on this repo; 2026-07-26)
- [x] Push synoptic public (tags v0.1.0-v0.1.5 as remote-bootstrap layers were fixed); push this repo. PENDING: old-repo deletion needs `gh auth refresh -h github.com -s delete_repo`, then rename v2-staging -> bible-mt-same-script

## 2. Pilot (gate before the fleet)

- [x] Smoke run end-to-end on cheetah (3090 blocked on driver reboot): validation set active, all test sets scored, chunked weights round-tripped, model loads and generates
- [x] First full-size pilot (task 1e01dd80): trained + scored; v2 scores slightly above v1 (+0.1-2.0, methodology fixes vindicated) — but 150 MB weight parts failed 4/4 uploads (file-server threshold drifts; MinIO unreachable from the Dallas workers, probe hung)
- [x] Chunked-artifact transport abandoned after three failure patterns (150 MB parts 4/4, 48 MB parts rejected after ~100 MB/task): the file server is unfit for bulk weights
- [ ] Pilot weights attempt on the MinIO store (task d92a100a, synoptic v0.2.1 uploads the run dir to nlp-research/MT/experiments/synoptic/, i.e. ~/M): on completion verify fetch_weights --run + generation, then STOP for David's go
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
