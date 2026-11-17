"""
This module contains tests for `OrcaMmRunner` command execution such as:
- Returning successful execution results
- Raising `OrcaMmError` with the captured STDERR after unsuccessful execution
- Passing command arguments and stream targets to `BaseRunner.run`
- Rejecting missing input files
- Verifying that expected output files are generated

ORCA discovery and binary execution are mocked so that these tests do not
depend on external ORCA or Open MPI installations or subprocess execution.
"""

import subprocess
from pathlib import Path
from typing import Protocol, Sequence
from unittest.mock import Mock

import pytest

from opi.exceptions import OrcaMmError
from opi.execution.base import RunResult
from opi.execution.orca_mm import OrcaMmRunner
from opi.lib.orca_binary import OrcaBinary


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
    # > Real `orca_mm` error output, distinct from the fixed text of the error message.
    stderr = "Error (ORCA_MM): Forcefield filename not assigned."
    runner, _ = orca_mm_runner_factory(returncode=1, stderr=stderr)

    with pytest.raises(OrcaMmError) as exc_info:
        runner.run_orca_mm("convff", ["-amber", "test.prm"])

    message = str(exc_info.value)
    assert stderr in message
    assert "orca_mm -convff -amber test.prm" in message


@pytest.mark.unit
def test_command_rejects_missing_input_file(
    orca_mm_runner_factory: RunnerFactory,
    tmp_path: Path,
) -> None:
    """Test that command helpers reject missing input files before execution."""
    runner, mock_run = orca_mm_runner_factory()
    missing_input = tmp_path / "missing.xyz"

    with pytest.raises(FileNotFoundError, match="Input file.*missing.xyz"):
        runner.run_get_h_dist(missing_input)

    mock_run.assert_not_called()


@pytest.mark.unit
def test_command_raises_when_expected_output_is_missing(
    orca_mm_runner_factory: RunnerFactory,
    tmp_path: Path,
) -> None:
    """Test that command helpers verify their expected outputs after execution."""
    runner, mock_run = orca_mm_runner_factory()
    structure_file = tmp_path / "structure.xyz"
    structure_file.touch()

    with pytest.raises(FileNotFoundError, match="Expected output file.*H_DIST.prms"):
        runner.run_get_h_dist(structure_file)

    mock_run.assert_called_once()


@pytest.mark.unit
def test_command_resolves_relative_paths_against_working_dir(
    orca_mm_runner_factory: RunnerFactory,
    tmp_path: Path,
) -> None:
    """Test that relative input paths are resolved against `working_dir`, not the process CWD."""
    runner, mock_run = orca_mm_runner_factory()
    runner.working_dir = tmp_path
    (tmp_path / "structure.xyz").touch()
    (tmp_path / "structure.H_DIST.prms").touch()

    result = runner.run_get_h_dist("structure.xyz")

    assert result == tmp_path / "structure.H_DIST.prms"
    assert mock_run.call_args.args[1] == ("-getHDist", str(tmp_path / "structure.xyz"))


@pytest.mark.unit
@pytest.mark.parametrize("method", ["run_splitff", "run_splitpdb"])
def test_split_rejects_split_point_at_first_atom(
    orca_mm_runner_factory: RunnerFactory,
    tmp_path: Path,
    method: str,
) -> None:
    """Test that splitting at atom 1, which would leave an empty first part, is rejected."""
    runner, mock_run = orca_mm_runner_factory()
    source = tmp_path / "system.ORCAFF.prms"
    source.touch()

    with pytest.raises(ValueError, match="greater than 1"):
        getattr(runner, method)(source, 1, 4)

    mock_run.assert_not_called()


@pytest.mark.unit
def test_splitff_deduplicates_and_sorts_split_points(
    orca_mm_runner_factory: RunnerFactory,
    tmp_path: Path,
) -> None:
    """Test that duplicate split points are removed and the rest are passed in order."""
    runner, mock_run = orca_mm_runner_factory()
    source = tmp_path / "system.ORCAFF.prms"
    source.touch()
    expected = [tmp_path / f"system_split{i}.ORCAFF.prms" for i in (1, 2, 3)]
    for path in expected:
        path.touch()

    result = runner.run_splitff(source, 7, 4, 7)

    assert result == expected
    assert mock_run.call_args.args[1] == ("-splitff", str(source), "4", "7")


def _touch(*paths: Path) -> None:
    """Create empty files standing in for `orca_mm` inputs or outputs."""
    for path in paths:
        path.touch()


# > The expected output names below were checked against the real `orca_mm` binary.


@pytest.mark.unit
def test_makeff_assembles_options(orca_mm_runner_factory: RunnerFactory, tmp_path: Path) -> None:
    """Test that `run_makeff` passes all options in `orca_mm` syntax."""
    runner, mock_run = orca_mm_runner_factory()
    structure = tmp_path / "complex.xyz"
    _touch(structure, tmp_path / "complex.ORCAFF.prms")

    result = runner.run_makeff(
        structure,
        charge=-1,
        multiplicity=2,
        nproc=4,
        charge_option="XTB",
        oxidation_states={"Fe": 3},
    )

    assert result == tmp_path / "complex.ORCAFF.prms"
    assert mock_run.call_args.args[1] == (
        "-makeff",
        str(structure),
        "-C",
        "-1",
        "-M",
        "2",
        "-nproc",
        "4",
        "-XTB",
        "-CEL",
        "Fe",
        "3.0",
    )


