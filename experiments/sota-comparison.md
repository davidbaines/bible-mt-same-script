# SOTA comparison: synoptic (closed-text) vs NLLB-1.3B

Contender = synoptic **ms8** (from-scratch, multi-source K=8, eBible only). SOTA = **facebook/nllb-200-distilled-1.3B** fine-tuned by silnlp on the *same* source→target parallel data and scored on the *same* test verses, per book. chrF3 is sacrebleu `char_order=6, word_order=0, beta=3` for both (byte-identical across sacrebleu 2.4.3/2.6.0). `Δ = ms8 − nllb`; verdict tie when `|Δ| < 1`. `copy` = source-copy floor; `base` = synoptic single-source. NLLB checkpoint = final step (load_best_model_at_end); `arabic_drafting_ckb` scored locally (its silnlp scoring step emitted no CSV) — metric verified to reproduce silnlp to 0.00.

**Verse counts** `verses_syn` vs `verses_nllb` are identical for 364 of 392 book-rows; the 28 that differ do so by ≤4 verses (NLLB keeps a verse when present in source+target, synoptic ms8 also requires source-side coverage across its fusion set). At corpus level these ≤4-verse differences do not move chrF3, so the per-book numbers compare directly.

## Headline

**The closed-text method does not beat NLLB-1.3B, and cannot replace it in
production for the drafting use case.** Across all 392 per-book comparisons,
synoptic ms8 wins **8**, ties **0**, loses **384**.

- **Old Testament — the production goal: 0 wins in 320 book-rows.** ms8 never
  beats NLLB on a single OT book, in any language, under either whole-OT
  drafting or Genesis-250 gap-filling. Typical margins are −8 to −16 chrF3
  (worst on Latin-Bantu drafting, −20 to −23). NLLB's pretraining advantage far
  exceeds the multi-source fusion gain (ms8 over base is real, ~+2 to +4
  drafting, but base and ms8 both sit well below NLLB).
- **New Testament: 8 wins, all Goofa (`gofe`).** The only place the closed-text
  method beats NLLB is Goofa Mark + epistles (+8.6 to +16.7 chrF3), under both
  drafting and gap-filling — the known Ometo-cluster anomaly. Every other NT
  book, including its sibling Gamo (`gmve`), loses to NLLB. And even for Goofa,
  NLLB still wins the OT decisively (Genesis −22 drafting, −9 gap-fill), so the
  win does not extend to the OT-drafting task.

Read plainly: fine-tuning a strong pretrained model on the same closed data is
the better production choice today. The from-scratch line's value is where a
pretrained model is unavailable or the target is genuinely out-of-distribution
(the Goofa signal), not as a general NLLB replacement.

## arabic_drafting_urd  (target `urdoucv`)

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| MRK    |          678 |           678 |  11.17 |  43.63 | 44.77 |  62.52 |  -17.75 | lose      |
| JAS    |          108 |           108 |  12.42 |  33.63 | 35.69 |  53.79 |  -18.1  | lose      |
| 1PE    |          105 |           105 |  12.32 |  31.71 | 34.18 |  50.5  |  -16.32 | lose      |
| 2PE    |           61 |            61 |  12.26 |  29.74 | 33.21 |  48.82 |  -15.61 | lose      |
| GEN    |         1533 |          1531 |  11.95 |  28.53 | 31.48 |  46.21 |  -14.73 | lose      |

OT books (n=39): beat/tie/lose = **0/0/39**, mean Δ = **-12.2** chrF3 (ms8 mean 28.5 vs NLLB 40.7). Best OT for ms8:

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| MAL    |           55 |            55 |  12.45 |  25.54 | 28.77 |  37.49 |   -8.72 | lose      |
| JOB    |         1070 |          1068 |  11    |  24.8  | 27.04 |  36.91 |   -9.87 | lose      |
| EST    |          167 |           167 |  13.63 |  25.17 | 27.87 |  38.11 |  -10.24 | lose      |
| ECC    |          222 |           222 |  12.11 |  24.45 | 28.02 |  38.46 |  -10.44 | lose      |
| DAN    |          357 |           356 |  13.34 |  25.97 | 29.5  |  40.02 |  -10.52 | lose      |

