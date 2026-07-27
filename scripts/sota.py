"""Build silnlp NLLB-1.3B SOTA baselines mirroring this series' experiments.

For each condition (one base_* config per script+condition) and each target,
emit a silnlp experiment that fine-tunes facebook/nllb-200-distilled-1.3B on
the SAME primary-source->target parallel data and scores the SAME held-out
verses, per book. The test verses come from the very same
synoptic.data_pipeline split the synoptic models used, so the sets are
identical and the chrF3 numbers compare directly.

    .venv/bin/python scripts/sota.py --build            # export extracts + write configs
    .venv/bin/python scripts/sota.py --preprocess NAME  # silnlp preprocess one (verify)
    .venv/bin/python scripts/sota.py --run              # enqueue all (AFTER the synoptic fleet)

Everything lands under one collected tree on the M drive
(MT/experiments/synoptic-sota/bible-mt-same-script/), and extracts go in a
dedicated scripture dir so the shared silnlp scripture dir is untouched.
"""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
os.environ.setdefault("SYNOPTIC_ROOT", str(REPO))

from synoptic import sota
from synoptic.config import ExperimentConfig
from synoptic.data import VREF_COLUMN, load_metadata
from synoptic.data_pipeline import prepare

# One base_* config per (script, condition); each expands to one SOTA run per
# target. ms8_* share the same split, so they compare against the same run.
# (pool, condition) is stated explicitly rather than parsed from the name.
CONDITIONS: list[tuple[str, str, str]] = [
    ("base_devanagari_drafting", "devanagari", "drafting"),
    ("base_devanagari_gapfill", "devanagari", "gapfill"),
    ("base_arabic_drafting", "arabic", "drafting"),
    ("base_arabic_gapfill", "arabic", "gapfill"),
    ("base_ethiopic_drafting_gmv", "ethiopic", "drafting"),
    ("base_ethiopic_drafting_gof", "ethiopic", "drafting"),
    ("base_ethiopic_gapfill_gmv", "ethiopic", "gapfill"),
    ("base_ethiopic_gapfill_gof", "ethiopic", "gapfill"),
    ("base_telugu", "telugu", "nt-only"),
    ("base_latin_bantu_drafting", "latin_bantu", "drafting"),
    ("base_latin_bantu_gapfill", "latin_bantu", "gapfill"),
]

MT = Path(os.environ.get("SIL_NLP_DATA_PATH", str(Path.home() / "M"))) / "MT"
# The shared silnlp scripture dir — the one the remote workers read. Our
# extracts carry the _synsota project suffix (synoptic.sota.SOTA_PROJECT_SUFFIX)
# so they never collide with silnlp's own files.
SCRIPTURE_DIR = MT / "scripture"
REL_ROOT = "synoptic-sota/bible-mt-same-script"
COLLECT_DIR = MT / "experiments" / REL_ROOT

# Corpus script name -> FLORES/NLLB 4-letter code. Fail loud on an unknown
# script rather than mint a bogus language token.
_SCRIPT4 = {"Latin": "Latn", "Arabic": "Arab", "Devanagari": "Deva",
            "Ethiopic": "Ethi", "Telugu": "Telu"}


def _script4(script: str) -> str:
    try:
        return _SCRIPT4[script]
    except KeyError:
        raise SystemExit(
            f"unknown script {script!r}; add its FLORES 4-letter code to "
            "_SCRIPT4 before building SOTA configs"
        )


def build_specs() -> list[sota.SotaSpec]:
    m = load_metadata().set_index("translationId")
    specs: list[sota.SotaSpec] = []
    for cfg_name, pool, cond in CONDITIONS:
        cfg = ExperimentConfig.load(REPO / "configs" / "experiments" / f"{cfg_name}.yaml")
        data = prepare(cfg)
        order = {v: i for i, v in enumerate(data.verses.index)}  # canonical vref order
        src = cfg.data.source
        for trg, sub in data.splits.test.groupby("translation"):
            vrefs = sorted(sub[VREF_COLUMN], key=lambda v: order.get(v, 1 << 30))
            specs.append(sota.SotaSpec(
                name=f"{pool}_{cond}_{m.at[trg, 'languageCode']}",
                src_iso=m.at[src, "languageCode"], src_project=src,
                src_script=_script4(m.at[src, "script"]),
                trg_iso=m.at[trg, "languageCode"], trg_project=trg,
                trg_script=_script4(m.at[trg, "script"]),
                test_vrefs=list(vrefs),
            ))
    return specs


def cmd_build() -> None:
    specs = build_specs()
    translations = sorted({p for s in specs for p in (s.src_project, s.trg_project)})
    print(f"{len(specs)} SOTA baselines; exporting {len(translations)} extracts "
          f"to {SCRIPTURE_DIR}")
    sota.export_scripture(translations, SCRIPTURE_DIR)
    for s in specs:
        sota.write_experiment(s, COLLECT_DIR, rel_root=REL_ROOT)
        print(f"  wrote {REL_ROOT}/{s.name}: {s.src_iso}->{s.trg_iso}, "
              f"{len(s.test_vrefs)} test verses")


def cmd_preprocess(name: str) -> None:
    argv = ["python", "-m", "silnlp.nmt.experiment",
            sota.exp_relref(REL_ROOT, name), "--preprocess"]
    print("running:", " ".join(argv))
    subprocess.run(argv, check=True)


def cmd_run(queue: str) -> None:
    for s in build_specs():
        argv = sota.run(s.name, REL_ROOT, queue=queue)
        print("enqueue:", " ".join(argv))
        subprocess.run(argv, check=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--build", action="store_true", help="export extracts + write configs")
    ap.add_argument("--preprocess", metavar="NAME", help="silnlp preprocess one experiment")
    ap.add_argument("--run", action="store_true", help="enqueue all (after the synoptic fleet)")
    ap.add_argument("--queue", default="jobs_backlog")
    args = ap.parse_args()
    if args.build:
        cmd_build()
    if args.preprocess:
        cmd_preprocess(args.preprocess)
    if args.run:
        cmd_run(args.queue)
    if not (args.build or args.preprocess or args.run):
        ap.error("nothing to do; pass --build, --preprocess NAME, or --run")


if __name__ == "__main__":
    main()
