#!/usr/bin/env python3
"""
Execute the OPI documentation notebooks, locally or as a SLURM job array.

The notebooks in ``docs/contents/notebooks/`` drive real ORCA calculations and install
their own third-party dependencies at runtime, so they can never run in GitHub CI. This
script runs them anywhere else and leaves behind a machine-readable summary.

Every notebook is executed in its own scratch directory, in its own process, under its
own wall-clock limit. One hung notebook therefore cannot take the rest of the run with
it, and nothing is written next to the notebook sources.

Commands
--------
``list``    Show which notebooks would run, and which are skipped.
``local``   Execute the notebooks on this machine.
``slurm``   Submit them as a SLURM job array, one task per notebook.
``report``  Print (and refresh ``summary.json`` for) a finished or running run.
``task``    Execute one notebook of a run; used by the array tasks, rarely by hand.
``exec``    Innermost worker: runs the notebook itself. Not meant to be called directly.

Examples
--------
::

    # everything, here, one at a time
    scripts/run_notebooks.py local

    # a single notebook, keeping its working directory
    scripts/run_notebooks.py local how_to_opi --keep all

    # a job array on the cluster; returns as soon as it is queued
    scripts/run_notebooks.py slurm --partition normal --time 08:00:00 --cpus-per-task 8

    # ... and check on it later
    scripts/run_notebooks.py report notebook-runs/20260914T101500Z

The environment the notebooks run in is the one this script runs in (SLURM tasks inherit
the submitting environment via ``--export=ALL``). Set it up first::

    uv sync --group notebooks

Use ``--preamble FILE`` to inject site-specific shell setup (``module load``, activating a
venv, exporting ``OPI_ORCA``) into the generated job script.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = Path(__file__).resolve()

DEFAULT_NOTEBOOKS_DIR = REPO_ROOT / "docs" / "contents" / "notebooks"
DEFAULT_RUNS_DIR = REPO_ROOT / "notebook-runs"

# > Notebooks that cannot run unattended:
# >   extopt / ir_spectrum / ml_properties -> require external tooling,
# >   opencosmors                          -> its openCOSMO-RS_py install instruction lives
# >                                           in a markdown cell, so the import always fails.
# > Naming a notebook explicitly on the command line overrides this list.
DEFAULT_SKIP = ("extopt", "ir_spectrum", "ml_properties", "opencosmors")

DEFAULT_CELL_TIMEOUT = 1800
DEFAULT_NOTEBOOK_TIMEOUT = 7200
DEFAULT_MAX_PARALLEL = 4
DEFAULT_POLL_INTERVAL = 60
# > Consecutive unusable `squeue` answers after which --wait stops waiting rather than
# > spinning forever against a controller it cannot reach.
MAX_SQUEUE_FAILURES = 10

# > Bump when the layout of summary.json changes incompatibly.
SCHEMA_VERSION = 2

# > Grace period between SIGTERM and SIGKILL when a notebook overruns its wall-clock limit.
KILL_GRACE_S = 15

# > ORCA scratch files are large and worthless for a post-mortem.
ARTIFACT_IGNORE = shutil.ignore_patterns(
    "*.tmp", "*.tmp.*", "*.bas*", "*.densities*", "__pycache__", ".ipynb_checkpoints"
)

_ANSI = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                                       HELPERS
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def utcnow() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def strip_ansi(text: str) -> str:
    """Remove ANSI colour escapes, which IPython tracebacks are full of."""
    return _ANSI.sub("", text)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    """
    Write `payload` to `path` as JSON, atomically.

    The file is written next to its destination and then `os.replace`d into position, so
    a concurrent reader (a `report` running against a live run) never sees half a file.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2) + "\n")
    os.replace(tmp, path)


def read_json(path: Path) -> dict[str, Any] | None:
    """Read a JSON object from `path`, or return None if it is missing or unreadable."""
    try:
        loaded = json.loads(path.read_text())
    except (OSError, ValueError):
        return None
    return loaded if isinstance(loaded, dict) else None


def package_version(name: str) -> str | None:
    """Return the installed version of `name`, or None if it is not installed."""
    try:
        return version(name)
    except PackageNotFoundError:
        return None


def orca_version() -> str | None:
    """
    Return the ORCA version OPI would use, or None if ORCA cannot be reached.

    Deliberately broad in what it swallows: a missing or broken ORCA must never stop the
    run from being recorded, because the summary is the only channel through which an
    unattended run reports anything at all.
    """
    try:
        from opi.execution.core import Runner

        found = Runner().get_version()
    except Exception:
        return None
    return None if found is None else str(found)


def git_info(root: Path) -> dict[str, Any]:
    """Return commit, branch, describe and dirty state of the checkout at `root`."""

    def git(*args: str) -> str | None:
        try:
            proc = subprocess.run(
                ["git", "-C", str(root), *args], capture_output=True, text=True, timeout=15
            )
        except (OSError, subprocess.SubprocessError):
            return None
        return proc.stdout.strip() if proc.returncode == 0 else None

    dirty = git("status", "--porcelain")
    return {
        "commit": git("rev-parse", "HEAD"),
        "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "describe": git("describe", "--tags", "--always"),
        # > None (git unavailable) is not the same as "clean"; keep those distinguishable.
        "dirty": None if dirty is None else bool(dirty),
    }


def slurm_info() -> dict[str, str | None]:
    """Return the SLURM identifiers of the current process, all None outside a job."""
    return {
        "job_id": os.environ.get("SLURM_JOB_ID"),
        "array_job_id": os.environ.get("SLURM_ARRAY_JOB_ID"),
        "array_task_id": os.environ.get("SLURM_ARRAY_TASK_ID"),
        "partition": os.environ.get("SLURM_JOB_PARTITION"),
        "nodelist": os.environ.get("SLURM_JOB_NODELIST"),
        "cpus_per_task": os.environ.get("SLURM_CPUS_PER_TASK"),
    }


