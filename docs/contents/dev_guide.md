# Development Guide

This guide is intended for developers contributing to this project.

## Python

OPI is completely written in Python. Therefore, only functioning Python code should be contributed.

## Dependency Management: uv

The OPI project uses [uv](https://github.com/astral-sh/uv) to manage dependencies and for installation.
uv is “an extremely fast Python package and project manager, written in Rust.”
There are several ways to install uv. However, we prefer to install it with [pipx](https://github.com/pypa/pipx):

```
pipx install uv
```

## Build Backend: Hatchling

[Hatchling](https://pypi.org/project/hatchling/) is used as build-backend.
The project can be build as follows from the project's root folder:

```
uv build [--wheel] [--sdist]
```

The build(s) can then be found in `dist/`.

## Installation as Developer

To install this package in development mode, run the following command from the root directory:

```
uv sync
```

This will create a new virtual environment (venv) with a matching Python version and install the package there:

- `--only-dev` will additionally install all developing dependencies.
- `--group <groupname>` allows including dependencies from the given dependency group.
- `--all-groups` adds all dependencies from all groups to the virtual environment.

The default location of the virtual environment is usually the `.venv/` folder in the project's root folder.
**Any pre-existing `.venv` folder should be deleted before installation!**

## Dependency Management

uv uses version locking, where the exact version of each required package and its sub-dependencies
are stored in a central lock file `uv.lock` (similar to `cargo.lock` from Rust).

**`uv.lock` is not meant to be edited by hand!**

First-level dependencies are external packages which a project directly depends on.
These are specified in `pyproject.toml`.

To add new dependencies to the project use uv's `add` command.
E.g., here shown with Numpy:

```
uv add numpy
```

Numpy will be added to `pyproject.toml` and the lock file.
The lock file will also contain all sub-dependencies of Numpy.

Version constraints can be imposed according to [PEP 508](https://peps.python.org/pep-0508/#grammar).
Usually this is not necessary, but can become necessary if a newer version contains a not yet fixed bug or the API
changed between two major versions, breaking the project.
Here is an example of how to constrain the version of Numpy:
To use the latest version 1.x, but do not update to next major version 2.0, one would include the constraint in the
command as follows:

```
uv add 'numpy>=1,<2'
```

It is generally good practice to wrap the package name into quotes when using version constraints, to avoid any escaping
issues with the shell.

To remove dependencies use:

```
uv remove numpy
```

### Grouping Dependencies

Most dependency managers allow to group dependencies, e.g., to allow modularization of programs or to
separate development requirements from execution requirements.
If no group is specified then the default group (or main group) is used,
which contains all dependencies required to execute the package.
To add a dependency to a group the `--group <groupname>` option is used:

```
uv add --group math 'numpy>=1,<2'
```

for both regular and development dependencies (`--dev`):

```
uv add --dev 'numpy>=1,<2'
```

Dependencies can be added to multiple groups at once.
Version constraints can be applied per dependency per group, but they cannot exclude each other.
In the end, only one version of the dependency that satisfies all the constraints will be installed.

## Nox

[Nox](https://nox.thea.codes/en/stable/) drives all tools we use to ensure code quality: the test suite, static type
checking, linting, formatting, spell checking and dead-code detection.
It is configured via the central file `noxfile.py`.
**Only touch this file if you know what you are doing!**

**Always run the tools through Nox, and Nox through uv.**
Do not call `pytest`, `mypy`, `ruff`, etc. directly.
Each Nox session installs exactly the dependency group it needs from the locked `uv.lock` into its own isolated
virtual environment, so you get the same tool versions and the same configuration as the CI.
Nox itself is part of the `dev` dependency group, which `uv sync` installs by default, so there is nothing to install
globally:

```
uv run nox <additional nox arguments>
```

### Quick start

Normal development needs only two commands:

```
uv run nox                  # all static checks and auto-fixers
uv run nox -s unit_tests    # the unit tests
```

`uv run nox` runs all static checks (type checking, linting, spell checking, dead-code detection) together with the
auto-fixers for formatting and imports. Use it for everyday work.
To run the unit tests, use the `unit_tests` session.
These are the checks the CI runs on every pull request, so run both before opening a pull request.

### Sessions

In Nox's world, a session is a predefined Python function that executes some code and returns a status.
Each session runs in its own isolated virtual environment, so executing multiple sessions has no influence on one another.
Virtual environments are kept in `.nox/` and reused between runs.

To list all available sessions (default sessions are marked with `*`):

```
uv run nox -l
```

To run specific session(s):

```
uv run nox -s <SESSION NAME> ...
```

Without any arguments, Nox executes all default sessions.

The sessions that fix formatting and imports modify files in place and report a failure if they changed anything,
so simply rerun `uv run nox`.

Nox is configured to stop as soon as a session fails; any following session is skipped.
To run all selected sessions regardless, add `--no-stop-on-first-error`:

```
uv run nox --no-stop-on-first-error
```

## Our Tools

Below is a brief overview of the tools we run with Nox.

### Static Type Checking: mypy

This project uses [mypy](https://mypy-lang.org/) to ensure type safety.
Mypy is a static type checker based on type annotations in Python.
_Static_ means it does not execute any of the code to be checked.
Mypy runs in strict mode, so all new code in `src/` must be fully typed.

To execute mypy run:

```
uv run nox -s type_check
```

Its output will look as follows:

```
src/opi/output/core.py:1: error: Cannot find implementation or library stub for module named "calc_status"  [import-not-found]
    import calc_status
    ^
src/opi/output/core.py:1: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
src/opi/output/core.py:2: error: Cannot find implementation or library stub for module named "geometry"  [import-not-found]
[...]
src/opi/output/geometry.py:1: error: Cannot find implementation or library stub for module named "coord"  [import-not-found]
    import coord
    ^
Found 30 errors in 3 files (checked 15 source files)
```

Before staging changes for a PR, all mypy errors should be resolved.

### Linting and Formatting: Ruff

[Ruff](https://docs.astral.sh/ruff/) is the fastest Python linter and code formatter currently out there.
In this project it is used for:

- linting:

```
uv run nox -s lint
```

- sorting imports (replaced: [isort](https://pypi.org/project/isort/)):

```
uv run nox -s sort_imports
```

- removing unused imports:

```
uv run nox -s remove_unused_imports
```

- and automatic and strict code formatting (replaced: [Black](https://pypi.org/project/black/)):

```
uv run nox -s format_code
```

All of these sessions are part of the default `uv run nox` run.

### Spell Checking: Codespell

We use [Codespell](https://github.com/codespell-project/codespell) for spell checking.
`codespell` expects American English.

It can be invoked as follows:

```
uv run nox -s spell_check
```

Its output looks as follows:

```
./src/opi/input/models/calculator.py:264: inout ==> input, in out
1
```

To exclude specific words or phrases from spell checking, add them to `.codespellignore`.
Each word or phrase must end with a newline.

### Dead Code: vulture

[vulture](https://github.com/jendrikseipp/vulture) finds unused code such as functions, classes and variables:

```
uv run nox -s dead_code
```

### API Documentation: AutoAPI

This project uses [AutoAPI](https://sphinx-autoapi.readthedocs.io/en/latest/#) to automatically generate API documentation from docstrings.
Docstrings follow the [numpydoc style convention](https://numpydoc.readthedocs.io/en/latest/format.html) and are processed using Sphinx’s Napoleon extension for proper formatting and integration.

### Testing: Pytest

[Pytest](https://docs.pytest.org/en/stable/) is the de-facto industry standard for unit testing in Python.
All tests and related files are stored in `tests/`.
Pytest is configured under `[tool.pytest]` in `pyproject.toml`, and `tests/conftest.py` holds shared fixtures and options.

We do use the following plugins to Pytest:

- [pytest-randomly](https://pypi.org/project/pytest-randomly/): Makes sure unit tests are always executed in random
  order, to avoid the introduction of biases due to the order
  of execution.
- [Hypothesis](https://hypothesis.readthedocs.io/en/latest): Allows generating random input for unit tests based on
  predefined constraints.
  This helps ensure that unit tests are not biased due to always having exactly the same input.

[Fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html) are stored in `tests/fixtures`.
Fixtures should be grouped into modules according to their nature.

Pytest is always run via Nox, never directly:

```
uv run nox -s unit_tests                   # unit tests only (marker `unit`), as run by the CI
uv run nox -s tests                        # all tests; the example tests require a local ORCA installation
```

Arguments following `--` are passed directly on to Pytest.
This allows, e.g., running a single test file, a single test, or selecting tests by marker:

```
uv run nox -s tests -- tests/unit/path/test_file.py
uv run nox -s tests -- tests/unit/path/test_file.py -k test_name
uv run nox -s tests -- -m "orca and not slow"
```

A few further sessions require a local ORCA installation and are only needed occasionally:

```
uv run nox -s json_gen                     # regenerate the JSON fixtures in tests/json_files/
uv run nox -s out_gen                      # regenerate the plain-text fixture tests/fixtures/job_fallback.out
uv run nox -s notebooks -- how_to_opi      # execute a documentation notebook (see tests/README.md)
```

See `tests/README.md` for the test layout, markers and fixtures.

## Style Guide

We strictly follow the rules employed in [Black](https://black.readthedocs.io/en/stable/).
For performance reasons, we use Ruff, which is designed as a drop-in replacement for Black.
Ruff is not fully compliant to Black ([https://docs.astral.sh/ruff/formatter/#intentional-deviations](https://docs.astral.sh/ruff/formatter/#intentional-deviations)).

### Code Conventions

We follow PEP 8 guidelines for naming variables, functions, and other identifiers to ensure consistency and readability across our codebase.
Indentation is standardized to 4 spaces per level—tabs must not be used.
Additionally, we've extended the maximum line length to 100 characters to enhance code clarity and make better use of modern screen widths.

### File Names

Please name files using snake_case, with words separated by underscores (e.g. `this_is_my_file.py`).
