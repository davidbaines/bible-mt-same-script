"""Enqueue up to N pending SOTA baselines, gated on free workers.

Called in bounded batches (a long-lived launcher gets killed): each capacity
ping runs this with --limit = effective_free - 2 so >=2 workers stay free.
The silnlp command is built by synoptic.sota.run (the reviewed single source
of truth); we only swap in silnlp's poetry interpreter and run from the silnlp
repo so ClearML captures silnlp as the code repo. Task ids append to
experiments/sota-tasks.csv; already-enqueued runs are skipped (idempotent).

    .venv/bin/python scripts/sota_enqueue.py --limit 3
"""

from __future__ import annotations

import argparse
import re
import csv
import os
import subprocess
from pathlib import Path

from synoptic import sota

REPO = Path(__file__).resolve().parents[1]
REL_ROOT = "synoptic-sota/bible-mt-same-script"
COLLECT = Path(os.environ.get("SIL_NLP_DATA_PATH", str(Path.home() / "M"))) / \
    "MT" / "experiments" / REL_ROOT
SILNLP_DIR = Path("/home/david/Documents/Github/silnlp")
SILNLP_PY = Path("/home/david/.cache/pypoetry/virtualenvs/"
                 "silnlp-cTQHTH1u-py3.10/bin/python")
TRACK = REPO / "experiments" / "sota-tasks.csv"


def all_runs() -> list[str]:
    return sorted(d.name for d in COLLECT.iterdir()
                  if d.is_dir() and not d.name.endswith("__testset"))


def enqueued() -> set[str]:
    if not TRACK.exists():
        return set()
    return {r["run"] for r in csv.DictReader(TRACK.open())}


def append(run: str, task_id: str) -> None:
    new = not TRACK.exists()
    with TRACK.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["run", "task_id"])
        w.writerow([run, task_id])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=1)
    ap.add_argument("--queue", default="jobs_backlog")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    pending = [r for r in all_runs() if r not in enqueued()]
    env = dict(os.environ, SIL_NLP_DATA_PATH=str(Path.home() / "M"))
    n = 0
    for run in pending:
        if n >= args.limit:
            break
        argv = sota.run(run, REL_ROOT, queue=args.queue)
        argv[0] = str(SILNLP_PY)  # swap generic "python" for silnlp's env
        if args.dry_run:
            print("DRY:", " ".join(argv))
            n += 1
            continue
        out = subprocess.run(argv, cwd=SILNLP_DIR, env=env,
                             capture_output=True, text=True)
        blob = out.stdout + out.stderr
        # ClearML prints "task id=<32hex>" and ".../experiments/<32hex>/output/log"
        m = re.search(r"(?:task id=|/experiments/)([0-9a-f]{32})", blob)
        tid = m.group(1) if m else ""
        if not tid:
            print(f"  FAILED {run}:\n{blob[-600:]}")
            break
        append(run, tid)
        print(f"  enqueued {run} -> {tid}")
        n += 1
    print(f"enqueued {n}; total {len(enqueued())}/{len(all_runs())}")


if __name__ == "__main__":
    main()
