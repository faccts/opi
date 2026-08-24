# Tests

This directory contains the test suite for **OPI**.\
This project uses the Pytest framework.

------------------------------------------------------------------------

## Overview

OPI distinguishes between two main kinds of tests:

1.  **Unit tests (CI-safe)**\
    These tests do **not** require ORCA and are run by default.
    -   Input-side tests (OPI → ORCA input generation)
    -   Output-side tests (JSON → Pydantic models → getters)
    -   General unit tests but no input formatting tests
2.  **Example tests (local-only)**\
    These tests execute the examples using ORCA.
    -   Used for end-to-end validation
    -   Also used to generate/update JSON files for output unit tests in the CI

Example code lives in the top-level `examples/` directory while
the corresponding tests are defined in `tests/examples`.

------------------------------------------------------------------------

## Running tests

Tests are run via **nox**. A typical invocation is:

    uv run nox -s tests

This executes all tests.

Running

    uv run nox -s unit_tests

will execute only the unit tests.
This is the mode typically used in CI.

------------------------------------------------------------------------

## Updating JSON output fixtures (requires ORCA)

Some unit output tests rely on JSON files derived from real ORCA
calculations.\
These JSON files are committed to the repository and stored under:

    tests/json_files/property

and 

    tests/json_files/gbw

To update these JSON fixtures, run:

    uv run nox -s json_gen

This will:

1.  Run selected example tests locally (with ORCA),
2.  Export and copy JSON output files,
3.  Update the committed JSON files used by output-side unit tests.

This step is only needed when the ORCA version or example
calculations change.

------------------------------------------------------------------------

## Updating the plain-text `.out` fixture (requires ORCA)

Some unit tests for the `Grepper` fallback rely on a minimal plain-text
ORCA output file committed at:

    tests/fixtures/job_fallback.out

This file is generated from `test_exmp003_opt` by extracting only the
blocks relevant to the `Grepper` (charge, multiplicity, Cartesian
coordinates, final single-point energy, Cartesian gradient). All
system-specific information (file paths, hostnames, timings) is
discarded automatically.

To regenerate this fixture, run:

    uv run nox -s out_gen

This step is only needed when the ORCA output format for these blocks
changes.

------------------------------------------------------------------------

## Output-side unit tests

Output tests verify OPI's parsing and API behavior without running ORCA.

Given JSON files from real ORCA runs, they check that:

-   Pydantic output models load successfully,
-   expected fields are populated (with a small set of
    exceptions),
-   output getter methods behave correctly.

Because these tests rely only on committed JSON fixtures, they are
CI-safe.

------------------------------------------------------------------------

## Notebook tests (requires ORCA and network access)

`test_notebook.py` executes every notebook in `docs/contents/notebooks/`
through `jupyter nbconvert`, one parametrized test per notebook:

    uv run nox -s notebook_tests

That session syncs the extra `notebooks` dependency group, which supplies
`nbconvert`, `ipykernel` and — because the notebooks install their own
extra dependencies with `!{sys.executable} -m pip install ...` and
uv-created environments have no `pip` — `pip` itself.

A single notebook can be run by its test id:

    uv run nox -s notebook_tests -- -k how_to_opi

Notebooks that cannot run unattended are skipped by default (`extopt`,
`ir_spectrum`, `ml_properties`, `opencosmors`); override the list with
`OPI_NOTEBOOKS_SKIP="a,b,c"`. `OPI_NOTEBOOK_CELL_TIMEOUT` (per cell) and
`OPI_NOTEBOOK_TIMEOUT` (per notebook) bound the runtime.

Two options support unattended runs:

-   `--notebook-summary=PATH`\
    Write a JSON summary of the run to `PATH`, atomically, with per-notebook
    status, duration and error information.

-   `--notebook-artifacts-dir=DIR`\
    Copy the working directory of each **failed** notebook into `DIR`, so
    the ORCA input/output files survive for a post-mortem.

See `scripts/slurm/README.md` for the weekly unattended cluster run.

------------------------------------------------------------------------

## Test markers

The following pytest markers are used:

-   `ase`\
    Tests that require **ASE**

-   `examples`\
    Tests that execute examples from the top level `examples/` directory.

-   `orca`\
    Tests that require **ORCA**

-   `slow`\
    Tests that take longer to run

-   `input`\
    Input-side unit tests (OPI → ORCA input)

-   `output`\
    Output-side unit tests (JSON → models → getters)

-   `unit`\
    General unit tests

-   `json_files`\
    Tests related to exporting/updating JSON files using
    `--update-json-files`

-   `out_files`\
    Tests related to exporting/updating the plain-text `.out` fixture
    using `--update-out-files`

-   `notebooks`\
    Tests that execute the documentation notebooks from
    `docs/contents/notebooks/`. These require **ORCA**, network access (the
    notebooks install their own extra dependencies at runtime) and take hours.
    Run them with `uv run nox -s notebook_tests`, which syncs the extra
    `notebooks` dependency group. See `scripts/slurm/README.md` for the weekly
    unattended run.

Markers can be combined using standard pytest syntax, for example:

    uv run nox -s tests -- -m "orca and not slow"

------------------------------------------------------------------------

## CI policy (summary)

-   CI typically runs unit tests only
-   CI does not run ORCA by default
-   JSON fixtures ensure output parsing is fully tested in CI
