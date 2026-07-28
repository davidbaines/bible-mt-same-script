"""Collect NLLB-1.3B (silnlp) per-book chrF3 and compare against synoptic.

For each of the 18 SOTA runs it reads silnlp's per-book scores from the store
(highest-step checkpoint), or — for a run whose scoring step did not emit a CSV
— scores locally from the detok refs/predictions with the identical metric
(sacrebleu char_order=6, word_order=0, beta=3; verified to reproduce silnlp's
numbers to 0.00 under both sacrebleu 2.4.3 and 2.6.0). It joins each run to its
synoptic ms8 (contender) and base (single-source) run on the target
translationId + book, and classifies ms8 vs NLLB per book as beat/tie/lose
(|Δ| < TIE = tie). Writes normalised per-run CSVs (git-tracked; weights stay in
the store) and experiments/sota-comparison.md.

    .venv/bin/python scripts/sota_compare.py
"""
from __future__ import annotations

import csv
import os
from collections import defaultdict
from pathlib import Path

import pandas as pd
import yaml
from sacrebleu.metrics import CHRF

REPO = Path(__file__).resolve().parents[1]
EXP = REPO / "experiments"
SOTA_OUT = EXP / "sota"
STORE = Path(os.environ.get("SIL_NLP_DATA_PATH", str(Path.home() / "M"))) / \
    "MT" / "experiments" / "synoptic-sota" / "bible-mt-same-script"
TIE = 1.0  # |ms8 - nllb| < TIE chrF3 counts as a tie

# run -> (ms8 synoptic run, base synoptic run)
RUNMAP = {
    "arabic_drafting_urd": ("ms8_arabic_drafting", "base_arabic_drafting"),
    "arabic_drafting_ckb": ("ms8_arabic_drafting", "base_arabic_drafting"),
    "arabic_gapfill_urd": ("ms8_arabic_gapfill", "base_arabic_gapfill"),
    "arabic_gapfill_ckb": ("ms8_arabic_gapfill", "base_arabic_gapfill"),
    "devanagari_drafting_hne": ("ms8_devanagari_drafting", "base_devanagari_drafting"),
    "devanagari_drafting_mar": ("ms8_devanagari_drafting", "base_devanagari_drafting"),
    "devanagari_gapfill_hne": ("ms8_devanagari_gapfill", "base_devanagari_gapfill"),
    "devanagari_gapfill_mar": ("ms8_devanagari_gapfill", "base_devanagari_gapfill"),
    "ethiopic_drafting_gmv": ("ms8_ethiopic_drafting_gmv", "base_ethiopic_drafting_gmv"),
    "ethiopic_drafting_gof": ("ms8_ethiopic_drafting_gof", "base_ethiopic_drafting_gof"),
    "ethiopic_gapfill_gmv": ("ms8_ethiopic_gapfill_gmv", "base_ethiopic_gapfill_gmv"),
    "ethiopic_gapfill_gof": ("ms8_ethiopic_gapfill_gof", "base_ethiopic_gapfill_gof"),
    "latin_bantu_drafting_nde": ("ms8_latin_bantu_drafting", "base_latin_bantu_drafting"),
    "latin_bantu_drafting_nya": ("ms8_latin_bantu_drafting", "base_latin_bantu_drafting"),
    "latin_bantu_gapfill_nde": ("ms8_latin_bantu_gapfill", "base_latin_bantu_gapfill"),
    "latin_bantu_gapfill_nya": ("ms8_latin_bantu_gapfill", "base_latin_bantu_gapfill"),
    "telugu_nt-only_nit": ("ms8_telugu", "base_telugu"),
    "telugu_nt-only_vgr": ("ms8_telugu", "base_telugu"),
}
EPISTLES = ["JAS", "1PE", "2PE"]


def target_project(run: str) -> str:
    """Target translationId from the run's config.yml trg stem (join key)."""
    cfg = yaml.safe_load((STORE / run / "config.yml").read_text())
    stem = cfg["data"]["corpus_pairs"][0]["trg"]  # "<iso>-<tid>_synsota"
    return stem.removesuffix("_synsota").split("-", 1)[1]


