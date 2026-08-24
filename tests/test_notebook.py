#!/usr/bin/env python
"""Execute every notebook in docs/contents/notebooks/ and report pass/fail per notebook."""

import os
import re
import shutil
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pytest

from tests.helpers import (
    NOTEBOOK_RESULTS,
    NOTEBOOK_RUN_CONFIG,
    NotebookResult,
    NotebookRunConfig,
)

NOTEBOOKS_DIR = Path(__file__).parent.parent / "docs" / "contents" / "notebooks"

# > Notebooks that cannot be executed unattended:
# >   extopt / ir_spectrum / ml_properties -> require external tooling,
# >   opencosmors                          -> its openCOSMO-RS_py install instruction lives in a
# >                                           markdown cell, so `import opencosmorspy` always fails.
# > Override with OPI_NOTEBOOKS_SKIP="a,b,c"; an empty string skips nothing.
DEFAULT_SKIP = ("extopt", "ir_spectrum", "ml_properties", "opencosmors")

# > Timeout nbconvert applies to a single CELL.
CELL_TIMEOUT = int(os.environ.get("OPI_NOTEBOOK_CELL_TIMEOUT", "1800"))
# > Hard cap on a whole notebook. Without this a single hung cell can consume an entire
# > batch allocation, and the run then produces no summary at all.
NOTEBOOK_TIMEOUT = int(os.environ.get("OPI_NOTEBOOK_TIMEOUT", "5400"))

ALL_NOTEBOOKS = sorted(NOTEBOOKS_DIR.glob("*.ipynb"))

# > ORCA scratch files are large and worthless for a post-mortem.
_ARTIFACT_IGNORE = shutil.ignore_patterns("*.tmp", "*.tmp.*", "*.bas*", "*.densities*")

_ERROR_LINE = re.compile(r"^(?P<kind>[A-Za-z_][\w.]*(?:Error|Exception)): ?(?P<msg>.*)$", re.M)
_ANSI = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")

# > nbclient wraps whatever the cell raised in one of these. They are always the *last*
# > exception in the log but say nothing useful ("An error occurred while executing the
# > following cell"), so the root cause below them is what gets reported.
_WRAPPER_ERRORS = frozenset(
    {
        "nbclient.exceptions.CellExecutionError",
        "CellExecutionError",
        "nbclient.exceptions.DeadKernelError",
        "DeadKernelError",
    }
)


def _strip_ansi(text: str) -> str:
    """Remove ANSI colour escapes, which nbconvert emits into its tracebacks."""
    return _ANSI.sub("", text)


def _skiplist() -> frozenset[str]:
    """Return the notebook stems to skip, honouring the OPI_NOTEBOOKS_SKIP override."""
    raw = os.environ.get("OPI_NOTEBOOKS_SKIP")
    if raw is None:
        return frozenset(DEFAULT_SKIP)
    return frozenset(part.strip() for part in raw.split(",") if part.strip())


def _last_error(log: str) -> tuple[str | None, str | None]:
    """
    Extract the last `SomeError: message` line from an nbconvert log.

    Parameters
    ----------
    log : str
        Combined stdout/stderr of the nbconvert run.

    Returns
    -------
    tuple[str | None, str | None]
        The exception class name and its message, or (None, None) if none was found.
    """
    matches = _ERROR_LINE.findall(log)
    if not matches:
        return None, None
    # > Prefer the deepest real exception over nbclient's outer wrapper.
    root_causes = [m for m in matches if m[0] not in _WRAPPER_ERRORS]
    kind, msg = (root_causes or matches)[-1]
    return kind, msg.strip()


def run_notebook(nb: Path, workdir: Path) -> tuple[int | None, float, str, bool]:
    """
    Execute a single notebook inside `workdir` via nbconvert.

    The notebook is copied into `workdir` first, because the notebooks create their
    scratch directories relative to the current working directory and would otherwise
    litter `docs/contents/notebooks/`.

    Parameters
    ----------
    nb : Path
        Notebook to execute.
    workdir : Path
        Directory to copy the notebook into and run it from.

    Returns
    -------
    tuple[int | None, float, str, bool]
        Exit code, elapsed seconds, combined output, and whether it timed out.
    """
    nb_copy = workdir / nb.name
    shutil.copy2(nb, nb_copy)
    cmd = [
        sys.executable,
        "-m",
        "jupyter",
        "nbconvert",
        "--execute",
        "--to",
        "notebook",
        f"--ExecutePreprocessor.timeout={CELL_TIMEOUT}",
        "--ExecutePreprocessor.kernel_name=python3",
        "--output",
        nb.name,
        "--output-dir",
        str(workdir),
        str(nb_copy),
    ]

    start = time.monotonic()
    # > `start_new_session` puts nbconvert, its ipykernel child and any ORCA/mpirun below it
    # > into one process group, so a timeout can kill the whole tree. Without it an orphaned
    # > ORCA keeps burning the allocation after the notebook has been abandoned.
    proc = subprocess.Popen(
        cmd,
        cwd=workdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True,
    )
    timed_out = False
    try:
        log = proc.communicate(timeout=NOTEBOOK_TIMEOUT)[0]
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            proc.kill()
        log = (proc.communicate()[0] or "") + f"\n[timeout after {NOTEBOOK_TIMEOUT}s]"

    return proc.returncode, time.monotonic() - start, _strip_ansi(log or ""), timed_out


@pytest.mark.notebooks
@pytest.mark.parametrize("notebook", ALL_NOTEBOOKS, ids=lambda nb: nb.stem)
def test_notebook(notebook: Path, tmp_path: Path, request: pytest.FixtureRequest) -> None:
    """
    Execute a single documentation notebook end-to-end and fail if it does not complete.

    Skipped notebooks are still recorded, so the summary file lists every notebook rather
    than silently omitting the ones that were not attempted.
    """
    config = request.config
    artifacts_dir = config.getoption("--notebook-artifacts-dir")
    skiplist = _skiplist()

    if NOTEBOOK_RUN_CONFIG not in config.stash:
        config.stash[NOTEBOOK_RUN_CONFIG] = NotebookRunConfig(
            notebooks_dir=str(NOTEBOOKS_DIR),
            skipped=sorted(skiplist),
            cell_timeout_s=CELL_TIMEOUT,
            notebook_timeout_s=NOTEBOOK_TIMEOUT,
            artifacts_dir=artifacts_dir,
        )

    record = NotebookResult(
        name=notebook.stem,
        path=str(notebook),
        started_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        workdir=str(tmp_path),
    )
    config.stash[NOTEBOOK_RESULTS].append(record)

    if notebook.stem in skiplist:
        record.status = "skipped"
        pytest.skip(f"{notebook.stem} is on the notebook skip list")

    returncode, duration, log, timed_out = run_notebook(notebook, tmp_path)
    record.duration_s = round(duration, 1)
    record.returncode = returncode

    if returncode == 0 and not timed_out:
        record.status = "passed"
        return

    record.status = "timeout" if timed_out else "failed"
    record.error_kind, record.error_message = _last_error(log)
    record.log_tail = log[-8000:]

    if artifacts_dir:
        dest = Path(artifacts_dir) / notebook.stem
        shutil.rmtree(dest, ignore_errors=True)
        shutil.copytree(tmp_path, dest, ignore=_ARTIFACT_IGNORE)
        record.artifacts = str(dest)

    pytest.fail(
        f"{notebook.name} {record.status} (exit {returncode})\n"
        f"{record.error_kind}: {record.error_message}\n"
        f"--- nbconvert log tail ---\n{log[-4000:]}",
        pytrace=False,
    )
