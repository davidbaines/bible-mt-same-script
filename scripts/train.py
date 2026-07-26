#!/usr/bin/env python3
"""Entry point for training runs — thin wrapper over synoptic.train.

ClearML remote execution captures the repo containing the entry-point file;
this wrapper keeps that THIS repo (configs, selections, holdouts), while the
toolkit itself arrives on the worker as the pinned synoptic dependency.

    .venv/bin/python scripts/train.py --config configs/experiments/<run>.yaml \
        --remote-queue jobs_backlog --generate-after
"""

from synoptic.train import main

if __name__ == "__main__":
    main()
