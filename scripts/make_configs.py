"""Generate the holdout and experiment YAMLs for every run (spec.md, "Runs").

Sources come from ``experiments/source-ranking.csv`` (eflomal mean over the
pool's targets, lower = better; the Ethiopic drafting runs force "the other OT
text" instead). Regenerates the Latin-control selection with NT truncation for
everything except the chosen source and the targets. Deterministic and
re-runnable; run after ``scripts/alignment/rank_sources.py``.

    .venv/bin/python scripts/make_configs.py
"""

import os
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
# Anchor every synoptic repo-level read/write (selection regeneration, data
# cache) to THIS repo, regardless of the invoking directory.
os.environ.setdefault("SYNOPTIC_ROOT", str(REPO))

import pandas as pd

from pools import POOLS

from synoptic.script_pool import build_pool, write_pool

TEST_BOOKS = "[MRK, JAS, 1PE, 2PE]"
GEN250 = "configs/test-verses-gen250.txt"

# Ethiopic drafting: only two OT texts exist, so each drafting run holds out
# one and forces the other as source (spec.md, "Runs").
ETHIOPIC_OT = {"gmve": "gofe", "gofe": "gmve"}  # target -> source


def winners() -> dict[str, str]:
    """Alignment winner per pool (mean eflomal over target rows, lower wins).

    Ethiopic is skipped: both its runs force "the other OT text" as source
    (ETHIOPIC_OT), so no alignment choice exists there. inf rows are scorer
    failures (eflomal emits inf on some pairs) and are dropped with a note —
    averaging them in would silently disqualify a candidate.
    """
    df = pd.read_csv(REPO / "experiments" / "source-ranking.csv")
    out = {}
    for pool, sub in df.groupby("pool"):
        if pool == "ethiopic":
            continue
        scored = sub[sub["other_is_target"]]
        bad = ~np.isfinite(scored["eflomal"])
        if bad.any():
            dropped = scored[bad][["candidate", "other"]].to_records(index=False)
            print(f"note: dropping {len(dropped)} inf eflomal row(s) for "
                  f"{pool}: {list(dropped)}")
            scored = scored[~bad]
        if scored.empty:
            raise SystemExit(
                f"no finite eflomal target rows for pool {pool!r}; re-run "
                "scripts/alignment/rank_sources.py"
            )
        agg = scored.groupby("candidate")["eflomal"].mean()
        out[pool] = agg.idxmin()
    return out


def holdout_yaml(entries: dict[str, str], verse_entries: list[str],
                 comment: str) -> str:
    lines = [f"# {comment}", "holdouts:"]
    for tid, books in entries.items():
        lines.append(f"  {tid}: {books}")
    if verse_entries:
        lines.append("verse_holdouts:")
        for tid in verse_entries:
            lines.append(f"  {tid}: [{GEN250}]")
    lines += ["valid_size: 5000", "seed: 13"]
    return "\n".join(lines) + "\n"


def experiment_yaml(*, name: str, pool: str, holdouts: str, source: str,
                    multi_source: bool, comment: str) -> str:
    data = [
        f"  selection: experiments/selection-{pool}.csv",
        f"  holdouts: {holdouts}",
        f"  source: {source}",
        "  companion_ranking: coverage   # v1 behaviour, uniform across all runs",
    ]
    if multi_source:
        data += [
            "  pairing: multi-source",
            "  k: 8",
            "  k_min: 1",
            "  max_len: 192",
            "  max_src_len: 640",
            "  max_ratio: 0",
        ]
        batch = ["  per_device_batch_size: 32     # max_src_len 640 on 40 GB; effective 256 seqs",
                 "  gradient_accumulation: 8"]
        probe_batch = 32
    else:
        data += [
            "  max_len: 192",
            "  max_ratio: 2.0",
        ]
        batch = ["  per_device_batch_size: 128    # effective 256 seqs",
                 "  gradient_accumulation: 2"]
        probe_batch = 64
    return "\n".join([
        f"# {comment}",
        f"# Hyperparameters inherit from bible-interlingua's "
        f"{'ms8_ie_shareable' if multi_source else 'ie_big_shareable (ebible-mt)'}",
        "# so the same-script comparison changes one variable (spec.md).",
        f"name: {name}",
        f"phase: {'multi-source' if multi_source else 'one-to-many'}",
        "",
        "data:",
        *data,
        "",
        "tokenizer:",
        "  type: bpe",
        "  vocab_size: 32000",
        "",
        "model:                    # transformer-big (~210M)",
        "  arch: marian",
        "  encoder_layers: 6",
        "  decoder_layers: 6",
        "  d_model: 1024",
        "  encoder_attention_heads: 16",
        "  decoder_attention_heads: 16",
        "  encoder_ffn_dim: 4096",
        "  decoder_ffn_dim: 4096",
        "  dropout: 0.1",
        "  label_smoothing: 0.1",
        "",
        "training:",
        "  lr: 5.0e-4",
        "  warmup_steps: 4000",
        "  lr_scheduler: cosine",
        *batch,
        "  max_grad_norm: 1.0",
        "  bf16: true",
        "  max_steps: 100000             # ceiling; probe early-stopping usually ends sooner",
        "  eval_every_steps: 2000",
        "  seed: 13",
        "",
        "inference:",
        "  beam: 5",
        "  length_penalty: 1.0",
        "  max_length: 192",
        "",
        "validation:                    # disjoint from train AND test (v2 policy)",
        "  every_steps: 1000",
        "  verses_per_language: 250",
        "  min_gain: 0.2                 # silnlp early-stop defaults",
        "  patience_steps: 4000",
        f"  batch_size: {probe_batch}",
        "  seed: 13",
    ]) + "\n"