## arabic_drafting_ckb  (target `ckb`)

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| MRK    |          678 |           678 |  13.19 |  49.6  | 52.69 |  70.07 |  -17.38 | lose      |
| JAS    |          108 |           108 |  12.6  |  33.89 | 37.41 |  55.13 |  -17.72 | lose      |
| 1PE    |          105 |           105 |  12.65 |  35.75 | 37.75 |  54.87 |  -17.12 | lose      |
| 2PE    |           61 |            61 |  12.54 |  34.22 | 36.46 |  52.28 |  -15.82 | lose      |
| GEN    |         1533 |          1531 |  14.17 |  27.96 | 31.56 |  48.44 |  -16.88 | lose      |

OT books (n=39): beat/tie/lose = **0/0/39**, mean Δ = **-16.3** chrF3 (ms8 mean 30.0 vs NLLB 46.3). Best OT for ms8:

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| JOB    |         1070 |          1068 |  11.86 |  25.21 | 27.03 |  38.21 |  -11.18 | lose      |
| ECC    |          222 |           222 |  12.65 |  27.31 | 29.7  |  41.13 |  -11.43 | lose      |
| OBA    |           21 |            21 |  12.93 |  24.7  | 28.21 |  41.1  |  -12.89 | lose      |
| HAB    |           56 |            56 |  12.79 |  28.52 | 29.73 |  42.74 |  -13.01 | lose      |
| HOS    |          197 |           197 |  14.06 |  27.81 | 31.27 |  44.56 |  -13.29 | lose      |

## arabic_gapfill_urd  (target `urdoucv`)

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| GEN    |          250 |           250 |  11.85 |  44.88 | 46.44 |  56.63 |  -10.19 | lose      |
| MRK    |          678 |           678 |  11.17 |  45.39 | 46.41 |  61.54 |  -15.13 | lose      |
| JAS    |          108 |           108 |  12.42 |  36.89 | 39.08 |  53.92 |  -14.84 | lose      |
| 1PE    |          105 |           105 |  12.32 |  34.2  | 37.52 |  50.34 |  -12.82 | lose      |
| 2PE    |           61 |            61 |  12.26 |  34.81 | 36.98 |  49.16 |  -12.18 | lose      |

## arabic_gapfill_ckb  (target `ckb`)

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| GEN    |          250 |           250 |  14.37 |  48.32 | 51.29 |  60.48 |   -9.19 | lose      |
| MRK    |          678 |           678 |  13.19 |  54.09 | 56.16 |  70    |  -13.84 | lose      |
| JAS    |          108 |           108 |  12.6  |  38.56 | 42.14 |  56.1  |  -13.96 | lose      |
| 1PE    |          105 |           105 |  12.65 |  40.26 | 42.72 |  55.66 |  -12.94 | lose      |
| 2PE    |           61 |            61 |  12.54 |  39.21 | 39.49 |  51.63 |  -12.14 | lose      |

## devanagari_drafting_hne  (target `hne`)

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| MRK    |          678 |           678 |  19.83 |  58.27 | 57.47 |  68.12 |  -10.65 | lose      |
| JAS    |          108 |           108 |  20.54 |  47.13 | 47.15 |  54.61 |   -7.46 | lose      |
| 1PE    |          105 |           105 |  21.58 |  43.08 | 44.46 |  53.04 |   -8.58 | lose      |
| 2PE    |           61 |            61 |  19.22 |  42.12 | 42.48 |  52.99 |  -10.51 | lose      |
| GEN    |         1533 |          1533 |  23.53 |  38.95 | 40.25 |  52.04 |  -11.79 | lose      |

OT books (n=39): beat/tie/lose = **0/0/39**, mean Δ = **-12.7** chrF3 (ms8 mean 33.5 vs NLLB 46.2). Best OT for ms8:

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| JON    |           48 |            48 |  23.69 |  38.08 | 38.99 |  45.35 |   -6.36 | lose      |
| JOB    |         1070 |          1070 |  17.24 |  31.54 | 32.04 |  40.06 |   -8.02 | lose      |
| ECC    |          222 |           222 |  18.15 |  31.55 | 31.29 |  39.84 |   -8.55 | lose      |
| NAM    |           47 |            47 |  18.31 |  27.73 | 28.61 |  37.23 |   -8.62 | lose      |
| PRO    |          915 |           915 |  18.42 |  32.78 | 33.15 |  42.17 |   -9.02 | lose      |

