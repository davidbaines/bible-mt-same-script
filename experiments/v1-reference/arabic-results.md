# Results: arabic

chrF3, corpus-level. `copy` = source-copy baseline; `best-other` = strongest copy-another-pool-language baseline; `base` = single-source one-to-many; `ms8` = multi-source K=8; `gain` = ms8 - base. Scores recovered from run console logs (`scripts/fetch_scores.py`); weights were not retained (artifact uploads fail at the file server).

## drafting

Runs: `ms8_arabic_drafting` vs `base_arabic_drafting`.

| translation   | book       |   verses |   copy |   best-other |   base |   ms8 |   gain |
|:--------------|:-----------|---------:|-------:|-------------:|-------:|------:|-------:|
| ckb           | GEN        |     1531 |  14.18 |        14.18 |  27.83 | 32.45 |   4.62 |
| ckb           | MRK        |      678 |  13.19 |        13.19 |  50.48 | 52.32 |   1.84 |
| ckb           | [epistles] |      274 |  12.6  |        12.6  |  35.46 | 35.83 |   0.37 |
| ckb           | [OT]       |    23130 |  13.83 |        13.83 |  25.59 | 31.09 |   5.5  |
| urdoucv       | GEN        |     1531 |  11.96 |        11.96 |  29.63 | 31.89 |   2.26 |
| urdoucv       | MRK        |      678 |  11.17 |        11.48 |  44.54 | 44.4  |  -0.14 |
| urdoucv       | [epistles] |      274 |  12.34 |        12.34 |  32.52 | 32.91 |   0.39 |
| urdoucv       | [OT]       |    23130 |  12.46 |        12.46 |  26.81 | 29.05 |   2.24 |

Easiest / hardest OT books by ms8 chrF3 (books >100 verses):

| translation   | book   |   verses |   base |   ms8 |   gain |
|:--------------|:-------|---------:|-------:|------:|-------:|
| ckb           | 2CH    |      822 |  26.4  | 33.04 |   6.64 |
| ckb           | 1KI    |      816 |  26.19 | 32.63 |   6.44 |
| ckb           | JDG    |      618 |  27.17 | 32.62 |   5.45 |
| ckb           | GEN    |     1531 |  27.83 | 32.45 |   4.62 |
| ckb           | 1SA    |      809 |  27.82 | 32.41 |   4.59 |

| translation   | book   |   verses |   base |   ms8 |   gain |
|:--------------|:-------|---------:|-------:|------:|-------:|
| ckb           | SNG    |      117 |  20.61 | 24.84 |   4.23 |
| urdoucv       | SNG    |      117 |  24.41 | 24.97 |   0.56 |
| urdoucv       | EST    |      167 |  26.5  | 26.42 |  -0.08 |
| urdoucv       | PRO    |      915 |  25.85 | 26.85 |   1    |
| urdoucv       | NUM    |     1288 |  24.93 | 27.2  |   2.27 |

## gap-filling

Runs: `ms8_arabic_gapfill` vs `base_arabic_gapfill`.

| translation   | book       |   verses |   copy |   best-other |   base |   ms8 |   gain |
|:--------------|:-----------|---------:|-------:|-------------:|-------:|------:|-------:|
| ckb           | GEN        |      250 |  14.37 |        14.37 |  48.04 | 49.77 |   1.73 |
| ckb           | MRK        |      678 |  13.19 |        13.19 |  53.21 | 55.33 |   2.12 |
| ckb           | [epistles] |      274 |  12.6  |        12.6  |  38.88 | 39.44 |   0.56 |
| urdoucv       | GEN        |      250 |  11.85 |        11.85 |  45.76 | 45.93 |   0.17 |
| urdoucv       | MRK        |      678 |  11.17 |        11.48 |  45.73 | 47.31 |   1.58 |
| urdoucv       | [epistles] |      274 |  12.34 |        12.34 |  35.53 | 36.35 |   0.82 |
