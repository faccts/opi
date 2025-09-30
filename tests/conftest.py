"""
Location of fixtures for pytest must be listed here.

To define the location of module containing fixtures, the absolute path to that model
starting from the main package folder must be given.
"""

from collections.abc import Generator
from pathlib import Path
from typing import Any, Optional, cast

import pytest
from _pytest._code.code import ExceptionRepr
from _pytest.nodes import Item
from _pytest.reports import TestReport
from _pytest.runner import CallInfo

# > Location of modules containing fixtures.
# >> Searching for Python modules which do no start with an underscore and converting file path to module path.
pytest_plugins = [
    f"tests.fixtures.{filename.stem}"
    for filename in Path(__file__).parent.joinpath("fixtures").glob("*.py")
    if not filename.name.startswith("_")
]


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
        tmp = cast(Optional[Path], funcargs.get("tmp_path"))
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