## devanagari_drafting_mar  (target `mar`)

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| MRK    |          673 |           673 |  14.92 |  45.4  | 44.54 |  55.66 |  -11.12 | lose      |
| JAS    |          108 |           108 |  17.3  |  33.38 | 33.24 |  48.39 |  -15.15 | lose      |
| 1PE    |          103 |           103 |  17.66 |  34.94 | 35.72 |  51.18 |  -15.46 | lose      |
| 2PE    |           61 |            61 |  16.48 |  34.18 | 31.65 |  47.91 |  -16.26 | lose      |
| GEN    |         1532 |          1532 |  16.49 |  30    | 29.34 |  45.67 |  -16.33 | lose      |

OT books (n=39): beat/tie/lose = **0/0/39**, mean Δ = **-15.1** chrF3 (ms8 mean 26.2 vs NLLB 41.3). Best OT for ms8:

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| JOB    |         1070 |          1070 |  13.25 |  23.65 | 22.86 |  30.74 |   -7.88 | lose      |
| ECC    |          222 |           222 |  14.65 |  25.14 | 24.59 |  34.99 |  -10.4  | lose      |
| HAB    |           56 |            56 |  15.68 |  26.25 | 24.98 |  36.75 |  -11.77 | lose      |
| NAM    |           47 |            47 |  14.28 |  23.6  | 23.26 |  35.09 |  -11.83 | lose      |
| 2SA    |          695 |           695 |  16.61 |  24.7  | 24.31 |  36.32 |  -12.01 | lose      |

## devanagari_gapfill_hne  (target `hne`)

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| GEN    |          250 |           250 |  23.64 |  53.85 | 53.79 |  61.54 |   -7.75 | lose      |
| MRK    |          678 |           678 |  19.83 |  57.64 | 57.65 |  68.24 |  -10.59 | lose      |
| JAS    |          108 |           108 |  20.54 |  47.24 | 51.17 |  55.42 |   -4.25 | lose      |
| 1PE    |          105 |           105 |  21.58 |  43.68 | 45.57 |  55.25 |   -9.68 | lose      |
| 2PE    |           61 |            61 |  19.22 |  42.27 | 44.66 |  53.78 |   -9.12 | lose      |

## devanagari_gapfill_mar  (target `mar`)

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| GEN    |          250 |           250 |  16.88 |  39.73 | 39.95 |  50.92 |  -10.97 | lose      |
| MRK    |          673 |           673 |  14.92 |  45.78 | 47.06 |  56.19 |   -9.13 | lose      |
| JAS    |          108 |           108 |  17.3  |  35.84 | 37.79 |  48.65 |  -10.86 | lose      |
| 1PE    |          103 |           103 |  17.66 |  36.05 | 38.64 |  51.92 |  -13.28 | lose      |
| 2PE    |           61 |            61 |  16.48 |  34.72 | 36.07 |  47.95 |  -11.88 | lose      |

## ethiopic_drafting_gmv  (target `gmve`)

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| MRK    |          673 |           669 |  10.9  |  30.75 | 34.52 |  39.93 |   -5.41 | lose      |
| JAS    |          105 |           104 |  10.78 |  20.96 | 25.41 |  33.8  |   -8.39 | lose      |
| 1PE    |          105 |           103 |  10.6  |  22.5  | 26.62 |  33.31 |   -6.69 | lose      |
| 2PE    |           61 |            61 |  11.31 |  19.54 | 24.2  |  28.5  |   -4.3  | lose      |
| GEN    |         1510 |          1510 |  14.44 |  21.6  | 23.72 |  42.19 |  -18.47 | lose      |

OT books (n=39): beat/tie/lose = **0/0/39**, mean Δ = **-13.0** chrF3 (ms8 mean 18.9 vs NLLB 31.9). Best OT for ms8:

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| JOB    |         1066 |          1066 |  11.61 |  15.48 | 17.3  |  26.23 |   -8.93 | lose      |
| NUM    |         1207 |          1207 |  11.67 |  16.51 | 17.58 |  26.87 |   -9.29 | lose      |
| OBA    |           21 |            21 |  11.89 |  13.89 | 16.24 |  25.64 |   -9.4  | lose      |
| HAB    |           56 |            56 |  11.43 |  14.14 | 15.71 |  25.18 |   -9.47 | lose      |
| LEV    |          854 |           854 |  11.97 |  16.59 | 17.19 |  26.75 |   -9.56 | lose      |

