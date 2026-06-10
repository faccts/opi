#!/usr/bin/env python
"""Run all notebooks in tests/notebooks/ and report pass/fail."""

import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pytest

# NOTEBOOKS_DIR = Path(__file__).parent.parent / "docs/contents/notebooks"
NOTEBOOKS_DIR = Path(__file__).parent / "notebooks"


def run_notebook(nb: Path) -> tuple[bool, float, str]:
    start = time.monotonic()
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            [
                "jupyter",
                "nbconvert",
                "--execute",
                "--to",
                "notebook",
                "--ExecutePreprocessor.timeout=1800",
                f"--ExecutePreprocessor.kernel_cwd={tmp}",
                "--output",
                nb.name,
                str(nb),
            ],
            capture_output=True,
            text=True,
            cwd=nb.parent,
        )
    elapsed = time.monotonic() - start
    return result.returncode == 0, elapsed, result.stdout + result.stderr


@pytest.mark.notebooks
def test_notebooks() -> None:
    notebooks = sorted(NOTEBOOKS_DIR.glob("*.ipynb"))
    if not notebooks:
        print(f"No notebooks found in {NOTEBOOKS_DIR}")
        sys.exit(1)

    results: list[tuple[str, bool, float]] = []
    for nb in notebooks:
        print(f"  running {nb.name} ...", end="", flush=True)
        ok, elapsed, output = run_notebook(nb)
        status = "PASS" if ok else "FAIL"
        print(f" {status} ({elapsed:.1f}s)")
        if not ok:
            print(output)
        results.append((nb.name, ok, elapsed))

    print()
    failures = [name for name, ok, _ in results if not ok]
    print(f"{len(notebooks) - len(failures)}/{len(notebooks)} notebooks passed")
    if failures:
        print("Failed:")
        for name in failures:
            print(f"  - {name}")
        sys.exit(1)
