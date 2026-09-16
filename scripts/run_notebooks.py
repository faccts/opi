#!/usr/bin/env python3
"""
Execute a list of notebooks, one after another.

Every notebook is handed to `run_notebook.py` in a process of its own, so one that
crashes its kernel -- or hangs until it is killed -- costs that notebook and not the rest
of the run. Output appears as it happens; at the end, one line per notebook says how it
went, and the exit status says whether anything went wrong.

They run one at a time on purpose: most of the documentation notebooks `pip install` into
the environment they run in, and concurrent installs into one environment corrupt it.

Examples
--------
::

    scripts/run_notebooks.py                  # the whitelist below
    scripts/run_notebooks.py how_to_opi led   # by name, whitelisted or not
    scripts/run_notebooks.py 'extrapolate_*'  # by glob
    scripts/run_notebooks.py '*'              # every notebook there is
    scripts/run_notebooks.py --list           # what would run?

Exit status is 0 if every notebook ran, and 1 otherwise.
"""

from __future__ import annotations

import argparse
import contextlib
import fnmatch
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

from run_notebook import DEFAULT_TIMEOUT, NOTEBOOKS_DIR

RUNNER = Path(__file__).resolve().parent / "run_notebook.py"

# > The notebooks a plain run works through, in this order. This list is the one place
# > that decides what "all of them" means: a notebook that cannot run here -- one that
# > needs a GPU, a licence or a machine with more patience -- is taken off it. Naming a
# > notebook on the command line runs it whether it is on this list or not.
WHITELIST = (
    "adld_dftd4",
    "adld_hfld",
    "atomic_fukui_indices",
    "covaled_ethane",
    "how_to_opi",
    "ir_spectrum",
    "led",
    "ml_properties",
    "moplot",
    "redox",
    "wb97m2",
)

# > Grace beyond a notebook's own budget before this script ends it, in seconds.
GRACE = 120
# > How long a notebook gets to clean up after being asked to stop, in seconds.
TERM_GRACE = 30


def whitelisted() -> list[Path]:
    """Resolve `WHITELIST` to paths, refusing a name that is not there to be run."""
    notebooks = []
    for name in WHITELIST:
        notebook = (NOTEBOOKS_DIR / name).with_suffix(".ipynb")
        if not notebook.is_file():
            raise SystemExit(f"error: whitelisted notebook does not exist: {name}")
        notebooks.append(notebook)
    return notebooks


def select(patterns: list[str]) -> list[Path]:
    """
    Work out which notebooks to run.

    Parameters
    ----------
    patterns : list[str]
        Paths to notebooks, or names and globs matched against the stems of the
        notebooks in `NOTEBOOKS_DIR`. Empty means the whitelist.
    """
    if not patterns:
        return whitelisted()

    available = sorted(NOTEBOOKS_DIR.glob("*.ipynb"))

    selected: list[Path] = []
    for pattern in patterns:
        path = Path(pattern)
        if path.is_file():
            selected.append(path.resolve())
            continue
        matches = [notebook for notebook in available if fnmatch.fnmatch(notebook.stem, pattern)]
        if not matches:
            raise SystemExit(f"error: no notebook matches: {pattern}")
        selected += matches
    # > Keep the order they were asked for, but run nothing twice.
    return list(dict.fromkeys(selected))


def stop(process: subprocess.Popen[bytes]) -> None:
    """
    End a notebook that overran, along with everything it started.

    The runner is asked to stop first, so that it can clean up after itself; whatever is
    left of its process group afterwards -- a kernel, an ORCA -- is killed outright.
    """
    # > SIGTERM to the runner alone: it then shuts its own kernel down in order and
    # > removes its temporary directory, which a signalled kernel would not let it do.
    process.terminate()
    with contextlib.suppress(subprocess.TimeoutExpired):
        process.wait(timeout=TERM_GRACE)
    # > Whatever is left of the group -- a kernel, an ORCA -- does not get a say.
    with contextlib.suppress(ProcessLookupError):
        os.killpg(process.pid, signal.SIGKILL)
    process.wait()


