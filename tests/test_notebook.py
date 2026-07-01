#!/usr/bin/env python
"""Run all notebooks in tests/notebooks/ and report pass/fail."""

import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pytest

NOTEBOOKS_DIR = Path(__file__).parent.parent / "docs/contents/notebooks"
BLACKLIST = [
    "extopt",
    "ir_spectrum",
    "ml_properties"
]


def run_notebook(nb: Path) -> tuple[bool, float, str]:
    """
    Helper function that runs a specific notebook and reports pass/fail.
    Parameters
    ----------
    nb

    Returns
    -------

    """
    start = time.monotonic()
    with tempfile.TemporaryDirectory() as tmp:
        nb_copy = Path(tmp) / nb.name
        shutil.copy2(nb, nb_copy)
        result = subprocess.run(
            [
                "jupyter",
                "nbconvert",
                "--execute",
                "--to",
                "notebook",
                "--ExecutePreprocessor.timeout=1800",
                "--output",
                nb.name,
                "--output-dir",
                tmp,
                str(nb_copy),
            ],
            capture_output=True,
            text=True,
            cwd=tmp,
        )
    elapsed = time.monotonic() - start
    return result.returncode == 0, elapsed, result.stdout + result.stderr


@pytest.mark.notebooks
def test_notebooks() -> None:
    """
    Function to iteratively test whether all notebooks (with exception to the ones to be excluded, which are defined in `BlACKLIST`) execute
    without issues. In the case that a notebook execution fails,the function will print out which notebooks fail and the error message.
    """
    notebooks = [nb for nb in NOTEBOOKS_DIR.glob("*.ipynb") if nb.stem not in BLACKLIST]
    if not notebooks:
        print(f"No valid notebooks found in {NOTEBOOKS_DIR}")
        sys.exit(1)

    results: list[tuple[str, bool, float]] = []
    for nb in notebooks:
        print(f"  running {nb.stem} ...", end="", flush=True)
        ok, elapsed, output = run_notebook(nb)
        status = "PASS" if ok else "FAIL"
        print(f" {status} ({elapsed:.1f}s)")
        if not ok:
            print(output)
        results.append((nb.name, ok, elapsed))

    failures = [name for name, ok, _ in results if not ok]
    print(f"{len(notebooks) - len(failures)}/{len(notebooks)} notebooks passed")
    if failures:
        print("Failed:")
        for name in failures:
            print(f"  - {name}")
        sys.exit(1)