## ethiopic_drafting_gof  (target `gofe`)

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| MRK    |          673 |           669 |  10.6  |  40.07 | 54.61 |  39.98 |   14.63 | beat      |
| JAS    |          107 |           104 |  11.56 |  26.62 | 44.1  |  34.55 |    9.55 | beat      |
| 1PE    |          103 |           103 |  12.09 |  28.09 | 45.16 |  34.97 |   10.19 | beat      |
| 2PE    |           61 |            61 |  13.06 |  25.87 | 40.3  |  31.71 |    8.59 | beat      |
| GEN    |         1510 |          1510 |  14.94 |  18.83 | 22.93 |  44.89 |  -21.96 | lose      |

OT books (n=39): beat/tie/lose = **0/0/39**, mean Δ = **-15.8** chrF3 (ms8 mean 18.4 vs NLLB 34.2). Best OT for ms8:

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| MIC    |          105 |           105 |  11.42 |  13.83 | 16.01 |  26.09 |  -10.08 | lose      |
| OBA    |           21 |            21 |  12.04 |  14.32 | 14.56 |  25.34 |  -10.78 | lose      |
| HAB    |           56 |            56 |  11.8  |  12.14 | 13.68 |  24.55 |  -10.87 | lose      |
| LEV    |          854 |           854 |  13.34 |  15.39 | 17.2  |  28.98 |  -11.78 | lose      |
| JOL    |           72 |            72 |  13.17 |  17.83 | 18.37 |  30.27 |  -11.9  | lose      |

## ethiopic_gapfill_gmv  (target `gmve`)

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| GEN    |          249 |           249 |  14.51 |  40.61 | 46.37 |  56.15 |   -9.78 | lose      |
| MRK    |          673 |           669 |  10.9  |  33.29 | 36.15 |  40.43 |   -4.28 | lose      |
| JAS    |          105 |           104 |  10.78 |  27.5  | 30.27 |  35.1  |   -4.83 | lose      |
| 1PE    |          105 |           103 |  10.6  |  25.98 | 30.81 |  33.72 |   -2.91 | lose      |
| 2PE    |           61 |            61 |  11.31 |  24.92 | 28.89 |  30.8  |   -1.91 | lose      |

## ethiopic_gapfill_gof  (target `gofe`)

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| GEN    |          249 |           249 |  14.99 |  42.92 | 47.71 |  56.91 |   -9.2  | lose      |
| MRK    |          673 |           669 |  10.6  |  41.34 | 57.38 |  40.65 |   16.73 | beat      |
| JAS    |          107 |           104 |  11.56 |  32.63 | 50.51 |  37.1  |   13.41 | beat      |
| 1PE    |          103 |           103 |  12.09 |  33    | 48.28 |  37.2  |   11.08 | beat      |
| 2PE    |           61 |            61 |  13.06 |  29.7  | 45.7  |  34.25 |   11.45 | beat      |

## latin_bantu_drafting_nde  (target `nde`)

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| MRK    |          678 |           678 |  18.37 |  55.39 | 56.51 |  70.3  |  -13.79 | lose      |
| JAS    |          108 |           108 |  17.18 |  40.78 | 41.64 |  64.39 |  -22.75 | lose      |
| 1PE    |          105 |           105 |  17.34 |  44.82 | 43.83 |  65.82 |  -21.99 | lose      |
| 2PE    |           61 |            61 |  18.44 |  43.1  | 43.48 |  62.03 |  -18.55 | lose      |
| GEN    |         1533 |          1533 |  19.84 |  36.79 | 37.54 |  62.27 |  -24.73 | lose      |

OT books (n=39): beat/tie/lose = **0/0/39**, mean Δ = **-23.1** chrF3 (ms8 mean 34.4 vs NLLB 57.5). Best OT for ms8:

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| JOB    |         1070 |          1070 |  16.46 |  32.36 | 32.94 |  50.9  |  -17.96 | lose      |
| HAB    |           56 |            56 |  18.14 |  30.77 | 32.51 |  51.25 |  -18.74 | lose      |
| PRO    |          915 |           915 |  16.01 |  32.38 | 32.66 |  51.63 |  -18.97 | lose      |
| LAM    |          154 |           154 |  16.9  |  30.95 | 31.72 |  51.01 |  -19.29 | lose      |
| JON    |           48 |            48 |  17.72 |  33.37 | 36.51 |  56.03 |  -19.52 | lose      |

