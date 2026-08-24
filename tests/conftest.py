"""
Location of fixtures for pytest must be listed here.

To define the location of module containing fixtures, the absolute path to that model
starting from the main package folder must be given.
"""

import time
from collections.abc import Generator
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, cast

import pytest
from _pytest._code.code import ExceptionRepr
from _pytest.nodes import Item
from _pytest.reports import TestReport
from _pytest.runner import CallInfo

from tests.helpers import (
    NOTEBOOK_RESULTS,
    NOTEBOOK_RUN_CONFIG,
    NOTEBOOK_RUN_START,
    JsonFilesExporter,
    OutFileExporter,
    write_notebook_summary,
)

JSON_DIR = Path(__file__).parent / "json_files"


@pytest.fixture(scope="session")
def json_dir() -> Path:
    """
    Path to the JSON directory.
    """
    return JSON_DIR


# > Location of modules containing fixtures.
# >> Searching for Python modules which do no start with an underscore and converting file path to module path.
pytest_plugins = [
    f"tests.fixtures.{filename.stem}"
    for filename in Path(__file__).parent.joinpath("fixtures").glob("*.py")
    if not filename.name.startswith("_")
]


@pytest.fixture(scope="session")
def json_file_list(json_dir: Path) -> list[Path]:
    """
    Provide list of test JSON file paths for Output unit tests.

    Parameters
    ----------
    json_dir: Path
        Path to the JSON directory.

    Returns
    -------
    list[Path]
        List of test JSON file paths.

    """
    filenames = [
        "gbw/test_exmp003_opt_job.json",
        "property/test_exmp003_opt_job.property.json",
        "gbw/test_exmp006_mp2_job.json",
        "property/test_exmp006_mp2_job.property.json",
        "gbw/test_exmp009_rama_job.json",
        "property/test_exmp009_rama_job.property.json",
        "gbw/test_exmp010_uvvis_job.json",
        "property/test_exmp010_uvvis_job.property.json",
        "gbw/test_exmp011_epr_job.json",
        "property/test_exmp011_epr_job.property.json",
        "gbw/test_exmp012_nmr_job.json",
        "property/test_exmp012_nmr_job.property.json",
        "gbw/test_exmp013_bs_job.json",
        "property/test_exmp013_bs_job.property.json",
        "gbw/test_exmp014_led_job.json",
        "property/test_exmp014_led_job.property.json",
        "gbw/test_exmp015_pop_analysis_job.json",
        "property/test_exmp015_pop_analysis_job.property.json",
        "gbw/test_exmp016_autoci_job.json",
        "property/test_exmp016_autoci_job.property.json",
        "gbw/test_exmp017_roci_job.json",
        "property/test_exmp017_roci_job.property.json",
        "gbw/test_exmp018_cipsi_job.json",
        "property/test_exmp018_cipsi_job.property.json",
        "gbw/test_exmp019_engrad_job.json",
        "property/test_exmp019_engrad_job.property.json",
        "gbw/test_exmp028_nevp2_job.json",
        "property/test_exmp028_nevp2_job.property.json",
        "gbw/test_exmp038_integrals_job.json",
        "property/test_exmp038_integrals_job.property.json",
        "gbw/test_exmp052_densities_job.json",
        "property/test_exmp052_densities_job.property.json",
    ]

    return [json_dir / f for f in filenames]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item: Item,
    call: CallInfo[Any],
) -> Generator[None, Any, None]:
    """
    Hookwrapper for printing the scratch directory when a test with `tmp_path` in its signature fails

    Examples
    --------
    When `test_example001` fails, pytest will print something like this:
        /user/opi/examples/exmp001_scf/job.py:48: SystemExit: 1
        see ORCA files in: /tmp/pytest-of-user/pytest-24/test_exmp001_scf0
    If no error message can be retrieved, just the folder is printed:
        Test of an example failed, see ORCA files in: /tmp/pytest-of-user/pytest-24/test_exmp001_scf0

    """
    # In a hookwrapper, the value of `outcome = yield` is *sent* into the generator.
    # We declare the generator's SendType as `Any`.
    outcome = yield

    # > cast outcome result to the concrete pytest report.
    rep = cast(TestReport, outcome.get_result())

    # > If the test failed
    if rep.failed:
        # `funcargs` isn't in Item's public stubs; use getattr + cast to satisfy mypy.
        funcargs = cast(dict[str, Any], getattr(item, "funcargs", {}))

        # > if `tmp_path` is in the functions signature
        tmp = cast(Path | None, funcargs.get("tmp_path"))
        if tmp is not None:
            # > make mypy happy by making sure `when` is not None
            when = rep.when or "call"
            item.add_report_section(when, "scratch", str(tmp))

            # > Write `long` representation of the test report
            if isinstance(rep.longrepr, ExceptionRepr):
                crash = rep.longrepr.reprcrash
                # > Try to give path, line number and error type, alternatively just the scratch_dir
                if crash is not None:
                    path = crash.path
                    lineno = crash.lineno
                    message = crash.message
                    rep.longrepr = f"{path}:{lineno}: {message}\nsee ORCA files in: {tmp}"
                else:
                    rep.longrepr = f"Test of an example failed, see ORCA files in: {tmp}"


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--update-json-files",
        action="store_true",
        default=False,
        help="After json file generator tests pass, copy all produced *.json from tmp_path into tests/json_files/.",
    )
    parser.addoption(
        "--update-out-files",
        action="store_true",
        default=False,
        help="After out file generator tests pass, extract grepper-relevant blocks from the produced .out file and write to tests/fixtures/job_fallback.out.",
    )
    parser.addoption(
        "--notebook-summary",
        action="store",
        default=None,
        metavar="PATH",
        help="Write a JSON summary of the notebook run to PATH (atomically overwritten each run).",
    )
    parser.addoption(
        "--notebook-artifacts-dir",
        action="store",
        default=None,
        metavar="DIR",
        help="Copy the working directory of each FAILED notebook into DIR for post-mortem analysis.",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.stash[NOTEBOOK_RESULTS] = []
    config.stash[NOTEBOOK_RUN_START] = (
        time.monotonic(),
        datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """
    Emit the notebook summary file, if one was requested and notebooks actually ran.

    The `results` guard means a plain `nox -s tests` run never writes a summary, and a
    run that collected no notebooks cannot clobber a good summary with an empty one.
    """
    summary_path = session.config.getoption("--notebook-summary")
    results = session.config.stash.get(NOTEBOOK_RESULTS, [])
    run_config = session.config.stash.get(NOTEBOOK_RUN_CONFIG, None)
    if not summary_path or not results or run_config is None:
        return

    started_monotonic, started_at = session.config.stash[NOTEBOOK_RUN_START]
    write_notebook_summary(
        Path(summary_path),
        results,
        rootpath=Path(session.config.rootpath),
        run_config=run_config,
        exit_status=exitstatus,
        started_monotonic=started_monotonic,
        started_at=started_at,
    )


@pytest.fixture(scope="session")
def json_files_dir(request: pytest.FixtureRequest) -> Path:
    return Path(request.config.rootpath) / "tests" / "json_files"


@pytest.fixture
def json_files_exporter(request: pytest.FixtureRequest, json_files_dir: Path) -> JsonFilesExporter:
    if "json_files" not in request.node.keywords:
        pytest.fail("json_files_exporter is intended for tests marked with @pytest.mark.json_files")

    return JsonFilesExporter(
        json_files_dir=json_files_dir,
        prefix=request.node.name,  # json_file basename
        enabled=request.config.getoption("--update-json-files"),
    )


@pytest.fixture(scope="session")
def fixtures_dir(request: pytest.FixtureRequest) -> Path:
    return Path(request.config.rootpath) / "tests" / "fixtures"


@pytest.fixture
def out_file_exporter(request: pytest.FixtureRequest, fixtures_dir: Path) -> OutFileExporter:
    if "out_files" not in request.node.keywords:
        pytest.fail("out_file_exporter is intended for tests marked with @pytest.mark.out_files")

    return OutFileExporter(
        out_file=fixtures_dir / "job_fallback.out",
        enabled=request.config.getoption("--update-out-files"),
    )
