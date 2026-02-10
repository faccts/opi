# > UV requires Python >= 3.8. So we cannot test any version older than that (not that we would want to anyway!).
import os

# > External packages
import nox

# > Don't update lock file when setting up virtual envs.
os.environ.update({"UV_FROZEN": "1"})
# > Disable automatic donwload of Python distributions
os.environ.update({"UV_PYTHON_DOWNLOADS": "never"})
# > Making sure Nox session only see their packages and not any globally installed packages.
os.environ.pop("PYTHONPATH", None)
# > Hiding any virtual environments from outside.
os.environ.pop("VIRTUAL_ENV", None)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                                               GLOBAL NOX OPTIONS
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# > Stop after first session that fails.
# > Can be turned off with '--no-stop-on-first-error'
nox.options.stop_on_first_error = True
# > NOX can detect if a binary is called from outside the currently running session.
# > Make sure we use that the binary from the session specific virtual environment.
nox.options.error_on_external_run = True
# > Mark sessions as failed if NOX cannot find the desired Python interpreter.
# > By default, NOX just skips these sessions.
nox.options.error_on_missing_interpreters = True
# > Always start from a clean environment.
nox.options.reuse_existing_virtualenvs = True
# > Using "uv" instead of "venv" as default backend
nox.options.default_venv_backend = "uv"


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                                                   NOX SESSIONS
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# //////////////////////////////////////////
# ///         UNIT TESTS: pytest         ///
# //////////////////////////////////////////
@nox.session(default=False)
def tests(session):
    session.run_install(
        "uv",
        "sync",
        "--group",
        "tests",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run("pytest", *session.posargs)


# //////////////////////////////////////////
# ///     STATIC TYPE CHECKING: mypy     ///
# //////////////////////////////////////////
@nox.session(tags=["static_check", "pr_check"])
def type_check(session):
    session.run_install(
        "uv",
        "sync",
        "--group",
        "type_check",
        "--all-extras",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run("mypy")


# //////////////////////////////////////////////////
# ///        REMOVING UNUSED IMPORTS: Ruff      ///
# ////////////////////////////////////////////////
@nox.session(tags=["style", "fix", "static_check"])
def remove_unused_imports(session):
    session.run_install(
        "uv",
        "sync",
        "--group",
        "lint",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    # > Sorting imports with ruff instead of isort
    session.run("ruff", "check", "--select", "F401", "--fix", "--exit-non-zero-on-fix")

@nox.session(tags=["pr_check"], default=False)
def check_unused_imports(session):
    session.run_install(
        "uv",
        "sync",
        "--group",
        "lint",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run("ruff", "check", "--select", "F401")


# //////////////////////////////////////////
# ///        SORTING IMPORTS: Ruff      ///
# //////////////////////////////////////////
@nox.session(tags=["style", "fix", "static_check"])
def sort_imports(session):
    session.run_install(
        "uv",
        "sync",
        "--group",
        "lint",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    # > Sorting imports with ruff instead of isort
    session.run("ruff", "check", "--select", "I", "--fix", "--exit-non-zero-on-fix")


@nox.session(tags=["pr_check"])
def check_sort_imports(session):
    session.run_install(
        "uv",
        "sync",
        "--group",
        "lint",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    # > Sorting imports with ruff instead of isort
    session.run("ruff", "check", "--select", "I")


# ////////////////////////////////////////
# ///         LINTING: Ruff            ///
# ////////////////////////////////////////
@nox.session(tags=["style", "static_check", "pr_check"])
def lint(session):
    session.run_install(
        "uv",
        "sync",
        "--group",
        "lint",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run("ruff", "check")


# //////////////////////////////////////////
# ///         CODE FORMATTING: Ruff     ///
# //////////////////////////////////////////
@nox.session(tags=["style", "fix", "static_check"])
def format_code(session):
    session.run_install(
        "uv",
        "sync",
        "--group",
        "lint",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run("ruff", "format", "--exit-non-zero-on-format")


@nox.session(tags=["pr_check"])
def check_format_code(session):
    """
    Only check if code was formatted with Ruff.
    """
    session.run_install(
        "uv",
        "sync",
        "--group",
        "lint",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run("ruff", "format", "--check")


# ////////////////////////////////////////////////////
# ///         SPELL CHECKING: codespell            ///
# ////////////////////////////////////////////////////
@nox.session(tags=["static_check", "pr_check"])
def spell_check(session):
    session.run_install(
        "uv",
        "sync",
        "--group",
        "spell-check",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run("codespell", "src/opi")


# //////////////////////////////////////////////
# ///         DEAD CODE: vulture            ///
# /////////////////////////////////////////////
@nox.session(tags=["static_check", "pr_check"], default=True)
def dead_code(session):
    session.run_install(
        "uv",
        "sync",
        "--group",
        "dead-code",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run("vulture")
