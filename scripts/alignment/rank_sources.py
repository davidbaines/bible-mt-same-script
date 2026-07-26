"""Rank candidate sources per script pool by alignment (spec.md, "Source").

For every pool: candidates are the full-coverage members that are not targets
(Ethiopic has none, so there the two OT texts — the targets themselves — are
ranked for the gap-filling run; the drafting runs force "the other OT text").
Each candidate is scored against every other pool member on the shared NT
verses (capped at 3000), with two scorers:

- IBM-1 alignability (``samileides.align_score``) — higher is better;
- eflomal per-token score (helper in the ``.venv-eflomal`` venv) — lower is
  better.

Output: ``experiments/source-ranking.csv`` (one row per candidate-member
pair) and a winners summary. The eflomal winner is the pool's source; IBM-1
is the sanity cross-check (spec.md, "Verification").

    .venv/bin/python scripts/alignment/rank_sources.py [--pools devanagari,...]
"""

import argparse
import csv
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import pandas as pd

from pools import POOLS

from synoptic.align_score import alignability, parallel_tokens
from synoptic.data import load_verses

EFLOMAL_PY = REPO / ".venv-eflomal" / "bin" / "python"
EFLOMAL_HELPER = REPO / "scripts" / "alignment" / "eflomal_score.py"
FULL_OT, FULL_NT = 20000, 7000


def write_lines(sents, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(" ".join(s) for s in sents) + "\n")


def eflomal_score(a_sents, b_sents) -> float:
    with tempfile.TemporaryDirectory() as d:
        write_lines(a_sents, f"{d}/a.txt")
        write_lines(b_sents, f"{d}/b.txt")
        out = subprocess.run(
            [str(EFLOMAL_PY), str(EFLOMAL_HELPER), f"{d}/a.txt", f"{d}/b.txt"],
            capture_output=True, text=True, check=True,
        )
        return float(out.stdout.strip().split("\n")[-1])


def candidates_for(pool: str, selection: pd.DataFrame) -> list[str]:
    spec = POOLS[pool]
    full = selection[
        (selection["OTverses"].astype(int) >= FULL_OT)
        & (selection["NTverses"].astype(int) >= FULL_NT)
    ]
    cands = [t for t in full["translationId"] if t not in spec.targets]
    # Ethiopic: only the two targets have OTs; rank them for the gap-filling
    # run (the drafting runs force the other OT text as source anyway).
    return cands or full["translationId"].tolist()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pools", default=",".join(sorted(POOLS)))
    args = ap.parse_args()
    pools = args.pools.split(",")

    rows = []
    for pool in pools:
        selection = pd.read_csv(REPO / "experiments" / f"selection-{pool}.csv")
        members = selection["translationId"].tolist()
        targets = POOLS[pool].targets
        cands = candidates_for(pool, selection)
        verses = load_verses(members)
        print(f"=== {pool}: candidates {cands} ===", flush=True)
        for cand in cands:
            for other in members:
                if other == cand:
                    continue
                a, b = parallel_tokens(verses, cand, other)
                ibm1 = alignability(a, b)
                efl = eflomal_score(a, b)
                rows.append({
                    "pool": pool, "candidate": cand, "other": other,
                    "other_is_target": other in targets, "n": len(a),
                    "ibm1_align": round(ibm1, 4), "eflomal": efl,
                })
                print(f"  {cand} ~ {other}: n={len(a)} ibm1={ibm1:.4f} "
                      f"eflomal={efl}", flush=True)

    out = REPO / "experiments" / "source-ranking.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"WROTE {out}", flush=True)

    df = pd.DataFrame(rows)
    print("\n=== winners (mean over pool targets; eflomal lower = better) ===")
    for pool in pools:
        sub = df[(df["pool"] == pool) & df["other_is_target"]]
        if sub.empty:  # Ethiopic candidates ARE the targets: use all others
            sub = df[df["pool"] == pool]
        agg = sub.groupby("candidate")[["ibm1_align", "eflomal"]].mean()
        ibm1_best = agg["ibm1_align"].idxmax()
        efl_best = agg["eflomal"].idxmin()
        verdict = "SAME" if ibm1_best == efl_best else "DIFFERENT"
        print(f"{pool}: eflomal -> {efl_best} | IBM-1 -> {ibm1_best} | {verdict}")
        print(agg.sort_values("eflomal").to_string())


if __name__ == "__main__":
    main()
