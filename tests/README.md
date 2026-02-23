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

Markers can be combined using standard pytest syntax, for example:

    uv run nox -s tests -- -m "orca and not slow"

------------------------------------------------------------------------

## CI policy (summary)

-   CI typically runs unit tests only
-   CI does not run ORCA by default
-   JSON fixtures ensure output parsing is fully tested in CI
