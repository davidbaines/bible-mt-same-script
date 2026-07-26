# Results: ethiopic

chrF3, corpus-level. `copy` = source-copy baseline; `best-other` = strongest copy-another-pool-language baseline; `base` = single-source one-to-many; `ms8` = multi-source K=8; `gain` = ms8 - base. Scores recovered from run console logs (`scripts/fetch_scores.py`); weights were not retained (artifact uploads fail at the file server).

## drafting, target gmv

Runs: `ms8_ethiopic_drafting_gmv` vs `base_ethiopic_drafting_gmv`.

| translation   | book       |   verses |   copy |   best-other |   base |   ms8 |   gain |
|:--------------|:-----------|---------:|-------:|-------------:|-------:|------:|-------:|
| gmve          | GEN        |     1511 |  14.44 |        14.44 |  21.23 | 22.71 |   1.48 |
| gmve          | MRK        |      673 |  10.9  |        10.9  |  31.93 | 31.52 |  -0.41 |
| gmve          | [epistles] |      271 |  10.84 |        10.84 |  21.85 | 23.45 |   1.6  |
| gmve          | [OT]       |    23060 |  13.54 |        13.54 |  17.51 | 18.82 |   1.31 |

Easiest / hardest OT books by ms8 chrF3 (books >100 verses):

| translation   | book   |   verses |   base |   ms8 |   gain |
|:--------------|:-------|---------:|-------:|------:|-------:|
| gmve          | GEN    |     1511 |  21.23 | 22.71 |   1.48 |
| gmve          | PSA    |     2458 |  19.74 | 22.01 |   2.27 |
| gmve          | ZEC    |      211 |  19    | 20.75 |   1.75 |
| gmve          | JDG    |      617 |  18.91 | 20.21 |   1.3  |
| gmve          | EXO    |     1208 |  18.39 | 19.88 |   1.49 |

| translation   | book   |   verses |   base |   ms8 |   gain |
|:--------------|:-------|---------:|-------:|------:|-------:|
| gmve          | NEH    |      401 |  13.86 | 15.26 |   1.4  |
| gmve          | EZR    |      271 |  15.03 | 15.58 |   0.55 |
| gmve          | SNG    |      117 |  15.72 | 16.38 |   0.66 |
| gmve          | 1CH    |      939 |  15.5  | 16.56 |   1.06 |
| gmve          | JOB    |     1068 |  15.43 | 16.6  |   1.17 |

## drafting, target gof

Runs: `ms8_ethiopic_drafting_gof` vs `base_ethiopic_drafting_gof`.

| translation   | book       |   verses |   copy |   best-other |   base |   ms8 |   gain |
|:--------------|:-----------|---------:|-------:|-------------:|-------:|------:|-------:|
| gofe          | GEN        |     1524 |  14.84 |        14.84 |  21.04 | 23.13 |   2.09 |
| gofe          | MRK        |      673 |  10.6  |        14.28 |  35.36 | 55    |  19.64 |
| gofe          | [epistles] |      271 |  12.14 |        14.95 |  25.21 | 44.72 |  19.51 |
| gofe          | [OT]       |    23042 |  14.37 |        14.37 |  17.83 | 19.79 |   1.96 |

Easiest / hardest OT books by ms8 chrF3 (books >100 verses):

| translation   | book   |   verses |   base |   ms8 |   gain |
|:--------------|:-------|---------:|-------:|------:|-------:|
| gofe          | GEN    |     1524 |  21.04 | 23.13 |   2.09 |
| gofe          | JDG    |      618 |  20.54 | 22.75 |   2.21 |
| gofe          | PSA    |     2457 |  19.1  | 22.36 |   3.26 |
| gofe          | 2CH    |      821 |  19.13 | 22.24 |   3.11 |
| gofe          | ZEC    |      211 |  19.92 | 22.11 |   2.19 |

| translation   | book   |   verses |   base |   ms8 |   gain |
|:--------------|:-------|---------:|-------:|------:|-------:|
| gofe          | SNG    |      117 |  14.04 | 16.01 |   1.97 |
| gofe          | NEH    |      403 |  15.03 | 16.06 |   1.03 |
| gofe          | MIC    |      105 |  14.94 | 16.51 |   1.57 |
| gofe          | ECC    |      222 |  15.44 | 16.99 |   1.55 |
| gofe          | EST    |      167 |  16.12 | 17.21 |   1.09 |

## gap-filling, target gmv

Runs: `ms8_ethiopic_gapfill_gmv` vs `base_ethiopic_gapfill_gmv`.

| translation   | book       |   verses |   copy |   best-other |   base |   ms8 |   gain |
|:--------------|:-----------|---------:|-------:|-------------:|-------:|------:|-------:|
| gmve          | GEN        |      249 |  14.51 |        14.51 |  42.7  | 45.76 |   3.06 |
| gmve          | MRK        |      673 |  10.9  |        10.9  |  35.83 | 36.81 |   0.98 |
| gmve          | [epistles] |      271 |  10.84 |        10.84 |  27.08 | 29.23 |   2.15 |

## gap-filling, target gof

Runs: `ms8_ethiopic_gapfill_gof` vs `base_ethiopic_gapfill_gof`.

| translation   | book       |   verses |   copy |   best-other |   base |   ms8 |   gain |
|:--------------|:-----------|---------:|-------:|-------------:|-------:|------:|-------:|
| gofe          | GEN        |      249 |  14.99 |        14.99 |  45.19 | 47.7  |   2.51 |
| gofe          | MRK        |      673 |  10.6  |        14.28 |  43.04 | 61.52 |  18.48 |
| gofe          | [epistles] |      271 |  12.14 |        14.95 |  34.12 | 52.4  |  18.28 |
