# v2 results: devanagari

chrF3, corpus-level. `copy` = source-copy floor; `base` = single-source; `ms8` = multi-source K=8; `gain` = ms8 - base. Clean methodology (validation set disjoint from train+test).

## Devanagari drafting

`ms8_devanagari_drafting` vs `base_devanagari_drafting`

| translation   | book       |   verses |   copy |   base |   ms8 |   gain |
|:--------------|:-----------|---------:|-------:|-------:|------:|-------:|
| hne           | GEN        |     1533 |  23.53 |  38.95 | 40.25 |   1.3  |
| hne           | MRK        |      678 |  19.83 |  58.27 | 57.47 |  -0.8  |
| hne           | [epistles] |      274 |  20.63 |  44.27 | 44.91 |   0.64 |
| hne           | [OT]       |    23142 |  21.77 |  33.6  | 34.12 |   0.52 |
| mar           | GEN        |     1532 |  16.49 |  30    | 29.34 |  -0.66 |
| mar           | MRK        |      673 |  14.92 |  45.4  | 44.54 |  -0.86 |
| mar           | [epistles] |      272 |  17.24 |  34.18 | 33.82 |  -0.36 |
| mar           | [OT]       |    23140 |  16.79 |  27.35 | 26.36 |  -0.99 |

Easiest OT books by ms8 chrF3:

| translation   | book   |   verses |   base |   ms8 |   gain |
|:--------------|:-------|---------:|-------:|------:|-------:|
| hne           | GEN    |     1533 |  38.95 | 40.25 |   1.3  |
| hne           | 1SA    |      810 |  36.37 | 37.12 |   0.75 |
| hne           | 1KI    |      816 |  34.87 | 35.54 |   0.67 |
| hne           | PSA    |     2460 |  34.95 | 35.49 |   0.54 |
| hne           | JDG    |      618 |  33.95 | 34.8  |   0.85 |

## Devanagari gap-filling

`ms8_devanagari_gapfill` vs `base_devanagari_gapfill`

| translation   | book       |   verses |   copy |   base |   ms8 |   gain |
|:--------------|:-----------|---------:|-------:|-------:|------:|-------:|
| hne           | GEN        |      250 |  23.64 |  53.85 | 53.79 |  -0.06 |
| hne           | MRK        |      678 |  19.83 |  57.64 | 57.65 |   0.01 |
| hne           | [epistles] |      274 |  20.63 |  44.58 | 47.31 |   2.73 |
| mar           | GEN        |      250 |  16.88 |  39.73 | 39.95 |   0.22 |
| mar           | MRK        |      673 |  14.92 |  45.78 | 47.06 |   1.28 |
| mar           | [epistles] |      272 |  17.24 |  35.65 | 37.7  |   2.05 |