def main() -> None:
    win = winners()
    print(f"sources by alignment: {win}")

    # Latin control: regenerate the selection with NT truncation for every
    # non-source, non-target member (spec.md, "Scripts and pools").
    sel = build_pool(POOLS["latin-bantu"], nt_only_except=[win["latin-bantu"]])
    out = write_pool(sel, "latin-bantu")
    print(f"rewrote {out} (ntOnly except {win['latin-bantu']} + targets)")

    runs: list[tuple[str, str, str, str, bool, str]] = []
    for pool, spec in POOLS.items():
        slug = pool.replace("-", "_")
        lang_of = {}  # translationId -> languageCode, for run naming
        selection = pd.read_csv(REPO / "experiments" / f"selection-{pool}.csv")
        lang_of = dict(zip(selection["translationId"], selection["languageCode"]))
        t1, t2 = spec.targets

        if pool == "telugu":
            # NT-only targets: the two conditions collapse (spec.md, "Runs").
            hfile = "configs/holdouts-telugu.yaml"
            (REPO / hfile).write_text(holdout_yaml(
                {t1: TEST_BOOKS, t2: TEST_BOOKS}, [],
                "Telugu: NT-only targets; the drafting and gap-filling "
                "conditions collapse.",
            ), encoding="utf-8")
            for ms in (True, False):
                runs.append((f"{'ms8' if ms else 'base'}_telugu", pool, hfile,
                             win[pool], ms, "Telugu minimum-pool run"))
            continue

        if pool == "ethiopic":
            # Both conditions run one target at a time: gmve and gofe are the
            # only OT texts, so a packed run would leave the held-out OT (or
            # Genesis-250) verses with zero source renderings. The other OT
            # text is always the source.
            for tgt, src in ETHIOPIC_OT.items():
                code = lang_of[tgt]
                hfile = f"configs/holdouts-ethiopic-drafting-{code}.yaml"
                (REPO / hfile).write_text(holdout_yaml(
                    {tgt: "[OT, MRK, JAS, 1PE, 2PE]"}, [],
                    f"Ethiopic drafting, target {code}: whole OT + NT test "
                    f"sets; {src} stays in the pool as the source.",
                ), encoding="utf-8")
                gfile = f"configs/holdouts-ethiopic-gapfill-{code}.yaml"
                (REPO / gfile).write_text(holdout_yaml(
                    {tgt: TEST_BOOKS}, [tgt],
                    f"Ethiopic gap-filling, target {code}: NT test sets plus "
                    f"Genesis-250; {src} stays in the pool as the source.",
                ), encoding="utf-8")
                for ms in (True, False):
                    kind = "ms8" if ms else "base"
                    runs.append((
                        f"{kind}_ethiopic_drafting_{code}", pool, hfile, src,
                        ms, f"Ethiopic drafting condition, target {code}",
                    ))
                    runs.append((
                        f"{kind}_ethiopic_gapfill_{code}", pool, gfile, src,
                        ms, f"Ethiopic gap-filling condition, target {code}",
                    ))
            continue
        else:
            hfile = f"configs/holdouts-{pool}-drafting.yaml"
            (REPO / hfile).write_text(holdout_yaml(
                {t1: "[OT, MRK, JAS, 1PE, 2PE]", t2: "[OT, MRK, JAS, 1PE, 2PE]"},
                [],
                f"{pool} drafting condition: both targets train NT-only "
                "(whole OT + NT test sets held out).",
            ), encoding="utf-8")
            for ms in (True, False):
                runs.append((
                    f"{'ms8' if ms else 'base'}_{slug}_drafting", pool, hfile,
                    win[pool], ms, f"{pool} drafting condition",
                ))

        # Gap-filling: packed run, both targets, NT test sets + Genesis-250.
        hfile = f"configs/holdouts-{pool}-gapfill.yaml"
        (REPO / hfile).write_text(holdout_yaml(
            {t1: TEST_BOOKS, t2: TEST_BOOKS}, [t1, t2],
            f"{pool} gap-filling condition: NT test sets plus the committed "
            "Genesis-250 verse list.",
        ), encoding="utf-8")
        for ms in (True, False):
            runs.append((
                f"{'ms8' if ms else 'base'}_{slug}_gapfill", pool, hfile,
                win[pool], ms, f"{pool} gap-filling condition",
            ))

    for name, pool, hfile, source, ms, comment in runs:
        path = REPO / "configs" / "experiments" / f"{name}.yaml"
        path.write_text(experiment_yaml(
            name=name, pool=pool, holdouts=hfile, source=source,
            multi_source=ms, comment=comment,
        ), encoding="utf-8")
    print(f"wrote {len(runs)} experiment configs under configs/experiments/")
    for name, *_ in runs:
        print(f"  {name}")


if __name__ == "__main__":
    main()