def _max_step(paths: list[Path]) -> Path:
    return max(paths, key=lambda p: int(p.stem.split("-")[1]))


def nllb_scores(run: str) -> tuple[pd.DataFrame, str]:
    """Per-book NLLB chrF3 for a run: from the store CSV, else scored locally."""
    csvs = sorted((STORE / run).glob("scores-*.csv"))
    if csvs:
        df = pd.read_csv(_max_step(csvs))
        out = df[["book", "trg_iso", "sent_len", "chrF3"]].rename(
            columns={"sent_len": "verses_nllb", "chrF3": "nllb"})
        return out, "store"
    return _score_locally(run), "local"


def _score_locally(run: str) -> pd.DataFrame:
    d = STORE / run
    preds = sorted(d.glob("test.trg-predictions.detok.txt.*"),
                   key=lambda p: int(p.suffix[1:]) if p.suffix[1:].isdigit() else -1)
    pred = [p for p in preds if p.suffix[1:].isdigit()][-1]
    vref = [l.split()[0] for l in (d / "test.vref.txt").read_text().splitlines()]
    refs = (d / "test.trg.detok.txt").read_text().splitlines()
    hyps = pred.read_text().splitlines()
    assert len(vref) == len(refs) == len(hyps)
    chrf = CHRF(char_order=6, word_order=0, beta=3)
    br, bh = defaultdict(list), defaultdict(list)
    for b, r, h in zip(vref, refs, hyps):
        br[b].append(r); bh[b].append(h)
    br["ALL"], bh["ALL"] = refs, hyps
    # trg iso is the run's last name segment (e.g. arabic_drafting_ckb -> ckb)
    trg_iso = run.split("_")[-1]
    rows = [{"book": b, "trg_iso": trg_iso, "verses_nllb": len(br[b]),
             "nllb": round(chrf.corpus_score(bh[b], [br[b]]).score, 2)}
            for b in br]
    return pd.DataFrame(rows)


def syn_scores(syn_run: str, tid: str) -> pd.DataFrame:
    df = pd.read_csv(EXP / f"scores-{syn_run}.csv")
    df = df[df["translation"] == tid]
    return df[["book", "verses", "copy_chrF3", "chrF3"]].rename(
        columns={"verses": "verses_syn", "copy_chrF3": "copy"})


def verdict(delta: float) -> str:
    if abs(delta) < TIE:
        return "tie"
    return "beat" if delta > 0 else "lose"


def main() -> None:
    SOTA_OUT.mkdir(exist_ok=True)
    all_rows = []
    for run, (ms8_run, base_run) in RUNMAP.items():
        tid = target_project(run)
        nllb, source = nllb_scores(run)
        nllb.to_csv(SOTA_OUT / f"scores-{run}.csv", index=False)
        ms8 = syn_scores(ms8_run, tid).rename(columns={"chrF3": "ms8"})
        base = syn_scores(base_run, tid)[["book", "chrF3"]].rename(columns={"chrF3": "base"})
        m = ms8.merge(base, on="book").merge(
            nllb[["book", "verses_nllb", "nllb"]], on="book")
        m["run"] = run; m["target"] = tid; m["score_src"] = source
        m["delta"] = (m["ms8"] - m["nllb"]).round(2)
        m["verdict"] = m["delta"].apply(verdict)
        all_rows.append(m)
    full = pd.concat(all_rows, ignore_index=True)
    full.to_csv(SOTA_OUT / "all-per-book.csv", index=False)
    _write_md(full)
    _print_summary(full)


def _bt_l(df: pd.DataFrame) -> str:
    v = df["verdict"].value_counts()
    return f"{v.get('beat',0)}/{v.get('tie',0)}/{v.get('lose',0)}"