def run(notebook: Path, limit: int, options: list[str]) -> tuple[str, float]:
    """
    Execute one notebook in a process of its own.

    Parameters
    ----------
    notebook : Path
        Notebook to execute.
    limit : int
        Wall-clock limit of the notebook itself, in seconds. This script waits `GRACE`
        seconds longer than that before stepping in.
    options : list[str]
        Options to pass on to `run_notebook.py`.

    Returns
    -------
    tuple[str, float]
        The status of the notebook, and how long it ran for in seconds.
    """
    start = time.monotonic()
    # > A session of its own, so the whole group can be signalled later if need be.
    process = subprocess.Popen(
        [sys.executable, str(RUNNER), str(notebook), *options], start_new_session=True
    )
    try:
        returncode = process.wait(timeout=limit + GRACE)
    except subprocess.TimeoutExpired:
        stop(process)
        print(
            f"\nSTOPPED: {notebook.name} outlasted its {limit} s "
            f"by more than the {GRACE} s of grace it is given.",
            file=sys.stderr,
            flush=True,
        )
        return "KILLED", time.monotonic() - start
    except KeyboardInterrupt:
        # > Ctrl-C does not reach the child by itself: it is in its own session.
        stop(process)
        raise
    return ("OK" if returncode == 0 else "FAILED"), time.monotonic() - start


def format_duration(seconds: float) -> str:
    """Render a duration in whichever unit keeps it readable."""
    if seconds < 60:
        return f"{seconds:.1f} s"
    minutes, second = divmod(int(seconds), 60)
    hour, minute = divmod(minutes, 60)
    return f"{hour}h {minute:02d}m" if hour else f"{minute}m {second:02d}s"


def report(results: list[tuple[Path, str, float]], total: float) -> None:
    """Print one line per notebook, and a count of how they ended."""
    width = max(len(notebook.stem) for notebook, _, _ in results)
    print("\n" + "=" * 72)
    for notebook, status, duration in results:
        print(f"  {status:<8} {notebook.stem:<{width}}  {format_duration(duration):>8}")
    print("-" * 72)

    counts = [
        f"{sum(1 for _, status, _ in results if status == name)} {label}"
        for name, label in (("OK", "ok"), ("FAILED", "failed"), ("KILLED", "killed"))
    ]
    print(f"  {len(results)} notebooks: {', '.join(counts)} -- {format_duration(total)} total")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "notebooks",
        nargs="*",
        help="paths, names or globs; without any, the whitelist at the top of this script runs",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="print the notebooks that would run, and stop",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        help="wall-clock limit for a whole notebook, in seconds",
    )
    parser.add_argument(
        "-c",
        "--cell-timeout",
        type=int,
        help="wall-clock limit for a single cell, in seconds",
    )
    args = parser.parse_args(argv)

    notebooks = select(args.notebooks)
    if args.list:
        print("\n".join(notebook.stem for notebook in notebooks))
        return 0

    # > The limits belong to `run_notebook.py`; only what was asked for is passed on.
    options: list[str] = []
    if args.timeout is not None:
        options += ["--timeout", str(args.timeout)]
    if args.cell_timeout is not None:
        options += ["--cell-timeout", str(args.cell_timeout)]
    limit = args.timeout if args.timeout is not None else DEFAULT_TIMEOUT

    results: list[tuple[Path, str, float]] = []
    start = time.monotonic()
    for index, notebook in enumerate(notebooks, start=1):
        print(f"\n===== [{index}/{len(notebooks)}] {notebook.stem} =====", flush=True)
        status, duration = run(notebook, limit, options)
        results.append((notebook, status, duration))

    report(results, time.monotonic() - start)
    return 0 if all(status == "OK" for _, status, _ in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
