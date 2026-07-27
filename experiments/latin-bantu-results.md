# v2 results: latin-bantu

chrF3, corpus-level. `copy` = source-copy floor; `base` = single-source; `ms8` = multi-source K=8; `gain` = ms8 - base. Clean methodology (validation set disjoint from train+test).

## Latin-Bantu drafting

`ms8_latin_bantu_drafting` vs `base_latin_bantu_drafting`

| translation   | book       |   verses |   copy |   base |   ms8 |   gain |
|:--------------|:-----------|---------:|-------:|-------:|------:|-------:|
| nde           | GEN        |     1533 |  19.84 |  36.79 | 37.54 |   0.75 |
| nde           | MRK        |      678 |  18.37 |  55.39 | 56.51 |   1.12 |
| nde           | [epistles] |      274 |  17.55 |  42.94 | 42.96 |   0.02 |
| nde           | [OT]       |    23142 |  18.79 |  33.17 | 34.85 |   1.68 |
| nya           | GEN        |     1533 |  24.45 |  37.35 | 39.75 |   2.4  |
| nya           | MRK        |      678 |  22.68 |  57.42 | 58.91 |   1.49 |
| nya           | [epistles] |      274 |  20.73 |  43.65 | 46.17 |   2.52 |
| nya           | [OT]       |    23142 |  22.8  |  34.1  | 37.13 |   3.03 |

Easiest OT books by ms8 chrF3:

| translation   | book   |   verses |   base |   ms8 |   gain |
|:--------------|:-------|---------:|-------:|------:|-------:|
| nya           | ZEC    |      211 |  39.14 | 41.53 |   2.39 |
| nya           | PSA    |     2460 |  37.9  | 40.17 |   2.27 |
| nya           | GEN    |     1533 |  37.35 | 39.75 |   2.4  |
| nya           | 2SA    |      695 |  35.64 | 39.38 |   3.74 |
| nya           | 2CH    |      822 |  35.69 | 39.31 |   3.62 |

## Latin-Bantu gap-filling

`ms8_latin_bantu_gapfill` vs `base_latin_bantu_gapfill`

| translation   | book       |   verses |   copy |   base |   ms8 |   gain |
|:--------------|:-----------|---------:|-------:|-------:|------:|-------:|
| nde           | GEN        |      250 |  20.05 |  58.82 | 57.82 |  -1    |
| nde           | MRK        |      678 |  18.37 |  59.79 | 59.77 |  -0.02 |
| nde           | [epistles] |      274 |  17.55 |  50.33 | 51.67 |   1.34 |
| nya           | GEN        |      250 |  24.7  |  54.55 | 54.29 |  -0.26 |
| nya           | MRK        |      678 |  22.68 |  62.02 | 62.59 |   0.57 |
| nya           | [epistles] |      274 |  20.73 |  49.63 | 51.38 |   1.75 |
