"""Generate v2 results docs and the v1-vs-v2 comparison from the score CSVs.

Reads experiments/scores-<run>.csv (v2, this fleet) and, where present,
experiments/v1-reference/scores-<run>.csv (the defective v1 run). Writes one
markdown table per script pool (ms8 vs single-source base, per named test set)
plus a series summary with the headline fusion gains and how much the v1
methodology defects moved the numbers.

    .venv/bin/python scripts/make_results.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
EXP = REPO / "experiments"
V1 = EXP / "v1-reference"

# (label, ms8 run, base run) — the 11 condition pairs (22 runs).
PAIRS = [
    ("Devanagari drafting", "ms8_devanagari_drafting", "base_devanagari_drafting"),
    ("Devanagari gap-filling", "ms8_devanagari_gapfill", "base_devanagari_gapfill"),
    ("Arabic drafting", "ms8_arabic_drafting", "base_arabic_drafting"),
    ("Arabic gap-filling", "ms8_arabic_gapfill", "base_arabic_gapfill"),
    ("Ethiopic drafting (gmv)", "ms8_ethiopic_drafting_gmv", "base_ethiopic_drafting_gmv"),
    ("Ethiopic drafting (gof)", "ms8_ethiopic_drafting_gof", "base_ethiopic_drafting_gof"),
    ("Ethiopic gap-filling (gmv)", "ms8_ethiopic_gapfill_gmv", "base_ethiopic_gapfill_gmv"),
    ("Ethiopic gap-filling (gof)", "ms8_ethiopic_gapfill_gof", "base_ethiopic_gapfill_gof"),
    ("Telugu (NT-only)", "ms8_telugu", "base_telugu"),
    ("Latin-Bantu drafting", "ms8_latin_bantu_drafting", "base_latin_bantu_drafting"),
    ("Latin-Bantu gap-filling", "ms8_latin_bantu_gapfill", "base_latin_bantu_gapfill"),
]
FOCUS = ["MRK", "[epistles]", "GEN", "[OT]"]
POOL_OF = {  # md filename grouping
    "Devanagari": "devanagari", "Arabic": "arabic", "Ethiopic": "ethiopic",
    "Telugu": "telugu", "Latin-Bantu": "latin-bantu",
}


def load(run: str, v1: bool = False) -> pd.DataFrame | None:
    p = (V1 if v1 else EXP) / f"scores-{run}.csv"
    return pd.read_csv(p) if p.exists() else None


def cmp_table(ms8: pd.DataFrame, base: pd.DataFrame) -> pd.DataFrame:
    key = ["translation", "book"]
    m = ms8.set_index(key)[["verses", "copy_chrF3", "chrF3"]].join(
        base.set_index(key)[["chrF3"]], rsuffix="_base")
    m["gain"] = (m["chrF3"] - m["chrF3_base"]).round(2)
    return m.rename(columns={"chrF3": "ms8", "chrF3_base": "base", "copy_chrF3": "copy"})


def focus_rows(m: pd.DataFrame) -> pd.DataFrame:
    f = m[m.index.get_level_values("book").isin(FOCUS)]
    return f.reset_index()[["translation", "book", "verses", "copy", "base", "ms8", "gain"]]


def main() -> None:
    # group pairs by pool for the per-pool docs
    by_pool: dict[str, list] = {}
    summary_rows = []
    for label, ms8_run, base_run in PAIRS:
        pool = next(p for name, p in POOL_OF.items() if name.split("-")[0] in label
                    or name in label)
        ms8, base = load(ms8_run), load(base_run)
        if ms8 is None or base is None:
            print(f"  skip {label}: missing scores")
            continue
        m = cmp_table(ms8, base)
        by_pool.setdefault(pool, []).append((label, ms8_run, base_run, m))
        # summary: whole-OT (drafting) or GEN (gapfill) + Mark, per target
        for (trg, book), row in m.iterrows():
            if book in ("[OT]", "GEN", "MRK", "[epistles]"):
                summary_rows.append({
                    "condition": label, "target": trg, "test": book,
                    "verses": int(row["verses"]), "copy": row["copy"],
                    "base": row["base"], "ms8": row["ms8"], "gain": row["gain"],
                })

    for pool, entries in by_pool.items():
        parts = [f"# v2 results: {pool}", "",
                 "chrF3, corpus-level. `copy` = source-copy floor; `base` = "
                 "single-source; `ms8` = multi-source K=8; `gain` = ms8 - base. "
                 "Clean methodology (validation set disjoint from train+test).", ""]
        for label, ms8_run, base_run, m in entries:
            parts += [f"## {label}", "", f"`{ms8_run}` vs `{base_run}`", "",
                      focus_rows(m).to_markdown(index=False), ""]
            drafting = "drafting" in label
            if drafting:
                ot = m[~m.index.get_level_values("book").str.startswith("[")]
                ot = ot[(ot["verses"] > 100)
                        & ~ot.index.get_level_values("book").isin(["MRK", "JAS", "1PE", "2PE"])]
                if len(ot):
                    top = ot.sort_values("ms8", ascending=False).head(5).reset_index()
                    parts += ["Easiest OT books by ms8 chrF3:", "",
                              top[["translation", "book", "verses", "base", "ms8", "gain"]]
                              .to_markdown(index=False), ""]
        (EXP / f"{pool}-results.md").write_text("\n".join(parts), encoding="utf-8")
        print(f"wrote {pool}-results.md")

    # series summary + v1-vs-v2
    s = pd.DataFrame(summary_rows)
    lines = ["# v2 series summary", "",
             "Fusion (ms8) vs single-source (base) chrF3 on the headline test "
             "sets, clean methodology.", "",
             s.to_markdown(index=False), "",
             "## v1 vs v2 (did the methodology fixes move the numbers?)", ""]
    v1v2 = []
    for label, ms8_run, base_run in PAIRS:
        v2, v1 = load(ms8_run), load(ms8_run, v1=True)
        if v2 is None or v1 is None:
            continue
        key = ["translation", "book"]
        j = v2.set_index(key)[["chrF3"]].join(v1.set_index(key)[["chrF3"]],
                                              rsuffix="_v1", how="inner")
        for (trg, book), row in j.iterrows():
            if book in ("[OT]", "GEN", "MRK"):
                v1v2.append({"condition": label, "target": trg, "test": book,
                             "v1_ms8": row["chrF3_v1"], "v2_ms8": row["chrF3"],
                             "delta": round(row["chrF3"] - row["chrF3_v1"], 2)})
    lines += [pd.DataFrame(v1v2).to_markdown(index=False) if v1v2 else "*(no v1 reference)*"]
    (EXP / "series-summary.md").write_text("\n".join(lines), encoding="utf-8")
    print("wrote series-summary.md")


if __name__ == "__main__":
    main()
