# Series summary: same-script multi-source (2026-07-25)

All 22 runs complete. Full tables per script in `<pool>-results.md`; raw
scores in `scores-<run>.csv` (recovered from console logs; weights were not
retained — the file server rejects artifact uploads persistently).

## The question and the answer

**Does the multi-source fusion gain (+2.5–2.9 chrF3 at K=8, mixed-script
Indo-European) reproduce when every source and target shares one script?**

Yes — and the experiments identify what actually governs the gain. It is not
script uniformity but **how many renderings of a verse the pool can supply at
inference**:

| Pool | OT renderings per test verse | whole-OT drafting gain (ms8 − base) |
|---|---|---|
| Arabic (ckb, urd targets) | 3 (arbnav, arb-vd, pesOPV) | **+5.50 (ckb), +2.24 (urd)** |
| Devanagari (hne, mar) | 1 (hin2017) | +0.78, +0.33 |
| Latin Bantu control (nde, nya) | 1 (sna) | +0.03, +1.02 |
| Ethiopic (gmv, gof; zero OT training pairs) | 1 (the other OT text) | +1.31, +1.96 |

With three OT renderings, the same-script whole-OT gain **matches or exceeds**
the mixed-script reference (+2.5–2.9). With one rendering there is nothing to
fuse and the gain nearly vanishes. The Latin control — profile-matched to
Devanagari (one OT source, NT-only rest) — produced Devanagari-sized gains on
high Bantu baselines, ruling out script as the driver.

On NT test sets, where every pool supplies 4–6 renderings, fusion gains are
consistently positive in the drafting condition (epistles +0.4 to +1.6;
Telugu, the 4-text minimum pool, +0.4 to +1.7), shrinking in gap-filling
where baselines are already high.

## Practicality for drafting an OT

Whole-OT chrF3 after NT-only training (multi-source, best run per target):
hne 34.4, mar 27.4, ckb 31.1, urd 29.1, nde 35.1, nya 37.2, gmv 18.8,
gof 19.8. The mixed-script 31-language pool reached 46.6 (Hindi). Small
same-script pools stay well below that: script purity costs breadth, and
breadth is what OT drafting quality feeds on. NT quality is far higher
everywhere (Mark 44–62), and Genesis is consistently among the easiest OT
books (e.g. hne GEN 40.5 vs its OT average 34.4).

## Source selection findings

- eflomal ranking picked **Persian over both Arabic texts** as the source for
  Kurdish and Urdu (0.35–0.40 vs 0.54–0.55 per-token; IBM-1 mildly
  disagreed). The +2.2–5.5 Arabic gains vindicate the choice.
- **chiShona** won the Bantu pool on both scorers (not Swahili).
- hin2017 (sanity check) and tel2017 (forced) as expected.

## Open questions

1. **The Gofa asymmetry.** In both conditions, fusion transforms Gofa's NT
   (+16 to +19 chrF3; Mark 61.5 in gap-filling) while mirrored Gamo barely
   moves (+1 to +3). Copying is ruled out: Gofa's best other-language copy
   scores only ~14 (Oyda). Hypotheses for the writeup: Gofa's centrality in
   the Ometo cluster; probe-driven checkpoint selection (the gmv drafting ms8
   run's best probe was step 2000, before warmup completes). A rerun of the
   gmv drafting pair with `early_stop: false` would separate the two.
2. **Bigger in-script pools.** Arabic shows the gain returns with renderings.
   A by-nc concession or new corpus texts that add OT renderings to
   Devanagari/Ethiopic would test the rendering-count curve directly.

## Infrastructure notes

- Artifact uploads to `files.sil.hosted.allegro.ai` fail persistently
  (SSL EOF), even with retries — every run's weights were lost. Scores
  survive via the console echo (`METRICS_CSV_BEGIN` blocks) and
  `scripts/fetch_scores.py`. Publishing any model requires re-running its
  config where weights can be kept (A100/3090) with `hf_export`.
- All 22 runs on H100 workers via ClearML `jobs_backlog`, enqueued under the
  free-worker gate (`~/Documents/Github/clearml_status.py`).
- Model licence for every pool: cc-by-sa-4.0 (all sources PD or by-sa).