## latin_bantu_drafting_nya  (target `nya`)

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| MRK    |          678 |           678 |  22.68 |  57.42 | 58.91 |  69.86 |  -10.95 | lose      |
| JAS    |          108 |           108 |  20.09 |  42.67 | 45.64 |  60.04 |  -14.4  | lose      |
| 1PE    |          105 |           105 |  20.67 |  44.4  | 46.54 |  62.43 |  -15.89 | lose      |
| 2PE    |           61 |            61 |  21.76 |  43.9  | 46.35 |  62.14 |  -15.79 | lose      |
| GEN    |         1533 |          1533 |  24.45 |  37.35 | 39.75 |  59.48 |  -19.73 | lose      |

OT books (n=39): beat/tie/lose = **0/0/39**, mean Δ = **-20.6** chrF3 (ms8 mean 36.9 vs NLLB 57.6). Best OT for ms8:

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| JOB    |         1070 |          1070 |  19.73 |  33.12 | 34.63 |  49.6  |  -14.97 | lose      |
| PRO    |          915 |           915 |  19.03 |  32.15 | 33.67 |  49.27 |  -15.6  | lose      |
| ISA    |         1291 |          1291 |  21.29 |  32.36 | 36.04 |  52.85 |  -16.81 | lose      |
| EZK    |         1273 |          1273 |  22.01 |  31.23 | 35.3  |  52.71 |  -17.41 | lose      |
| HAB    |           56 |            56 |  21.2  |  33.8  | 35.34 |  53.33 |  -17.99 | lose      |

## latin_bantu_gapfill_nde  (target `nde`)

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| GEN    |          250 |           250 |  20.05 |  58.82 | 57.82 |  68.95 |  -11.13 | lose      |
| MRK    |          678 |           678 |  18.37 |  59.79 | 59.77 |  70.4  |  -10.63 | lose      |
| JAS    |          108 |           108 |  17.18 |  49.91 | 50.73 |  65.19 |  -14.46 | lose      |
| 1PE    |          105 |           105 |  17.34 |  51.44 | 52.73 |  66.65 |  -13.92 | lose      |
| 2PE    |           61 |            61 |  18.44 |  49.16 | 51.36 |  62.93 |  -11.57 | lose      |

## latin_bantu_gapfill_nya  (target `nya`)

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| GEN    |          250 |           250 |  24.7  |  54.55 | 54.29 |  65.1  |  -10.81 | lose      |
| MRK    |          678 |           678 |  22.68 |  62.02 | 62.59 |  70.64 |   -8.05 | lose      |
| JAS    |          108 |           108 |  20.09 |  49.39 | 51.32 |  62.72 |  -11.4  | lose      |
| 1PE    |          105 |           105 |  20.67 |  50.49 | 51.84 |  62.71 |  -10.87 | lose      |
| 2PE    |           61 |            61 |  21.76 |  48.6  | 50.76 |  63.26 |  -12.5  | lose      |

## telugu_nt-only_nit  (target `nit`)

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| MRK    |          672 |           670 |  14.59 |  27.99 | 28.99 |  37.86 |   -8.87 | lose      |
| JAS    |          108 |           108 |  18.19 |  27.8  | 28.23 |  43.15 |  -14.92 | lose      |
| 1PE    |          105 |           105 |  16.56 |  28.55 | 28.71 |  41.46 |  -12.75 | lose      |
| 2PE    |           60 |            60 |  18.01 |  27.76 | 26.89 |  40.72 |  -13.83 | lose      |

## telugu_nt-only_vgr  (target `vgr`)

| book   |   verses_syn |   verses_nllb |   copy |   base |   ms8 |   nllb |   delta | verdict   |
|:-------|-------------:|--------------:|-------:|-------:|------:|-------:|--------:|:----------|
| MRK    |          678 |           676 |  15.67 |  24.57 | 25.84 |  36.21 |  -10.37 | lose      |
| JAS    |          108 |           108 |  17.82 |  23.91 | 22.83 |  38.11 |  -15.28 | lose      |
| 1PE    |          105 |           105 |  19.01 |  23.39 | 23.16 |  36.97 |  -13.81 | lose      |
| 2PE    |           61 |            61 |  18.13 |  22.61 | 19.38 |  33.88 |  -14.5  | lose      |

## Totals (per book, excluding the ALL row)

- beat/tie/lose across all 392 book-rows: **8/0/384**
- OT-only: **0/0/320**
- NT-only (MRK + epistles): **8/0/64**