def environment_info() -> dict[str, Any]:
    """Collect provenance for the summary: host, git state and the versions that matter."""
    return {
        "hostname": socket.gethostname(),
        "user": os.environ.get("USER") or os.environ.get("LOGNAME"),
        "python_executable": sys.executable,
        "git": git_info(REPO_ROOT),
        "versions": {
            "python": platform.python_version(),
            "opi": package_version("orca-pi"),
            "orca": orca_version(),
            "nbclient": package_version("nbclient"),
        },
    }


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                                 NOTEBOOK DISCOVERY
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def all_notebooks(notebooks_dir: Path) -> list[Path]:
    """Return every notebook in `notebooks_dir`, sorted by name."""
    if not notebooks_dir.is_dir():
        raise SystemExit(f"FATAL: no notebook directory at {notebooks_dir}")
    return sorted(p for p in notebooks_dir.glob("*.ipynb") if ".ipynb_checkpoints" not in p.parts)


def select_notebooks(
    notebooks_dir: Path, selectors: list[str], skip: set[str]
) -> tuple[list[Path], list[str]]:
    """
    Resolve the command line selection into notebooks to run and notebooks to skip.

    Parameters
    ----------
    notebooks_dir : Path
        Directory holding the notebooks.
    selectors : list[str]
        Names, file names or glob patterns. Empty means "all of them".
    skip : set[str]
        Notebook stems to leave out. Ignored for explicitly named notebooks: naming one
        is how you run a notebook that is skipped by default.

    Returns
    -------
    tuple[list[Path], list[str]]
        The notebooks to execute and the stems that were skipped.
    """
    available = all_notebooks(notebooks_dir)
    if not selectors:
        chosen = [nb for nb in available if nb.stem not in skip]
        skipped = [nb.stem for nb in available if nb.stem in skip]
        return chosen, skipped

    chosen = []
    for selector in selectors:
        stem = Path(selector).stem
        matches = [nb for nb in available if nb.stem == stem or nb.match(selector)]
        if not matches:
            known = ", ".join(nb.stem for nb in available)
            raise SystemExit(f"FATAL: '{selector}' matches no notebook in {notebooks_dir}\n{known}")
        chosen.extend(nb for nb in matches if nb not in chosen)
    return sorted(chosen), []


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                                   RUN DIRECTORY
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def create_run(args: argparse.Namespace, backend: str) -> tuple[Path, dict[str, Any]]:
    """
    Lay out a fresh run directory and write its manifest.

    The manifest is the single source of truth for everything that happens afterwards:
    the local driver, the array tasks and `report` all read the notebook list and the
    settings from it, so a run can be re-reported (or a single task re-run) long after
    the command line that started it is gone.

    Returns
    -------
    tuple[Path, dict[str, Any]]
        The run directory and the manifest that was written into it.
    """
    skip = parse_skip(args.skip)
    notebooks, skipped = select_notebooks(args.notebooks_dir, args.notebooks, skip)
    if not notebooks:
        raise SystemExit("FATAL: no notebooks selected")

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = (args.run_dir or DEFAULT_RUNS_DIR / run_id).resolve()
    # > Reusing a run directory would mix this run's results with the previous one's and
    # > report the mixture as a single run. Runs are cheap; stale results are not.
    if (run_dir / "manifest.json").exists():
        raise SystemExit(
            f"FATAL: {run_dir} already holds a run.\n"
            "Pick another --run-dir, or delete that one. To re-run a single notebook "
            f"into it instead:\n    {SCRIPT_PATH} task {run_dir} <index>"
        )
    for sub in ("results", "logs", "executed"):
        (run_dir / sub).mkdir(parents=True, exist_ok=True)

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "backend": backend,
        "created_at": utcnow(),
        "repo_root": str(REPO_ROOT),
        "script": str(SCRIPT_PATH),
        "config": {
            "notebooks_dir": str(args.notebooks_dir.resolve()),
            "cell_timeout_s": args.cell_timeout,
            "notebook_timeout_s": args.timeout,
            "scratch_base": str(args.scratch_base) if args.scratch_base else None,
            "keep": args.keep,
            "kernel": args.kernel or None,
        },
        "notebooks": [
            {"index": i, "name": nb.stem, "path": str(nb.resolve())}
            for i, nb in enumerate(notebooks)
        ],
        "skipped": skipped,
        "environment": environment_info(),
    }
    write_json(run_dir / "manifest.json", manifest)

    # > Record the skipped notebooks as results straight away, so the summary lists every
    # > notebook that exists rather than silently omitting the ones nobody attempted.
    for name in skipped:
        write_json(
            run_dir / "results" / f"{name}.json",
            {"name": name, "index": None, "status": "skipped", "finished_at": utcnow()},
        )
    return run_dir, manifest


def load_manifest(run_dir: Path) -> dict[str, Any]:
    """Read the manifest of `run_dir`, or exit if it is not a run directory."""
    manifest = read_json(run_dir / "manifest.json")
    if manifest is None:
        raise SystemExit(f"FATAL: no readable manifest.json in {run_dir}")
    return manifest


def parse_skip(raw: str) -> set[str]:
    """Split a comma-separated skip list; an empty string skips nothing."""
    return {part.strip() for part in raw.split(",") if part.strip()}


