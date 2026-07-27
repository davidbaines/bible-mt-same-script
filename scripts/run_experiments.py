"""Pace the experiment fleet onto a ClearML queue under a free-worker gate.

House rule (David, 2026-07-23, tightened 2026-07-24): a run may only BEGIN
when at least two workers are free, so shared capacity stays available for
production and other agents. This launcher enqueues one experiment at a time,
only when the queue reports >= --min-free effective-free workers, and paces so
a just-enqueued job is picked up before the next gate check.

Safety and idempotency:
- Records every enqueue to experiments/fleet-tasks.csv; on re-invocation it
  skips configs already recorded as queued/in_progress/completed, so it is
  safe to stop and restart.
- Before each new enqueue it refreshes the status of its own enqueued tasks;
  if any has FAILED it stops rather than fanning out into a systemic problem
  (e.g. a queue whose workers can't reach the weights store — the per-run
  preflight makes that fail in seconds).
- Absolute paths and SYNOPTIC_ROOT are pinned so the invoking directory can
  never retarget reads/writes.

    .venv/bin/python scripts/run_experiments.py [--queue jobs_backlog]
        [--min-free 2] [--configs a,b,c]
"""

from __future__ import annotations

import argparse
import csv
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
os.environ.setdefault("SYNOPTIC_ROOT", str(REPO))

TRACK = REPO / "experiments" / "fleet-tasks.csv"
TERMINAL_BAD = {"failed", "stopped"}
DONE_OR_RUNNING = {"queued", "in_progress", "completed"}


def effective_free(queue: str) -> int:
    """Free workers on ``queue`` minus jobs already waiting in it."""
    from clearml.backend_api.session.client import APIClient

    c = APIClient()
    free = 0
    for w in c.workers.get_all():
        qs = [q.name for q in (getattr(w, "queues", None) or [])]
        if queue in qs and not getattr(w, "task", None):
            free += 1
    waiting = sum(len(getattr(q, "entries", []) or [])
                  for q in c.queues.get_all() if q.name == queue)
    return max(0, free - waiting)


def load_tracked() -> dict[str, dict]:
    if not TRACK.exists():
        return {}
    with TRACK.open(encoding="utf-8") as f:
        return {r["run"]: r for r in csv.DictReader(f)}


def write_tracked(rows: dict[str, dict]) -> None:
    TRACK.parent.mkdir(parents=True, exist_ok=True)
    with TRACK.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["run", "task_id", "status", "enqueued_at"])
        w.writeheader()
        for r in sorted(rows.values(), key=lambda r: r["run"]):
            w.writerow(r)


def refresh_statuses(rows: dict[str, dict]) -> None:
    from clearml import Task

    for r in rows.values():
        if r["status"] in ("completed",) or not r["task_id"]:
            continue
        try:
            r["status"] = Task.get_task(task_id=r["task_id"]).status
        except Exception:  # noqa: BLE001 - transient lookup failure, keep old
            pass


def enqueue(config: Path, queue: str) -> str | None:
    """Enqueue one experiment via the repo's train wrapper; return its task id."""
    proc = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "train.py"),
         "--config", str(config.relative_to(REPO)),
         "--remote-queue", queue, "--generate-after"],
        cwd=REPO, capture_output=True, text=True,
    )
    out = proc.stdout + proc.stderr
    for line in out.splitlines():
        if "task id=" in line:
            return line.split("task id=", 1)[1].split()[0].strip()
    print(f"  !! no task id in enqueue output for {config.name}:\n{out[-500:]}")
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--queue", default="jobs_backlog")
    ap.add_argument("--min-free", type=int, default=2)
    ap.add_argument("--configs", default=None,
                    help="comma-separated run names to limit to (default: all "
                         "configs/experiments/*.yaml except smoke)")
    ap.add_argument("--poll", type=int, default=90, help="seconds between gate checks")
    args = ap.parse_args()

    all_cfgs = {p.stem: p for p in sorted((REPO / "configs" / "experiments").glob("*.yaml"))
                if p.stem != "smoke"}
    if args.configs:
        wanted = set(args.configs.split(","))
        all_cfgs = {k: v for k, v in all_cfgs.items() if k in wanted}

    tracked = load_tracked()
    pending = [name for name in all_cfgs
               if tracked.get(name, {}).get("status") not in DONE_OR_RUNNING]
    print(f"{len(all_cfgs)} experiments; {len(pending)} pending "
          f"(queue={args.queue}, min_free={args.min_free})")

    while pending:
        refresh_statuses(tracked)
        write_tracked(tracked)
        bad = [r["run"] for r in tracked.values() if r["status"] in TERMINAL_BAD]
        if bad:
            print(f"STOP: enqueued run(s) {bad} in a bad state; not fanning out. "
                  "Investigate (transport/preflight?) before resuming.")
            return
        free = effective_free(args.queue)
        if free >= args.min_free:
            name = pending.pop(0)
            tid = enqueue(all_cfgs[name], args.queue)
            tracked[name] = {
                "run": name, "task_id": tid or "",
                "status": "queued" if tid else "enqueue_failed",
                "enqueued_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            }
            write_tracked(tracked)
            print(f"enqueued {name} ({tid}); effective_free was {free}; "
                  f"{len(pending)} left")
            time.sleep(args.poll)  # let a worker claim it before the next check
        else:
            print(f"waiting: effective_free={free} < {args.min_free}")
            time.sleep(args.poll)

    print(f"all experiments enqueued; task ids in {TRACK.relative_to(REPO)}")


if __name__ == "__main__":
    main()
