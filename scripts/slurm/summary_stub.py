#!/usr/bin/env python3
"""
Maintain the run-level status of the notebook summary file around a batch job.

pytest writes the real summary in `pytest_sessionfinish`. If the job is killed first
(wall-clock limit, OOM, `scancel`), that hook never runs and `latest.json` would keep
showing the *previous* run's result -- a silently stale green. This script closes that
hole: the job script marks the summary "running" before pytest starts and "aborted" from
an EXIT trap afterwards.

The "aborted" transition only applies when the file is still "running" *and* was stamped
by this job, so it can never overwrite a summary pytest already produced.

Standard library only, so it runs under whatever `python3` the compute node provides.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _write_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2) + "\n")
    os.replace(tmp, path)


def _load(path: Path) -> dict[str, Any] | None:
    try:
        loaded = json.loads(path.read_text())
    except (OSError, ValueError):
        return None
    return loaded if isinstance(loaded, dict) else None


def mark_running(path: Path, job_id: str) -> str:
    """Stamp the summary as belonging to a job that has just started."""
    _write_atomic(
        path,
        {
            "schema_version": SCHEMA_VERSION,
            "status": "running",
            "run": {
                "started_at": _now(),
                "slurm": {"job_id": job_id},
            },
            "notebooks": [],
        },
    )
    return f"marked running (job {job_id})"


def mark_aborted(path: Path, job_id: str, message: str) -> str:
    """
    Downgrade a still-"running" summary belonging to `job_id` to "aborted".

    A no-op if the file is missing, unreadable, already finished by pytest, or owned
    by a different job.
    """
    current = _load(path)
    if current is None:
        return "no readable summary; nothing to do"
    if current.get("status") != "running":
        return f"summary already final ({current.get('status')!r}); left untouched"

    recorded = str(current.get("run", {}).get("slurm", {}).get("job_id"))
    if recorded != job_id:
        return f"summary belongs to job {recorded}, not {job_id}; left untouched"

    current["status"] = "aborted"
    run = current.setdefault("run", {})
    run["finished_at"] = _now()
    run["abort_reason"] = message
    _write_atomic(path, current)
    return f"marked aborted (job {job_id})"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", required=True, type=Path, help="Summary file to update.")
    parser.add_argument("--status", required=True, choices=("running", "aborted"))
    parser.add_argument("--job-id", required=True, help="SLURM job id owning this run.")
    parser.add_argument("--message", default="", help="Reason recorded for an aborted run.")
    args = parser.parse_args()

    if args.status == "running":
        print(mark_running(args.path, args.job_id))
    else:
        print(mark_aborted(args.path, args.job_id, args.message))
    return 0


if __name__ == "__main__":
    sys.exit(main())