def resolve_scratch_base(manifest: dict[str, Any]) -> Path:
    """
    Decide where notebook working directories live.

    ORCA is I/O heavy, so its scratch belongs on node-local disk. `$SLURM_TMPDIR` is the
    site's own answer to that question wherever it is set, which is why it wins over the
    system temp directory.
    """
    configured = manifest["config"].get("scratch_base")
    if configured:
        return Path(configured)
    for var in ("SLURM_TMPDIR", "TMPDIR"):
        value = os.environ.get(var)
        if value:
            return Path(value)
    return Path(tempfile.gettempdir())


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                          INNERMOST WORKER: EXECUTE ONE NOTEBOOK
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def first_error(notebook: Any) -> dict[str, Any] | None:
    """
    Return information about the first cell that produced an error output.

    Parameters
    ----------
    notebook : nbformat.NotebookNode
        The notebook *after* execution; nbclient records the error into the cell outputs.

    Returns
    -------
    dict[str, Any] | None
        Error class, message, cell index, cell source and traceback, or None if no cell
        carries an error output.
    """
    for index, cell in enumerate(notebook.cells):
        for output in cell.get("outputs", []):
            if output.get("output_type") != "error":
                continue
            traceback = strip_ansi("\n".join(output.get("traceback", [])))
            return {
                "kind": output.get("ename"),
                "message": strip_ansi(str(output.get("evalue", "")))[:2000],
                "cell_index": index,
                "cell_source": "".join(cell.get("source", ""))[:1000],
                "traceback": traceback[-8000:],
            }
    return None


def execute_notebook(
    notebook_path: Path, workdir: Path, *, cell_timeout: int, kernel: str | None
) -> dict[str, Any]:
    """
    Execute one notebook in `workdir` and return its outcome.

    The executed copy is written to `workdir` whatever happens, because for a notebook the
    executed copy *is* the log: it carries every cell's output and the full traceback.

    Parameters
    ----------
    notebook_path : Path
        Notebook to execute. It is not modified.
    workdir : Path
        Working directory for the kernel. Everything the notebook writes lands here.
    cell_timeout : int
        Seconds a single cell may take before the kernel is killed.
    kernel : str | None
        Kernel name to force, or None to use whatever the notebook declares.

    Returns
    -------
    dict[str, Any]
        Keys `status` ("passed", "failed", "timeout" or "error"), `error`, `duration_s`
        and `executed_notebook`.
    """
    import nbformat
    from nbclient import NotebookClient
    from nbclient.exceptions import CellExecutionError, CellTimeoutError

    notebook = nbformat.read(notebook_path, as_version=4)

    # > A cell that times out never gets an error output, so the only way to say *which*
    # > cell hung is to remember which one was last started.
    running: dict[str, Any] = {"cell_index": None, "cell_source": ""}

    def on_cell_start(cell: Any = None, cell_index: int | None = None, **_: Any) -> None:
        running["cell_index"] = cell_index
        running["cell_source"] = "".join(cell.get("source", "") if cell else "")[:1000]

    client = NotebookClient(
        notebook,
        timeout=cell_timeout,
        resources={"metadata": {"path": str(workdir)}},
        allow_errors=False,
        record_timing=True,
        on_cell_start=on_cell_start,
        **({"kernel_name": kernel} if kernel else {}),
    )

    started = time.monotonic()
    status = "passed"
    error: dict[str, Any] | None = None
    try:
        client.execute()
    except CellTimeoutError as exc:
        status = "timeout"
        error = {
            "kind": "CellTimeoutError",
            "message": f"cell {running['cell_index']} exceeded the {cell_timeout}s cell timeout",
            "cell_index": running["cell_index"],
            "cell_source": running["cell_source"],
            "traceback": strip_ansi(str(exc))[-8000:],
        }
    except CellExecutionError:
        status = "failed"
        error = first_error(notebook) or {"kind": "CellExecutionError", "message": "unknown"}
    except Exception as exc:
        # > A dead kernel, a missing kernelspec, an unreadable notebook: everything that
        # > goes wrong around the notebook rather than inside it.
        status = "error"
        error = {
            "kind": type(exc).__name__,
            "message": strip_ansi(str(exc))[:2000],
            "cell_index": running["cell_index"],
        }

    executed = workdir / f"{notebook_path.stem}.executed.ipynb"
    try:
        nbformat.write(notebook, executed)
    except OSError as exc:
        print(f"WARNING: could not write {executed}: {exc}", file=sys.stderr)

    return {
        "status": status,
        "error": error,
        "duration_s": round(time.monotonic() - started, 1),
        "executed_notebook": str(executed),
    }


def cmd_exec(args: argparse.Namespace) -> int:
    """
    Execute one notebook and write its result next to it. The innermost layer.

    This runs as its own process so that the layer above can enforce a wall-clock limit on
    it and, more importantly, kill the whole process group -- a hung ORCA that outlives its
    notebook would otherwise keep burning the allocation.
    """
    manifest = load_manifest(args.run_dir)
    entry = manifest["notebooks"][args.index]
    workdir = args.workdir.resolve()
    config = manifest["config"]

    print(f"== {utcnow()} executing {entry['name']} on {socket.gethostname()}")
    print(f"== workdir: {workdir}")
    version_found = orca_version()
    print(f"== ORCA version: {version_found or 'NOT FOUND -- ORCA notebooks will fail'}")

    result = execute_notebook(
        Path(entry["path"]),
        workdir,
        cell_timeout=int(config["cell_timeout_s"]),
        kernel=config.get("kernel"),
    )
    result["orca_version"] = version_found
    write_json(workdir / "result.json", result)

    print(f"== {utcnow()} {entry['name']}: {result['status']} in {result['duration_s']}s")
    if result["error"]:
        print(f"== {result['error'].get('kind')}: {result['error'].get('message')}")
    return 0 if result["status"] == "passed" else 1


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                       SUPERVISOR: ONE NOTEBOOK, START TO FINISH
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


class Terminated(Exception):
    """Raised in place of a SIGTERM, so the notebook below can be shut down cleanly."""


