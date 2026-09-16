#!/usr/bin/env python3
"""
Execute one Jupyter notebook headlessly and report whether it ran to the end.

The notebook runs in a temporary directory -- so nothing is written next to the notebook
sources -- with a non-interactive matplotlib backend, in whatever Python environment this
script runs in. Everything the notebook writes is discarded with that directory
afterwards: the only thing checked here is that every cell terminated normally.

A notebook gets 45 minutes of wall clock in total, and no single cell may run longer
than 30 minutes. Whichever limit is reached first ends the run.

Examples
--------
::

    scripts/run_notebook.py docs/contents/notebooks/how_to_opi.ipynb
    scripts/run_notebook.py how_to_opi --timeout 7200 --cell-timeout 3600

Exit status is 0 if every cell ran, and 1 if one did not.
"""

from __future__ import annotations

import argparse
import os
import signal
import sys
import tempfile
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError, CellTimeoutError, DeadKernelError
from nbformat import NotebookNode

# > A notebook can be named by its path, or -- for the documentation ones -- by its stem.
# > `notebooks` is a symlink next to this script, so where they live is decided there.
NOTEBOOKS_DIR = (Path(__file__).resolve().parent / "notebooks").resolve()


class NotebookTimeout(Exception):
    """Raised when a notebook runs out of its wall-clock budget."""


# > Wall-clock limit for a whole notebook, in seconds.
DEFAULT_TIMEOUT = 60 * 60
# > Wall-clock limit for a single cell, in seconds.
DEFAULT_CELL_TIMEOUT = 45 * 60


def resolve_notebook(name: str) -> Path:
    """
    Turn a command line argument into the path of a notebook.

    Parameters
    ----------
    name : str
        Path to a notebook, or the name of a notebook in `NOTEBOOKS_DIR`.
    """
    candidates = (Path(name), (NOTEBOOKS_DIR / name).with_suffix(".ipynb"))
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    raise SystemExit(f"error: no such notebook: {name}")


def execute(notebook: Path, workdir: Path, timeout: int, cell_timeout: int, kernel: str) -> None:
    """
    Execute a notebook in `workdir`, printing one line per code cell as it goes.

    Raises whatever nbclient raises when a cell does not terminate normally, including
    when it runs into either of the two limits.

    Parameters
    ----------
    notebook : Path
        Notebook to execute.
    workdir : Path
        Working directory of the kernel.
    timeout : int
        Wall-clock limit for the notebook as a whole, in seconds.
    cell_timeout : int
        Wall-clock limit for a single cell, in seconds.
    kernel : str
        Name of the Jupyter kernel to run the notebook with.
    """
    nb = nbformat.read(notebook, as_version=4)
    n_code_cells = sum(1 for cell in nb.cells if cell.cell_type == "code" and cell.source.strip())
    started = 0
    cell_start = 0.0
    # > A cell is announced before it runs, and its line stays open until it is done.
    line_open = False

    def report_start(cell: NotebookNode, cell_index: int) -> None:
        nonlocal started, cell_start, line_open
        started += 1
        cell_start = time.monotonic()
        first_line = cell.source.strip().splitlines()[0]
        print(f"  [{started}/{n_code_cells}] {first_line[:70]}", end="", flush=True)
        line_open = True

    def report_end(cell: NotebookNode, cell_index: int, execute_reply: dict) -> None:
        nonlocal line_open
        print(f"  ({time.monotonic() - cell_start:.1f} s)", flush=True)
        line_open = False

    deadline = time.monotonic() + timeout
    # > Whether the cell that is running was cut short by the notebook's budget.
    budget_bound = False

    def limit(cell: NotebookNode) -> int:
        """Cap a cell at its own limit, or at what is left of the notebook's, if less."""
        nonlocal budget_bound
        remaining = deadline - time.monotonic()
        budget_bound = remaining < cell_timeout
        # > Never zero or negative: nbclient reads that as "no limit at all".
        return max(1, int(min(cell_timeout, remaining)))

    client = NotebookClient(
        nb,
        timeout=cell_timeout,
        timeout_func=limit,
        kernel_name=kernel,
        # > Stop at the first cell that fails: the rest would run on a broken state.
        allow_errors=False,
        resources={"metadata": {"path": str(workdir)}},
        on_cell_execute=report_start,
        on_cell_executed=report_end,
    )
    try:
        client.execute()
    except CellTimeoutError as exc:
        # > The cell only timed out because the notebook had nothing left to give it.
        if budget_bound:
            raise NotebookTimeout(f"{exc}\nThe notebook ran out of its {timeout} s.") from exc
        raise
    finally:
        # > A cell that timed out or killed the kernel never reported back.
        if line_open:
            print("  (did not finish)", flush=True)


def terminate(signum: int, frame: object) -> None:
    """Turn a SIGTERM into an exception, so that the temporary directory is cleaned up."""
    raise SystemExit(f"terminated by signal {signum}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "notebook",
        help="path to a notebook, or the name of one in scripts/notebooks/",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"wall-clock limit for the whole notebook, in seconds (default: {DEFAULT_TIMEOUT})",
    )
    parser.add_argument(
        "-c",
        "--cell-timeout",
        type=int,
        default=DEFAULT_CELL_TIMEOUT,
        help=f"wall-clock limit for a single cell, in seconds (default: {DEFAULT_CELL_TIMEOUT})",
    )
    parser.add_argument(
        "-k",
        "--kernel",
        default="python3",
        help="Jupyter kernel to run the notebook with (default: python3)",
    )
    args = parser.parse_args(argv)

    notebook = resolve_notebook(args.notebook)

    # > Headless: no GUI backend, and no plot window waiting for someone to close it.
    os.environ.setdefault("MPLBACKEND", "Agg")
    # > Whoever stops this run -- `run_notebooks.py`, a batch system -- gets a clean exit.
    signal.signal(signal.SIGTERM, terminate)

    print(f"notebook : {notebook}")
    print(f"python   : {sys.executable}")
    print(f"timeout  : {args.timeout} s per notebook, {args.cell_timeout} s per cell")

    error: Exception | None = None
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix=f"{notebook.stem}-") as workdir:
        print(f"workdir  : {workdir}\n")
        try:
            execute(notebook, Path(workdir), args.timeout, args.cell_timeout, args.kernel)
        except (CellExecutionError, CellTimeoutError, DeadKernelError, NotebookTimeout) as exc:
            error = exc
    duration = time.monotonic() - start

    if error is not None:
        print(f"\n{error}", file=sys.stderr)
        print(f"\nFAILED after {duration:.1f} s: {notebook.name}", file=sys.stderr)
        return 1

    print(f"\nOK in {duration:.1f} s: {notebook.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
