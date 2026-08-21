import subprocess
from typing import Protocol, Sequence
from unittest.mock import Mock

import pytest

from opi.execution.base import RunResult
from opi.execution.orca_mm import OrcaMmError, OrcaMmRunner
from opi.lib.orca_binary import OrcaBinary

"""
This module contains tests for `OrcaMmRunner` command execution such as:
- Returning successful execution results
- Raising `OrcaMmError` after unsuccessful execution
- Passing command arguments and stream targets to `BaseRunner.run`

ORCA discovery and binary execution are mocked so that these tests do not
depend on external ORCA or Open MPI installations or subprocess execution.
"""


class RunnerFactory(Protocol):
    """Callable interface for creating an `OrcaMmRunner` with a mocked execution result."""

    def __call__(
        self,
        *,
        returncode: int = 0,
        stdout: str = "",
        stderr: str = "",
    ) -> tuple[OrcaMmRunner, Mock]: ...


@pytest.fixture
def orca_mm_runner_factory(monkeypatch: pytest.MonkeyPatch) -> RunnerFactory:
    """Provide a factory for `OrcaMmRunner` instances with mocked execution.

    `OrcaMmRunner` discovers ORCA and Open MPI during initialization. Bypassing that
    discovery keeps these unit tests independent of machine configuration. The factory's
    `returncode`, `stdout`, and `stderr` arguments configure the result returned by the
    mocked `BaseRunner.run` method.
    """
    monkeypatch.setattr(OrcaMmRunner, "set_orca_path", Mock())
    monkeypatch.setattr(OrcaMmRunner, "set_open_mpi_path", Mock())

    def create_runner(
        *,
        returncode: int = 0,
        stdout: str = "",
        stderr: str = "",
    ) -> tuple[OrcaMmRunner, Mock]:
        """Create a runner and its execution mock with the configured result values."""
        runner = OrcaMmRunner()

        def execute(binary: OrcaBinary, args: Sequence[str] = (), /, **_kwargs) -> RunResult:
            """Return a configured result using the arguments actually received."""
            return RunResult(
                binary=binary.value,
                args=tuple(args),
                returncode=returncode,
                stdout=stdout,
                stderr=stderr,
            )

        mock_run = Mock(side_effect=execute)
        monkeypatch.setattr(runner, "run", mock_run)
        return runner, mock_run

    return create_runner


@pytest.mark.unit
def test_run_orca_mm_returns_successful_result(orca_mm_runner_factory: RunnerFactory) -> None:
    """Test that successful binary execution returns the expected result."""
    runner, mock_run = orca_mm_runner_factory()

    result = runner.run_orca_mm("convff", ["-amber", "test.prm"])

    assert result.returncode == 0
    assert result.stderr == ""
    assert mock_run.call_args.args[1] == ("-convff", "-amber", "test.prm")
    assert subprocess.PIPE in mock_run.call_args.kwargs["stderr"]


@pytest.mark.unit
def test_run_orca_mm_raises_on_nonzero_returncode(
    orca_mm_runner_factory: RunnerFactory,
) -> None:
    """Test that unsuccessful binary execution raises `OrcaMmError`."""
    runner, _ = orca_mm_runner_factory(returncode=1, stderr="orca_mm failed")

    with pytest.raises(OrcaMmError, match="orca_mm failed"):
        runner.run_orca_mm("convff", ["-amber", "test.prm"])