# > Every worker currently running, so an interrupt can take their process trees with it
# > instead of orphaning an ORCA per notebook. Written from the local driver's threads.
_LIVE_WORKERS: set[subprocess.Popen[bytes]] = set()
_LIVE_WORKERS_LOCK = threading.Lock()


def catch_sigterm() -> None:
    """
    Turn SIGTERM into a `Terminated` exception, so a killed run can still clean up.

    SIGTERM is what SLURM sends at the wall-clock limit and on `scancel`, and what a
    `timeout` or a process supervisor sends locally. Left at its default disposition it
    kills this process outright, orphaning the notebook and its ORCA below it.
    """

    def on_sigterm(signum: int, frame: Any) -> None:
        raise Terminated(f"received signal {signum}")

    signal.signal(signal.SIGTERM, on_sigterm)


def terminate_group(process: subprocess.Popen[bytes]) -> None:
    """SIGTERM the process group of `process`, then SIGKILL whatever survives."""
    for sig, wait in ((signal.SIGTERM, KILL_GRACE_S), (signal.SIGKILL, 10)):
        try:
            os.killpg(os.getpgid(process.pid), sig)
        except (ProcessLookupError, PermissionError):
            process.kill()
        try:
            process.wait(timeout=wait)
            return
        except subprocess.TimeoutExpired:
            continue


def terminate_live_workers() -> None:
    """Kill every running worker's process tree. Called when the run is interrupted."""
    with _LIVE_WORKERS_LOCK:
        workers = list(_LIVE_WORKERS)
    for process in workers:
        terminate_group(process)


def keep_artifacts(status: str, policy: str) -> bool:
    """Decide whether the working directory of a notebook with `status` is worth keeping."""
    if policy == "all":
        return True
    if policy == "none":
        return False
    return status != "passed"


def run_one(run_dir: Path, index: int, *, quiet: bool = False) -> dict[str, Any]:
    """
    Run notebook `index` of the run in `run_dir` and record the result.

    Supervises the actual execution from the outside: it owns the scratch directory, the
    wall-clock limit and the artifact retention, and it guarantees a result file even when
    the worker below it dies without writing one.

    Parameters
    ----------
    run_dir : Path
        Run directory holding `manifest.json`.
    index : int
        Position of the notebook in the manifest.
    quiet : bool
        Suppress the one-line progress messages (the local driver prints its own).

    Returns
    -------
    dict[str, Any]
        The result record, as written to `<run_dir>/results/<name>.json`.
    """
    manifest = load_manifest(run_dir)
    config = manifest["config"]
    entry = manifest["notebooks"][index]
    name = entry["name"]

    workdir = resolve_scratch_base(manifest) / f"opi-nb-{manifest['run_id']}" / name
    shutil.rmtree(workdir, ignore_errors=True)
    (workdir / "tmp").mkdir(parents=True, exist_ok=True)

    log_path = run_dir / "logs" / f"{name}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    timeout = int(config["notebook_timeout_s"])
    command = [
        sys.executable,
        str(manifest.get("script") or SCRIPT_PATH),
        "exec",
        str(run_dir),
        str(index),
        "--workdir",
        str(workdir),
    ]
    # > Keep the notebook's stray temporary files on the same (node-local) disk as its
    # > working directory, so cleaning up the working directory cleans up everything.
    env = os.environ | {"TMPDIR": str(workdir / "tmp")}

    if not quiet:
        print(f"-- {name}: starting (log: {log_path})", flush=True)

    started_at = utcnow()
    started = time.monotonic()
    with log_path.open("wb") as log:
        # > `start_new_session` puts the worker, its kernel and any ORCA/mpirun below it
        # > into one process group, so the timeout below can kill the entire tree.
        process = subprocess.Popen(
            command,
            cwd=workdir,
            stdout=log,
            stderr=subprocess.STDOUT,
            env=env,
            start_new_session=True,
        )
        with _LIVE_WORKERS_LOCK:
            _LIVE_WORKERS.add(process)
        timed_out = False
        aborted: BaseException | None = None
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            terminate_group(process)
            log.write(f"\n[killed: exceeded the {timeout}s notebook timeout]\n".encode())
        except BaseException as exc:
            # > Ctrl-C, or SLURM's SIGTERM at the job's wall-clock limit. Take the notebook
            # > and its ORCA down with us rather than leaving them behind, but still write
            # > a result first -- "this one was cut short" is worth knowing afterwards.
            aborted = exc
            terminate_group(process)
            log.write(f"\n[aborted: {type(exc).__name__}]\n".encode())
        finally:
            with _LIVE_WORKERS_LOCK:
                _LIVE_WORKERS.discard(process)

    worker_result = read_json(workdir / "result.json") or {}
    if aborted is not None:
        status = "error"
        error = {
            "kind": type(aborted).__name__,
            "message": "the run was interrupted before this notebook finished",
        }
    elif timed_out:
        status = "timeout"
        error = {"kind": "NotebookTimeout", "message": f"exceeded the {timeout}s limit"}
    elif worker_result:
        status = str(worker_result.get("status", "error"))
        error = worker_result.get("error")
    else:
        # > The worker died without writing a result: an OOM kill, a SIGTERM from SLURM at
        # > the wall-clock limit, or a crash before it could report anything.
        status = "error"
        error = {
            "kind": "WorkerDied",
            "message": f"worker exited with {process.returncode} without writing a result",
        }

    result: dict[str, Any] = {
        "name": name,
        "index": index,
        "path": entry["path"],
        "status": status,
        "error": error,
        "started_at": started_at,
        "finished_at": utcnow(),
        "duration_s": round(time.monotonic() - started, 1),
        "returncode": process.returncode,
        "orca_version": worker_result.get("orca_version"),
        "workdir": str(workdir),
        "log": str(log_path),
        "host": socket.gethostname(),
        "slurm": slurm_info(),
        "artifacts": None,
        "executed_notebook": None,
    }

    # > Retention runs on a best-effort basis: a full disk or an unreadable scratch file
    # > must cost us the artifacts, never the result record itself.
    try:
        # > The executed notebook is the most useful single artifact there is, so it is
        # > kept for every notebook regardless of the retention policy.
        executed = workdir / f"{name}.executed.ipynb"
        if executed.is_file():
            destination = run_dir / "executed" / f"{name}.ipynb"
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(executed, destination)
            result["executed_notebook"] = str(destination)

        if keep_artifacts(status, str(config["keep"])):
            destination = run_dir / "artifacts" / name
            shutil.rmtree(destination, ignore_errors=True)
            shutil.copytree(workdir, destination, ignore=ARTIFACT_IGNORE, dirs_exist_ok=True)
            result["artifacts"] = str(destination)
    except OSError as exc:
        result["retention_error"] = str(exc)
        print(f"WARNING: could not keep the artifacts of {name}: {exc}", file=sys.stderr)

    shutil.rmtree(workdir, ignore_errors=True)
    write_json(run_dir / "results" / f"{name}.json", result)

    if not quiet:
        print(f"-- {name}: {status} in {result['duration_s']}s", flush=True)
    if aborted is not None:
        raise aborted
    return result