@pytest.mark.unit
def test_convff_derives_output_from_first_file(
    orca_mm_runner_factory: RunnerFactory, tmp_path: Path
) -> None:
    """Test that `run_convff` names its output after the first forcefield file."""
    runner, mock_run = orca_mm_runner_factory()
    psf = tmp_path / "1C1E.psf"
    prm = tmp_path / "par_all36_prot.prm"
    _touch(psf, prm)

    def create_output(*_args: object, **_kwargs: object) -> RunResult:
        _touch(tmp_path / "1C1E.ORCAFF.prms")
        return RunResult(binary="orca_mm", args=(), returncode=0, stdout="", stderr="")

    mock_run.side_effect = create_output

    result = runner.run_convff("charmm", [psf, prm])

    assert result == tmp_path / "1C1E.ORCAFF.prms"
    assert mock_run.call_args.args[1] == ("-convff", "-charmm", str(psf), str(prm))


@pytest.mark.unit
def test_convff_reuses_existing_output_unless_forced(
    orca_mm_runner_factory: RunnerFactory, tmp_path: Path
) -> None:
    """Test that an existing forcefield is reused, and regenerated only with `force=True`."""
    runner, mock_run = orca_mm_runner_factory()
    prmtop = tmp_path / "complex.prmtop"
    output = tmp_path / "complex.ORCAFF.prms"
    _touch(prmtop, output)

    assert runner.run_convff("amber", [prmtop]) == output
    mock_run.assert_not_called()

    # > The stale output is removed first, so a run that creates nothing must fail.
    with pytest.raises(FileNotFoundError, match="Expected output file"):
        runner.run_convff("amber", [prmtop], force=True)
    mock_run.assert_called_once()


@pytest.mark.unit
def test_repeatff_output_name(orca_mm_runner_factory: RunnerFactory, tmp_path: Path) -> None:
    """Test that `run_repeatff` passes the repeat count and expects `_repeat<N>` output."""
    runner, mock_run = orca_mm_runner_factory()
    source = tmp_path / "water.ORCAFF.prms"
    _touch(source, tmp_path / "water_repeat3.ORCAFF.prms")

    result = runner.run_repeatff(source, 3)

    assert result == tmp_path / "water_repeat3.ORCAFF.prms"
    assert mock_run.call_args.args[1] == ("-repeatff", str(source), "3")


@pytest.mark.unit
def test_mergeff_output_name(orca_mm_runner_factory: RunnerFactory, tmp_path: Path) -> None:
    """Test that `run_mergeff` keeps the input order and names the output after the first file."""
    runner, mock_run = orca_mm_runner_factory()
    first = tmp_path / "water_split1.ORCAFF.prms"
    second = tmp_path / "water_split2.ORCAFF.prms"
    _touch(first, second, tmp_path / "water_split1_merged.ORCAFF.prms")

    result = runner.run_mergeff(first, second)

    assert result == tmp_path / "water_split1_merged.ORCAFF.prms"
    assert mock_run.call_args.args[1] == ("-mergeff", str(first), str(second))


@pytest.mark.unit
def test_splitpdb_output_names(orca_mm_runner_factory: RunnerFactory, tmp_path: Path) -> None:
    """Test that `run_splitpdb` expects one `_split<N>.pdb` file per part."""
    runner, mock_run = orca_mm_runner_factory()
    pdb = tmp_path / "protein.pdb"
    expected = [tmp_path / "protein_split1.pdb", tmp_path / "protein_split2.pdb"]
    _touch(pdb, *expected)

    result = runner.run_splitpdb(pdb, 5)

    assert result == expected
    assert mock_run.call_args.args[1] == ("-splitpdb", str(pdb), "5")


@pytest.mark.unit
def test_mergepdb_output_name(orca_mm_runner_factory: RunnerFactory, tmp_path: Path) -> None:
    """Test that `run_mergepdb` names the output after the first file."""
    runner, mock_run = orca_mm_runner_factory()
    first = tmp_path / "protein.pdb"
    second = tmp_path / "ligand.pdb"
    _touch(first, second, tmp_path / "protein_merged.pdb")

    result = runner.run_mergepdb(first, second)

    assert result == tmp_path / "protein_merged.pdb"
    assert mock_run.call_args.args[1] == ("-mergepdb", str(first), str(second))


@pytest.mark.unit
def test_get_h_dist_keeps_dots_in_stem(
    orca_mm_runner_factory: RunnerFactory, tmp_path: Path
) -> None:
    """Test that only the last suffix is replaced for filenames containing dots."""
    runner, _ = orca_mm_runner_factory()
    structure = tmp_path / "my.mol.xyz"
    _touch(structure, tmp_path / "my.mol.H_DIST.prms")

    assert runner.run_get_h_dist(structure) == tmp_path / "my.mol.H_DIST.prms"
