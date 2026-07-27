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
- [x] Weights transport proven end-to-end (synoptic v0.2.3): a worker uploads the run dir to the MinIO store (~/M/MT/experiments/synoptic/<repo>/<run>/), fetch_weights --run downloads it, model loads and generates. Diagnosis chain: ClearML file-server drops bulk uploads (any chunk size) -> switched to the MinIO store silnlp uses -> agents inject the store as a bare IP the hostname-only cert rejects, and the hostname doesn't resolve on workers -> --add-host maps hostname->IP (resolved at enqueue) so it connects by the cert-valid hostname to the routable IP, full TLS
- [x] Transport code reviewed (the advisor caught that v0.1.1-v0.2.3 + the v0.3.0 store rewrite were post-review): 2 reviewers on the transport diff + 1 on store.py; all findings fixed (partial-upload-looks-complete closed via manifest+verify; preflight; prefix-clear; enqueue hard-fail; overfit upload gate). synoptic v0.3.1.
- [ ] GATE (David's instruction): real full-size round-trip — ms8_arabic_drafting on v0.3.1 (task 65a03603) RUNNING; on completion verify manifest-guaranteed upload of the ~840 MB model + fetch_weights --run + generate, THEN report gate met

## Awaiting David
- [ ] Go/no-go on the 22-run fleet (held per instruction)
- [ ] Recommended first: single ms8_arabic_drafting re-run on v0.2.3 to bank the first real retained weights (its earlier real run predated the transport fix, so those weights were lost) and prove full-size (~840 MB) download
- [ ] `gh auth refresh -h github.com -s delete_repo`, then delete old bible-mt-same-script + rename v2-staging -> bible-mt-same-script (do BEFORE the fleet: store paths key off the repo name)
- [ ] 3090 driver reboot (local training/verification blocked until then)
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