def _print_summary(full: pd.DataFrame) -> None:
    print("per-run beat/tie/lose (ms8 vs NLLB), all books incl. NT:")
    for run in RUNMAP:
        d = full[full["run"] == run]
        ot = d[~d["book"].isin(["ALL", "MRK", *EPISTLES])]
        print(f"  {run:28} all={_bt_l(d)}  OT-only={_bt_l(ot)}  "
              f"meanΔ={d[d.book!='ALL']['delta'].mean():+.1f}")
    nn = full[full.book != "ALL"]
    print(f"\nTOTAL per-book (excl ALL): {_bt_l(nn)}  (beat/tie/lose)")


def _tbl(df: pd.DataFrame, books: list[str]) -> str:
    d = df[df["book"].isin(books)].copy()
    d["book"] = pd.Categorical(d["book"], categories=books, ordered=True)
    d = d.sort_values("book")
    cols = ["book", "verses_syn", "verses_nllb", "copy", "base", "ms8", "nllb", "delta", "verdict"]
    return d[cols].to_markdown(index=False)


def _write_md(full: pd.DataFrame) -> None:
    lines = [
        "# SOTA comparison: synoptic (closed-text) vs NLLB-1.3B", "",
        "Contender = synoptic **ms8** (from-scratch, multi-source K=8, eBible "
        "only). SOTA = **facebook/nllb-200-distilled-1.3B** fine-tuned by silnlp "
        "on the *same* source→target parallel data and scored on the *same* test "
        "verses, per book. chrF3 is sacrebleu `char_order=6, word_order=0, "
        f"beta=3` for both (byte-identical across sacrebleu 2.4.3/2.6.0). "
        f"`Δ = ms8 − nllb`; verdict tie when `|Δ| < {TIE:g}`. `copy` = "
        "source-copy floor; `base` = synoptic single-source. NLLB checkpoint = "
        "final step (load_best_model_at_end); `arabic_drafting_ckb` scored "
        "locally (its silnlp scoring step emitted no CSV) — metric verified to "
        "reproduce silnlp to 0.00.", "",
        "**Verse counts** `verses_syn` vs `verses_nllb` can differ slightly: "
        "NLLB keeps a verse when present in source+target; synoptic ms8 also "
        "requires source-side coverage across its fusion set. Where they differ "
        "the chrF3 is over near-identical (not identical) verse sets.", "",
        "## Headline", "",
        "_(filled from the numbers below)_", "",
    ]
    # per-run sections
    for run, (ms8_run, base_run) in RUNMAP.items():
        d = full[full["run"] == run]
        tid = d["target"].iloc[0]
        drafting = "drafting" in run
        ot = d[~d["book"].isin(["ALL", "MRK", *EPISTLES])]
        lines += [f"## {run}  (target `{tid}`)", ""]
        focus = (["GEN", "MRK", *EPISTLES] if not drafting
                 else ["MRK", *EPISTLES, "GEN"])
        lines += [_tbl(d, focus), ""]
        if drafting and len(ot):
            lines += [
                f"OT books (n={len(ot)}): beat/tie/lose = **{_bt_l(ot)}**, "
                f"mean Δ = **{ot['delta'].mean():+.1f}** chrF3 "
                f"(ms8 mean {ot['ms8'].mean():.1f} vs NLLB {ot['nllb'].mean():.1f}). "
                f"Best OT for ms8:", ""]
            best = ot.sort_values("delta", ascending=False).head(5)
            lines += [_tbl(best, list(best["book"])), ""]
    # totals
    nn = full[full.book != "ALL"]
    lines += ["## Totals (per book, excluding the ALL row)", "",
              f"- beat/tie/lose across all {len(nn)} book-rows: **{_bt_l(nn)}**",
              f"- OT-only: **{_bt_l(nn[~nn['book'].isin(['MRK', *EPISTLES])])}**",
              f"- NT-only (MRK + epistles): **{_bt_l(nn[nn['book'].isin(['MRK', *EPISTLES])])}**",
              ""]
    (EXP / "sota-comparison.md").write_text("\n".join(lines), encoding="utf-8")
    print("wrote experiments/sota-comparison.md")


if __name__ == "__main__":
    main()
