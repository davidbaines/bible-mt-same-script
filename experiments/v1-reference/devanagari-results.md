# Results: devanagari

chrF3, corpus-level. `copy` = source-copy baseline; `best-other` = strongest copy-another-pool-language baseline; `base` = single-source one-to-many; `ms8` = multi-source K=8; `gain` = ms8 - base. Scores recovered from run console logs (`scripts/fetch_scores.py`); weights were not retained (artifact uploads fail at the file server).

## drafting

Runs: `ms8_devanagari_drafting` vs `base_devanagari_drafting`.

| translation   | book       |   verses |   copy |   best-other |   base |   ms8 |   gain |
|:--------------|:-----------|---------:|-------:|-------------:|-------:|------:|-------:|
| hne           | GEN        |     1533 |  23.53 |        23.53 |  39.32 | 40.5  |   1.18 |
| hne           | MRK        |      678 |  19.83 |        20.29 |  58.02 | 58.24 |   0.22 |
| hne           | [epistles] |      274 |  20.63 |        20.65 |  43.51 | 44.9  |   1.39 |
| hne           | [OT]       |    23142 |  21.77 |        21.77 |  33.63 | 34.41 |   0.78 |
| mar           | GEN        |     1532 |  16.49 |        16.49 |  29.89 | 30.32 |   0.43 |
| mar           | MRK        |      673 |  14.92 |        14.92 |  45.33 | 45.19 |  -0.14 |
| mar           | [epistles] |      272 |  17.24 |        17.24 |  33.53 | 34.13 |   0.6  |
| mar           | [OT]       |    23140 |  16.79 |        16.79 |  27.08 | 27.41 |   0.33 |

Easiest / hardest OT books by ms8 chrF3 (books >100 verses):

| translation   | book   |   verses |   base |   ms8 |   gain |
|:--------------|:-------|---------:|-------:|------:|-------:|
| hne           | GEN    |     1533 |  39.32 | 40.5  |   1.18 |
| hne           | 1SA    |      810 |  36.5  | 37.88 |   1.38 |
| hne           | 2KI    |      719 |  34.16 | 35.76 |   1.6  |
| hne           | 1KI    |      816 |  34.46 | 35.73 |   1.27 |
| hne           | 2SA    |      695 |  33.85 | 35.3  |   1.45 |

| translation   | book   |   verses |   base |   ms8 |   gain |
|:--------------|:-------|---------:|-------:|------:|-------:|
| mar           | JOB    |     1070 |  23.23 | 23.29 |   0.06 |
| mar           | PRO    |      915 |  25    | 24.76 |  -0.24 |
| mar           | NEH    |      405 |  24.98 | 25    |   0.02 |
| mar           | ECC    |      222 |  24.54 | 25.21 |   0.67 |
| mar           | 2SA    |      695 |  25.42 | 25.4  |  -0.02 |

## gap-filling

Runs: `ms8_devanagari_gapfill` vs `base_devanagari_gapfill`.

| translation   | book       |   verses |   copy |   best-other |   base |   ms8 |   gain |
|:--------------|:-----------|---------:|-------:|-------------:|-------:|------:|-------:|
| hne           | GEN        |      250 |  23.64 |        23.64 |  53.41 | 53.1  |  -0.31 |
| hne           | MRK        |      678 |  19.83 |        20.29 |  58.41 | 57.95 |  -0.46 |
| hne           | [epistles] |      274 |  20.63 |        20.65 |  44.93 | 46.42 |   1.49 |
| mar           | GEN        |      250 |  16.88 |        16.88 |  40.94 | 40.35 |  -0.59 |
| mar           | MRK        |      673 |  14.92 |        14.92 |  46.16 | 46.37 |   0.21 |
| mar           | [epistles] |      272 |  17.24 |        17.24 |  36.14 | 37.31 |   1.17 |