def cmd_task(args: argparse.Namespace) -> int:
    """
    Run a single notebook of an existing run. This is what each array task calls.

    SIGTERM is turned into an exception because that is how SLURM announces the wall-clock
    limit (and `scancel`): the notebook then gets shut down and recorded on the way out,
    instead of the task disappearing and leaving a `missing` entry behind.
    """
    manifest = load_manifest(args.run_dir)
    count = len(manifest["notebooks"])
    if not 0 <= args.index < count:
        raise SystemExit(f"FATAL: task index {args.index} out of range (run has {count})")

    catch_sigterm()
    try:
        result = run_one(args.run_dir, args.index)
    except Terminated as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 143
    return 0 if result["status"] == "passed" else 1


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                                     LOCAL BACKEND
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def cmd_local(args: argparse.Namespace) -> int:
    """Execute the selected notebooks on this machine and print a report."""
    require_nbclient()
    catch_sigterm()
    run_dir, manifest = create_run(args, backend="local")
    notebooks = manifest["notebooks"]

    print(f"run directory: {run_dir}")
    print(f"notebooks:     {len(notebooks)} to run, {len(manifest['skipped'])} skipped")
    print(f"ORCA:          {manifest['environment']['versions']['orca'] or 'NOT FOUND'}")
    if args.jobs > 1:
        # > Most notebooks `pip install` into the running environment; doing that from
        # > several processes at once is how you get a half-installed package.
        print(
            f"WARNING: -j {args.jobs}: the notebooks install packages into this "
            "environment, and concurrent installs can corrupt it",
        )
    print()

    done = 0
    total = len(notebooks)

    def execute(index: int) -> dict[str, Any]:
        nonlocal done
        try:
            result = run_one(run_dir, index, quiet=True)
        except Exception as exc:
            # > A notebook that breaks its own supervisor (unwritable scratch, a full disk)
            # > must not take the rest of the run down with it.
            name = notebooks[index]["name"]
            result = {
                "name": name,
                "index": index,
                "path": notebooks[index]["path"],
                "status": "error",
                "error": {"kind": type(exc).__name__, "message": str(exc)[:2000]},
                "duration_s": None,
                "finished_at": utcnow(),
            }
            write_json(run_dir / "results" / f"{name}.json", result)

        done += 1
        duration = result.get("duration_s")
        elapsed = f"{duration:>8.1f}s" if isinstance(duration, (int, float)) else " " * 9
        detail = "" if result["status"] == "passed" else f"  {error_line(result)}"
        print(
            f"[{done}/{total}] {result['name']:<32} {result['status']:<8}{elapsed}{detail}",
            flush=True,
        )
        return result

    try:
        if args.jobs > 1:
            pool = ThreadPoolExecutor(max_workers=args.jobs)
            try:
                list(pool.map(execute, range(total)))
            except (KeyboardInterrupt, Terminated):
                # > The worker threads are blocked on their notebooks and will not see this,
                # > so kill the notebooks: otherwise the shutdown below waits for all of
                # > them to finish, which is the opposite of what Ctrl-C asked for.
                terminate_live_workers()
                raise
            finally:
                pool.shutdown(wait=True)
        else:
            for index in range(total):
                execute(index)
    except (KeyboardInterrupt, Terminated):
        terminate_live_workers()
        print("\ninterrupted; reporting what finished so far", file=sys.stderr)

    print()
    return report(run_dir)


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                                     SLURM BACKEND
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def job_script(args: argparse.Namespace, run_dir: Path, count: int) -> str:
    """
    Render the sbatch script for a run: a job array with one task per notebook.

    Everything is baked into the script rather than passed on the `sbatch` command line,
    so `<run-dir>/job.sh` is a complete, re-submittable record of what was queued.
    """
    directives = [
        f"#SBATCH --job-name={args.job_name}",
        f"#SBATCH --array=0-{count - 1}%{args.max_parallel}",
        f"#SBATCH --output={run_dir}/logs/slurm-%A_%a.out",
        "#SBATCH --nodes=1",
        "#SBATCH --ntasks=1",
        f"#SBATCH --cpus-per-task={args.cpus_per_task}",
        f"#SBATCH --mem={args.mem}",
        f"#SBATCH --time={args.time}",
        f"#SBATCH --export={args.export}",
    ]
    if args.partition:
        directives.append(f"#SBATCH --partition={args.partition}")
    if args.account:
        directives.append(f"#SBATCH --account={args.account}")
    if args.qos:
        directives.append(f"#SBATCH --qos={args.qos}")
    if args.mail:
        directives.append(f"#SBATCH --mail-user={args.mail}")
        directives.append("#SBATCH --mail-type=FAIL,TIME_LIMIT")
    directives.extend(f"#SBATCH {extra}" for extra in args.sbatch_arg)

    preamble = ""
    if args.preamble:
        preamble = (
            f"# ---- from {args.preamble} ----\n"
            f"{Path(args.preamble).read_text().rstrip()}\n"
            "# ---- end preamble ----\n"
        )

    header = "\n".join(directives)
    return f"""#!/bin/bash
{header}
#
# Generated by {SCRIPT_PATH} on {utcnow()}.
# One array task per notebook; the mapping from task id to notebook is in
#   {run_dir}/manifest.json
# Re-run a single notebook by hand with:
#   {sys.executable} {SCRIPT_PATH} task {run_dir} <index>

set -euo pipefail

cd {REPO_ROOT}
{preamble}
exec {sys.executable} {SCRIPT_PATH} task {run_dir} "$SLURM_ARRAY_TASK_ID"
"""


