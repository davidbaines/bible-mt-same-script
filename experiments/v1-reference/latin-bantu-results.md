# Results: latin-bantu

chrF3, corpus-level. `copy` = source-copy baseline; `best-other` = strongest copy-another-pool-language baseline; `base` = single-source one-to-many; `ms8` = multi-source K=8; `gain` = ms8 - base. Scores recovered from run console logs (`scripts/fetch_scores.py`); weights were not retained (artifact uploads fail at the file server).

## drafting

Runs: `ms8_latin_bantu_drafting` vs `base_latin_bantu_drafting`.

| translation   | book       |   verses |   copy |   best-other |   base |   ms8 |   gain |
|:--------------|:-----------|---------:|-------:|-------------:|-------:|------:|-------:|
| nde           | GEN        |     1533 |  19.84 |        20.51 |  38.4  | 37.76 |  -0.64 |
| nde           | MRK        |      678 |  18.37 |        19.79 |  56.15 | 56.05 |  -0.1  |
| nde           | [epistles] |      274 |  17.55 |        20.03 |  43.72 | 44.62 |   0.9  |
| nde           | [OT]       |    23142 |  18.79 |        20.44 |  35.08 | 35.11 |   0.03 |
| nya           | GEN        |     1533 |  24.45 |        24.45 |  38.96 | 39.66 |   0.7  |
| nya           | MRK        |      678 |  22.68 |        22.68 |  57.67 | 58.57 |   0.9  |
| nya           | [epistles] |      274 |  20.73 |        20.73 |  44.17 | 46.4  |   2.23 |
| nya           | [OT]       |    23142 |  22.8  |        22.8  |  36.19 | 37.21 |   1.02 |

Easiest / hardest OT books by ms8 chrF3 (books >100 verses):

| translation   | book   |   verses |   base |   ms8 |   gain |
|:--------------|:-------|---------:|-------:|------:|-------:|
| nya           | ZEC    |      211 |  40.16 | 41.82 |   1.66 |
| nya           | PSA    |     2460 |  39.96 | 40.86 |   0.9  |
| nya           | DEU    |      959 |  37.94 | 39.71 |   1.77 |
| nya           | GEN    |     1533 |  38.96 | 39.66 |   0.7  |
| nya           | MIC    |      105 |  38.2  | 39.31 |   1.11 |

| translation   | book   |   verses |   base |   ms8 |   gain |
|:--------------|:-------|---------:|-------:|------:|-------:|
| nde           | EST    |      167 |  29.45 | 28.71 |  -0.74 |
| nde           | SNG    |      117 |  29.91 | 29.16 |  -0.75 |
| nya           | EST    |      167 |  33.58 | 32.73 |  -0.85 |
| nde           | LAM    |      154 |  33.68 | 32.81 |  -0.87 |
| nde           | DAN    |      357 |  33.43 | 33.17 |  -0.26 |

## gap-filling

Runs: `ms8_latin_bantu_gapfill` vs `base_latin_bantu_gapfill`.

| translation   | book       |   verses |   copy |   best-other |   base |   ms8 |   gain |
|:--------------|:-----------|---------:|-------:|-------------:|-------:|------:|-------:|
| nde           | GEN        |      250 |  20.05 |        20.42 |  58.82 | 56.95 |  -1.87 |
| nde           | MRK        |      678 |  18.37 |        19.79 |  59.79 | 59.64 |  -0.15 |
| nde           | [epistles] |      274 |  17.55 |        20.03 |  50.33 | 51.04 |   0.71 |
| nya           | GEN        |      250 |  24.7  |        24.7  |  54.55 | 53.78 |  -0.77 |
| nya           | MRK        |      678 |  22.68 |        22.68 |  62.02 | 62.2  |   0.18 |
| nya           | [epistles] |      274 |  20.73 |        20.73 |  49.63 | 50.33 |   0.7  |
