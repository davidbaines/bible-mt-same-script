"""Probe artifact uploads from a worker (sizes and destinations).

The ClearML file server drops large uploads unreliably (150 MB parts failed
4/4 on 2026-07-26 after a 200 MB probe passed the day before). The cluster
provides a MinIO store (bucket ``nlp-research``); this task uploads
incompressible dummies of increasing size so we can verify whether the
workers can write to it via ``--output-uri`` and whether size still matters.

    .venv/bin/python scripts/upload_probe.py --remote-queue cheetah_94gb \
        --output-uri s3://truenas.psonet.languagetechnology.org:9000/nlp-research/clearml
"""

import argparse
import os
import tempfile

SIZES_MB = [50, 150, 400]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--remote-queue", default=None)
    ap.add_argument("--output-uri", default=None)
    args = ap.parse_args()

    from clearml import Task

    task = Task.init(
        project_name="bible-mt-same-script",
        task_name="upload_probe_v2",
        output_uri=args.output_uri or None,
    )
    if args.remote_queue:
        task.set_base_docker(
            docker_image="pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime",
        )
        task.execute_remotely(queue_name=args.remote_queue, exit_process=True)

    results = {}
    for mb in SIZES_MB:
        with tempfile.NamedTemporaryFile(suffix=f"-{mb}mb.bin", delete=False) as f:
            chunk = os.urandom(1024 * 1024)
            for _ in range(mb):
                f.write(chunk)
            path = f.name
        try:
            ok = task.upload_artifact(f"probe_{mb}mb", artifact_object=path,
                                      wait_on_upload=True)
            results[mb] = bool(ok)
            print(f"UPLOAD_PROBE {mb}MB: {'OK' if ok else 'REJECTED'}", flush=True)
        except Exception as e:  # noqa: BLE001
            results[mb] = False
            print(f"UPLOAD_PROBE {mb}MB: FAILED {type(e).__name__}: {e}", flush=True)
        finally:
            os.unlink(path)
    print(f"UPLOAD_PROBE summary: {results}", flush=True)


if __name__ == "__main__":
    main()