def cmd_slurm(args: argparse.Namespace) -> int:
    """Submit the selected notebooks as a job array and, with --wait, follow it."""
    if args.preamble and not args.preamble.is_file():
        raise SystemExit(f"FATAL: no preamble file at {args.preamble}")
    # > The tasks run this very interpreter (by absolute path, with --export=ALL), so a
    # > notebook stack missing here is 19 identical failures an hour from now.
    try:
        require_nbclient()
    except SystemExit as exc:
        print(f"WARNING: {exc}\nThe array tasks use this same interpreter.\n")

    run_dir, manifest = create_run(args, backend="slurm")
    count = len(manifest["notebooks"])

    script_path = run_dir / "job.sh"
    script_path.write_text(job_script(args, run_dir, count))
    script_path.chmod(0o755)

    command = ["sbatch", "--parsable", str(script_path)]
    print(f"run directory: {run_dir}")
    print(f"job script:    {script_path}")
    print(f"notebooks:     {count} to run, {len(manifest['skipped'])} skipped")
    print(f"command:       {' '.join(command)}")

    if args.dry_run:
        print("\n--dry-run: nothing submitted. The run directory is ready, so this script")
        print(f"can be submitted by hand once it looks right:\n    sbatch {script_path}\n")
        print(script_path.read_text())
        return 0

    if shutil.which("sbatch") is None:
        raise SystemExit("FATAL: 'sbatch' not on PATH -- is this a submit host?")

    try:
        proc = subprocess.run(command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f"FATAL: sbatch failed ({exc.returncode}): {exc.stderr.strip()}")

    # > --parsable prints "<jobid>" or "<jobid>;<cluster>".
    job_id = proc.stdout.strip().split(";")[0]
    manifest["slurm"] = {
        "job_id": job_id,
        "array": f"0-{count - 1}%{args.max_parallel}",
        "script": str(script_path),
        "submitted_at": utcnow(),
    }
    write_json(run_dir / "manifest.json", manifest)

    print(f"submitted:     job {job_id} ({count} array tasks)")
    print(f"\nfollow with:   {SCRIPT_PATH} report {run_dir}")

    if not args.wait:
        return 0
    return wait_for_job(job_id, run_dir, args.poll_interval)


def squeue_states(job_id: str) -> list[str] | None:
    """
    Return the states of the tasks of `job_id`, or None if squeue could not be asked.

    An empty list means the job has left the queue -- which is the only reliable
    "finished" signal, since a finished array job disappears from `squeue` entirely.
    """
    try:
        proc = subprocess.run(
            ["squeue", "-h", "-j", job_id, "-o", "%T"], capture_output=True, text=True, timeout=60
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        # > "Invalid job id specified" also lands here once the job has been purged.
        return [] if "Invalid job id" in proc.stderr else None
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def wait_for_job(job_id: str, run_dir: Path, poll_interval: int) -> int:
    """
    Block until job `job_id` has left the queue, then report.

    Two consecutive empty `squeue` answers are required before the job is called finished:
    a single one can be a controller hiccup, and giving up early would report a run as
    incomplete while its tasks are still writing results.
    """
    print(f"\nwaiting for job {job_id} (polling every {poll_interval}s; Ctrl-C is safe)")
    empty_polls = 0
    unavailable_polls = 0
    try:
        while empty_polls < 2:
            states = squeue_states(job_id)
            if states is None:
                unavailable_polls += 1
                if unavailable_polls > MAX_SQUEUE_FAILURES:
                    print(f"  squeue unusable for {unavailable_polls} polls; giving up on waiting")
                    print(
                        f"  the job keeps running; report later with: {SCRIPT_PATH} report {run_dir}"
                    )
                    return report(run_dir)
                print(f"  squeue unavailable ({unavailable_polls}); retrying")
            elif not states:
                unavailable_polls = 0
                empty_polls += 1
            else:
                empty_polls = 0
                unavailable_polls = 0
                counts = {state: states.count(state) for state in sorted(set(states))}
                queued = ", ".join(f"{n} {s.lower()}" for s, n in counts.items())
                finished = len(list((run_dir / "results").glob("*.json")))
                print(f"  [{utcnow()}] {queued}; {finished} results written", flush=True)
            if empty_polls < 2:
                time.sleep(poll_interval)
    except KeyboardInterrupt:
        print("\nstopped waiting; the job keeps running. Report later with:")
        print(f"  {SCRIPT_PATH} report {run_dir}")
        return 0

    print()
    return report(run_dir)


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                                   SUMMARY AND REPORT
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def error_line(result: dict[str, Any]) -> str:
    """Render the error of a result as a single line, empty if there is none."""
    error = result.get("error")
    if not error:
        return ""
    message = " ".join(str(error.get("message", "")).split())[:120]
    return f"{error.get('kind')}: {message}" if message else str(error.get("kind"))


def build_summary(run_dir: Path) -> dict[str, Any]:
    """
    Merge the manifest and every per-notebook result into one summary dictionary.

    A notebook with no result file is reported as `missing`: either its task has not run
    yet, or it was killed so hard that even the supervisor could not write a record.
    """
    manifest = load_manifest(run_dir)
    results = []
    for entry in manifest["notebooks"]:
        result = read_json(run_dir / "results" / f"{entry['name']}.json")
        results.append(
            result
            or {
                "name": entry["name"],
                "index": entry["index"],
                "path": entry["path"],
                "status": "missing",
                "error": None,
                "duration_s": None,
            }
        )
    for name in manifest["skipped"]:
        result = read_json(run_dir / "results" / f"{name}.json")
        if result:
            results.append(result)

    totals = {"total": len(results)}
    for status in ("passed", "failed", "timeout", "error", "skipped", "missing"):
        totals[status] = sum(1 for r in results if r.get("status") == status)

    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": manifest["run_id"],
        "run_dir": str(run_dir),
        "backend": manifest["backend"],
        "status": "completed" if totals["missing"] == 0 else "incomplete",
        "created_at": manifest["created_at"],
        "reported_at": utcnow(),
        "config": manifest["config"],
        "environment": manifest["environment"],
        "slurm": manifest.get("slurm"),
        "totals": totals,
        "notebooks": sorted(results, key=lambda r: str(r.get("name"))),
    }


