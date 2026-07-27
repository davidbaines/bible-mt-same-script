# v2 results: arabic

chrF3, corpus-level. `copy` = source-copy floor; `base` = single-source; `ms8` = multi-source K=8; `gain` = ms8 - base. Clean methodology (validation set disjoint from train+test).

## Arabic drafting

`ms8_arabic_drafting` vs `base_arabic_drafting`

| translation   | book       |   verses |   copy |   base |   ms8 |   gain |
|:--------------|:-----------|---------:|-------:|-------:|------:|-------:|
| ckb           | GEN        |     1533 |  14.17 |  27.96 | 31.56 |   3.6  |
| ckb           | MRK        |      678 |  13.19 |  49.6  | 52.69 |   3.09 |
| ckb           | [epistles] |      274 |  12.6  |  34.69 | 37.3  |   2.61 |
| ckb           | [OT]       |    23142 |  13.82 |  26.39 | 30.19 |   3.8  |
| urdoucv       | GEN        |     1533 |  11.95 |  28.53 | 31.48 |   2.95 |
| urdoucv       | MRK        |      678 |  11.17 |  43.63 | 44.77 |   1.14 |
| urdoucv       | [epistles] |      274 |  12.34 |  31.91 | 34.48 |   2.57 |
| urdoucv       | [OT]       |    23142 |  12.46 |  25.65 | 28.86 |   3.21 |

Easiest OT books by ms8 chrF3:

| translation   | book   |   verses |   base |   ms8 |   gain |
|:--------------|:-------|---------:|-------:|------:|-------:|
| ckb           | EZR    |      280 |  27.07 | 31.89 |   4.82 |
| ckb           | 2CH    |      822 |  27.06 | 31.87 |   4.81 |
| ckb           | JDG    |      618 |  27.07 | 31.77 |   4.7  |
| ckb           | 1SA    |      810 |  27.77 | 31.67 |   3.9  |
| ckb           | ZEC    |      211 |  28.32 | 31.6  |   3.28 |

## Arabic gap-filling

`ms8_arabic_gapfill` vs `base_arabic_gapfill`

| translation   | book       |   verses |   copy |   base |   ms8 |   gain |
|:--------------|:-----------|---------:|-------:|-------:|------:|-------:|
| ckb           | GEN        |      250 |  14.37 |  48.32 | 51.29 |   2.97 |
| ckb           | MRK        |      678 |  13.19 |  54.09 | 56.16 |   2.07 |
| ckb           | [epistles] |      274 |  12.6  |  39.38 | 41.7  |   2.32 |
| urdoucv       | GEN        |      250 |  11.85 |  44.88 | 46.44 |   1.56 |
| urdoucv       | MRK        |      678 |  11.17 |  45.39 | 46.41 |   1.02 |
| urdoucv       | [epistles] |      274 |  12.34 |  35.31 | 37.94 |   2.63 |
