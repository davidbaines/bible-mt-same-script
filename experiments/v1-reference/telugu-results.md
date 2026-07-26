# Results: telugu

chrF3, corpus-level. `copy` = source-copy baseline; `best-other` = strongest copy-another-pool-language baseline; `base` = single-source one-to-many; `ms8` = multi-source K=8; `gain` = ms8 - base. Scores recovered from run console logs (`scripts/fetch_scores.py`); weights were not retained (artifact uploads fail at the file server).

## NT-only (conditions collapse)

Runs: `ms8_telugu` vs `base_telugu`.

| translation   | book       |   verses |   copy |   best-other |   base |   ms8 |   gain |
|:--------------|:-----------|---------:|-------:|-------------:|-------:|------:|-------:|
| nit           | MRK        |      672 |  14.59 |        14.59 |  27.9  | 29.55 |   1.65 |
| nit           | [epistles] |      273 |  17.48 |        17.48 |  27.68 | 28.07 |   0.39 |
| vgr           | MRK        |      678 |  15.67 |        15.67 |  24.05 | 25.55 |   1.5  |
| vgr           | [epistles] |      274 |  18.36 |        18.36 |  21.75 | 22.95 |   1.2  |