def print_report(summary: dict[str, Any]) -> None:
    """Print the human-readable version of a summary."""
    print(f"run {summary['run_id']} ({summary['backend']}, {summary['status']})")
    print(f"  {summary['run_dir']}")
    versions = summary["environment"]["versions"]
    commit = summary["environment"]["git"].get("commit") or "?"
    print(f"  opi {versions['opi']}  orca {versions['orca']}  commit {commit[:12]}")
    print()

    width = max((len(str(r.get("name", ""))) for r in summary["notebooks"]), default=20)
    for result in summary["notebooks"]:
        duration = result.get("duration_s")
        elapsed = f"{duration:>8.1f}s" if isinstance(duration, (int, float)) else " " * 9
        detail = error_line(result)
        print(
            f"  {str(result.get('name')):<{width}}  {str(result.get('status')):<8}{elapsed}"
            f"{'  ' + detail if detail else ''}"
        )

    totals = summary["totals"]
    parts = [f"{totals[k]} {k}" for k in sorted(totals) if k != "total" and totals[k]]
    print(f"\n  {totals['total']} notebooks: {', '.join(parts) or 'nothing ran'}")

    failed = [r for r in summary["notebooks"] if r.get("status") in ("failed", "timeout", "error")]
    if failed:
        print("\n  post-mortem:")
        for result in failed:
            print(f"    {result['name']}: {result.get('log')}")
            if result.get("artifacts"):
                print(f"      artifacts: {result['artifacts']}")


def report(run_dir: Path) -> int:
    """Write `summary.json` for `run_dir`, print the report, and return an exit code."""
    summary = build_summary(run_dir)
    write_json(run_dir / "summary.json", summary)
    print_report(summary)
    print(f"\n  summary: {run_dir / 'summary.json'}")

    totals = summary["totals"]
    return 1 if any(totals[k] for k in ("failed", "timeout", "error", "missing")) else 0


def cmd_report(args: argparse.Namespace) -> int:
    """Refresh and print the summary of an existing run."""
    return report(args.run_dir.resolve())


def cmd_list(args: argparse.Namespace) -> int:
    """Print which notebooks would run and which would be skipped."""
    skip = parse_skip(args.skip)
    notebooks, skipped = select_notebooks(args.notebooks_dir, args.notebooks, skip)
    for notebook in notebooks:
        print(f"  run   {notebook.stem}")
    for name in skipped:
        print(f"  skip  {name}")
    print(f"\n{len(notebooks)} to run, {len(skipped)} skipped, from {args.notebooks_dir}")
    return 0


