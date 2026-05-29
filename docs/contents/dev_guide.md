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

[Nox](https://nox.thea.codes/en/stable/) is a framework for automated testing.
It is configured via a central configuration file `noxfile.py`.
**Only touch this file if you know what you are doing!**

We use Nox not just for testing but also to drive all our tools that we use to ensure code quality and safety.
The individual tools will be explained in more detail later.

To execute Nox, o execute Nox, navigate to the project's root directory and use the following command:

```
nox <additional nox arguments>
```

Without any additional arguments, Nox will execute all (default) sessions that are defined in `noxfile.py`.
In Nox's world, a session is a predefined Python function that executes some code and returns a status.
Each session is executed in its own and isolated Python environment, which is set up and managed by Nox according to the
configuration.
This ensures that the outcome of each session is consistent across different environments.

To list all available sessions use:

```
nox -l
```

To run specific session(s):

```
nox -l <SESSION NAME> ...
```

We configured Nox such that it stops immediately as soon as a session fails.
Any following session will be skipped.
To disable this behaviour add `--no-stop-on-first-error` command shown above.
**This should be done if a specific aspect needs to be checked for which all desired sessions need to run!**

Furthermore, Nox allows adding tags to sessions:

```
@nox.session(tags=["static_check"])
def type_check(session):
    session.run_always("uv", "sync", "--group", "type_check")
    session.run("mypy")
```

which allows grouping multiple sessions together.

To run sessions by tags use:

```
nox -t <TAG> ...
```

All sessions are executed sequentially and independent of each other,
so that executing multiple sessions has no influence on one another.

## Our Nox Session

Below is a brief overview of the tools we use with Nox.

### Static Type Checking: mypy

This project uses [mypy](https://mypy-lang.org/) to ensure type safety.
Mypy is a static type checker based on type annotations in Python.
_Static_ means it does not execute any of the code to be checked.

To execute mypy run:

```
nox -s type_check
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

Before staging changes for a PR, all Mypy errors should be resolved.

### Linting and formatting: Ruff

[Ruff](https://docs.astral.sh/ruff/) is the fastest Python linter and code formatter currently out there.
In this project it is used for:

- linting:

```
nox -s lint
```

- sorting imports (replaced: [isort](https://pypi.org/project/isort/)):

```
nox -s imports
```

- and automatic and strict code formatting (replaced: [Black](https://pypi.org/project/black/)):

```
nox -s format_code
```

### Spell Checking: Codespell

We use [Codespell](https://github.com/codespell-project/codespell) for grammar and spell checking.
`codespell` expects American English.

It can be invoked as follows:

```
nox -s spell_check
```

Its output looks as follows:

```
./examples/exmp003_opt/job.out:1004: contruction ==> construction
./examples/exmp003_opt/job.out:1480: contruction ==> construction
./examples/exmp003_opt/job.out:1954: contruction ==> construction
./examples/exmp003_opt/job.out:2437: contruction ==> construction
./src/opi/input/models/calculator.py:264: inout ==> input, in out
./build/lib/opi/input/models/calculator.py:264: inout ==> input, in out
6
```

To exclude specific words or phrases from spell checking, add them to `.codespellignore`.
Each word or phrase must end with a newline.

### API Documentation: AutoAPI

This project uses [AutoAPI](https://sphinx-autoapi.readthedocs.io/en/latest/#) to automatically generate API documentation from docstrings.
Docstrings follow the [numpydoc style convention](https://numpydoc.readthedocs.io/en/latest/format.html) and are processed using Sphinx’s Napoleon extension for proper formatting and integration.

### Testing: Pytest

[Pytest](https://docs.pytest.org/en/stable/) is the de-facto industry standard for unit testing in Python.
All tests and related files are stored in `tests/`.

`tests/conftest.py` is the configuration file for Pytest.

We do use the following plugins to Pytest:

- [pytest-randomly](https://pypi.org/project/pytest-randomly/): Makes sure unit tests are always executed in random
  order, to avoid the introduction of biases due to the order
  of execution.
- [Hypothesis](https://hypothesis.readthedocs.io/en/latest): Allows generating random input for unit tests based on
  predefined constraints.
  This helps ensure that unit tests are not biased due to always having exactly the same input.

[Fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html) are stored in `tests/fixtures`.
Fixtures should be grouped into modules according to their nature.

To execute pytest run:

```
nox -s tests [--] [<pytest arguments>] 
```

Arguments following `--` are passed directly onto Pytest.

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