def require_nbclient() -> None:
    """Fail fast, with the fix, if the notebook execution stack is not installed."""
    try:
        import nbclient  # noqa: F401
        import nbformat  # noqa: F401
    except ImportError as exc:
        raise SystemExit(
            f"FATAL: {exc.name} is not installed.\n"
            "The notebooks need the 'notebooks' dependency group:\n"
            "    uv sync --group notebooks"
        )


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                                    COMMAND LINE
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def build_parser() -> argparse.ArgumentParser:
    """Assemble the command line parser."""
    parser = argparse.ArgumentParser(
        prog=SCRIPT_PATH.name,
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # > Shared by every command that selects notebooks.
    selection = argparse.ArgumentParser(add_help=False)
    selection.add_argument(
        "notebooks",
        nargs="*",
        metavar="NOTEBOOK",
        help="Notebook names or glob patterns; default: all of them. Naming a notebook "
        "explicitly overrides --skip.",
    )
    selection.add_argument(
        "--notebooks-dir",
        type=Path,
        default=Path(os.environ.get("OPI_NB_DIR", DEFAULT_NOTEBOOKS_DIR)),
        help="Directory holding the notebooks (default: %(default)s).",
    )
    selection.add_argument(
        "--skip",
        default=os.environ.get("OPI_NB_SKIP", ",".join(DEFAULT_SKIP)),
        metavar="A,B,C",
        help="Comma-separated notebooks to skip; empty string skips none (default: %(default)s).",
    )

    # > Shared by the two commands that actually start a run.
    execution = argparse.ArgumentParser(add_help=False, parents=[selection])
    execution.add_argument(
        "--run-dir",
        type=Path,
        default=None,
        help=f"Where to put results and logs (default: {DEFAULT_RUNS_DIR}/<timestamp>).",
    )
    execution.add_argument(
        "--cell-timeout",
        type=int,
        default=DEFAULT_CELL_TIMEOUT,
        metavar="S",
        help="Seconds a single cell may take (default: %(default)s).",
    )
    execution.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_NOTEBOOK_TIMEOUT,
        metavar="S",
        help="Seconds a whole notebook may take before its process tree is killed "
        "(default: %(default)s).",
    )
    execution.add_argument(
        "--scratch-base",
        type=Path,
        default=os.environ.get("OPI_NB_SCRATCH") or None,
        metavar="DIR",
        help="Parent of the notebook working directories; keep this on node-local disk "
        "(default: $SLURM_TMPDIR, else $TMPDIR, else the system temp directory).",
    )
    execution.add_argument(
        "--keep",
        choices=("all", "failed", "none"),
        default="failed",
        help="Which working directories to copy into the run directory (default: %(default)s). "
        "The executed notebook is always kept.",
    )
    execution.add_argument(
        "--kernel",
        default="python3",
        metavar="NAME",
        help="Jupyter kernel to force; empty string uses what each notebook declares "
        "(default: %(default)s).",
    )

    list_parser = subparsers.add_parser(
        "list", parents=[selection], help="Show which notebooks would run."
    )
    list_parser.set_defaults(func=cmd_list)

    local_parser = subparsers.add_parser(
        "local", parents=[execution], help="Execute the notebooks on this machine."
    )
    local_parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=1,
        metavar="N",
        help="Notebooks to execute at once (default: %(default)s). Above 1 the notebooks "
        "install packages into this environment concurrently, which is risky.",
    )
    local_parser.set_defaults(func=cmd_local)

    slurm_parser = subparsers.add_parser(
        "slurm", parents=[execution], help="Submit the notebooks as a SLURM job array."
    )
    slurm_parser.add_argument("--job-name", default="opi-notebooks", help="(default: %(default)s)")
    slurm_parser.add_argument(
        "--partition", default=os.environ.get("OPI_NB_PARTITION"), help="SLURM partition."
    )
    slurm_parser.add_argument(
        "--account", default=os.environ.get("OPI_NB_ACCOUNT"), help="SLURM account."
    )
    slurm_parser.add_argument("--qos", default=None, help="SLURM QOS.")
    slurm_parser.add_argument(
        "--time",
        default="12:00:00",
        metavar="HH:MM:SS",
        help="Wall-clock limit PER NOTEBOOK (default: %(default)s).",
    )
    slurm_parser.add_argument(
        "--cpus-per-task",
        type=int,
        default=8,
        metavar="N",
        help="Cores per notebook; the largest `ncores` any notebook asks for is 8 "
        "(default: %(default)s).",
    )
    slurm_parser.add_argument(
        "--mem", default="32G", help="Memory per notebook (default: %(default)s)."
    )
    slurm_parser.add_argument(
        "--max-parallel",
        type=int,
        default=DEFAULT_MAX_PARALLEL,
        metavar="N",
        help="Array throttle: tasks running at once (default: %(default)s).",
    )
    slurm_parser.add_argument(
        "--mail",
        default=None,
        metavar="ADDRESS",
        help="Mail address for FAIL and TIME_LIMIT notifications.",
    )
    slurm_parser.add_argument(
        "--export",
        default="ALL",
        metavar="SPEC",
        help="sbatch --export value. The default hands the tasks the environment you "
        "submit from, including the active virtualenv (default: %(default)s).",
    )
    slurm_parser.add_argument(
        "--preamble",
        type=Path,
        default=None,
        metavar="FILE",
        help="Shell snippet inserted into the job script before the notebook runs: "
        "`module load`, activating a venv, exporting OPI_ORCA.",
    )
    slurm_parser.add_argument(
        "--sbatch-arg",
        action="append",
        default=[],
        metavar="ARG",
        help="Extra #SBATCH directive, e.g. --sbatch-arg=--constraint=avx2. Repeatable.",
    )
    slurm_parser.add_argument(
        "--wait", action="store_true", help="Block until the array finishes, then report."
    )
    slurm_parser.add_argument(
        "--poll-interval",
        type=int,
        default=DEFAULT_POLL_INTERVAL,
        metavar="S",
        help="Seconds between squeue polls while waiting (default: %(default)s).",
    )
    slurm_parser.add_argument(
        "--dry-run", action="store_true", help="Write the job script and print it; do not submit."
    )
    slurm_parser.set_defaults(func=cmd_slurm)

    report_parser = subparsers.add_parser("report", help="Print the summary of a run.")
    report_parser.add_argument("run_dir", type=Path, metavar="RUN_DIR")
    report_parser.set_defaults(func=cmd_report)

    task_parser = subparsers.add_parser("task", help="Execute one notebook of an existing run.")
    task_parser.add_argument("run_dir", type=Path, metavar="RUN_DIR")
    task_parser.add_argument("index", type=int, metavar="INDEX")
    task_parser.set_defaults(func=cmd_task)

    exec_parser = subparsers.add_parser("exec", help=argparse.SUPPRESS)
    exec_parser.add_argument("run_dir", type=Path)
    exec_parser.add_argument("index", type=int)
    exec_parser.add_argument("--workdir", type=Path, required=True)
    exec_parser.set_defaults(func=cmd_exec)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Parse the command line and dispatch."""
    # > Unattended runs redirect stdout into a log file, where Python would otherwise hold
    # > every progress line in a buffer until the run is over.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(line_buffering=True)

    args = build_parser().parse_args(argv)
    result: int = args.func(args)
    return result


if __name__ == "__main__":
    sys.exit(main())
