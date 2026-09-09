from functools import partialmethod
from pathlib import Path

import pytest

from opi.core import Calculator
from opi.input import Input
from opi.input.blocks import BlockScf
from opi.input.simple_keywords import BasisSet, Dft, SimpleKeyword, Task
from opi.input.structures import Structure
from opi.simple_tasks import SinglePointTask
from opi.simple_tasks.simple_task import SimpleTask

"""
Unit tests for the four steps `SimpleTask.run()` delegates to:
- prepare_working_dir() strict / non-strict handling of the working directory
- make_input() returns a detached copy, so that the per-run resource overrides
  neither stick to the task nor leak into a later run
- make_calculator() assembles a Calculator without touching the filesystem
- run() orchestrates the steps and honours a subclass that overrides one of them

`make_results()` is covered by `test_simpletasks_status.py`, which asserts on the
method family it threads into the returned results object.
"""


@pytest.fixture
def structure() -> Structure:
    return Structure.from_lists(["H", "H"], [(0.0, 0.0, 0.0), (0.0, 0.0, 0.74)])


@pytest.fixture
def no_orca(monkeypatch: pytest.MonkeyPatch) -> None:
    """Skip contacting the ORCA binary, on `Calculator` construction and on execution alike.

    `SimpleTask.run()` does not expose the `version_check` of the `Calculator` that
    `make_calculator()` builds, so `version_check=False` is bound onto that step;
    `write_and_run` is stubbed separately since it always executes ORCA regardless of
    `version_check`.
    """
    monkeypatch.setattr(
        SimpleTask,
        "make_calculator",
        partialmethod(SimpleTask.make_calculator, version_check=False),
    )
    monkeypatch.setattr(Calculator, "write_and_run", lambda self: True)


# ---------------------------------------------------------------------------
# prepare_working_dir()
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.simpletasks
def test_prepare_working_dir_creates_missing_directory(tmp_path: Path) -> None:
    """Without `strict` a missing directory is created and returned."""
    task = SinglePointTask(method="pbe")
    working_dir = task.prepare_working_dir(tmp_path / "RUN")

    assert working_dir == tmp_path / "RUN"
    assert working_dir.is_dir()


@pytest.mark.unit
@pytest.mark.simpletasks
def test_prepare_working_dir_wipes_existing_directory(tmp_path: Path) -> None:
    """Without `strict` an existing directory is deleted and recreated empty."""
    working_dir = tmp_path / "RUN"
    working_dir.mkdir()
    (working_dir / "job.out").write_text("stale output")

    task = SinglePointTask(method="pbe")
    task.prepare_working_dir(working_dir)

    assert working_dir.is_dir()
    assert not any(working_dir.iterdir())


@pytest.mark.unit
@pytest.mark.simpletasks
def test_prepare_working_dir_accepts_a_string(tmp_path: Path) -> None:
    """A string path is normalised into a `Path`."""
    task = SinglePointTask(method="pbe")
    working_dir = task.prepare_working_dir(str(tmp_path / "RUN"))

    assert isinstance(working_dir, Path)
    assert working_dir.is_dir()


@pytest.mark.unit
@pytest.mark.simpletasks
def test_prepare_working_dir_strict_requires_existing_directory(tmp_path: Path) -> None:
    """In strict mode a missing directory is an error and nothing is created."""
    task = SinglePointTask(method="pbe")

    with pytest.raises(ValueError, match="does not exist"):
        task.prepare_working_dir(tmp_path / "RUN", strict=True)

    assert not (tmp_path / "RUN").exists()


@pytest.mark.unit
@pytest.mark.simpletasks
def test_prepare_working_dir_strict_requires_empty_directory(tmp_path: Path) -> None:
    """In strict mode a populated directory is an error and its content is kept."""
    working_dir = tmp_path / "RUN"
    working_dir.mkdir()
    (working_dir / "job.out").write_text("stale output")

    task = SinglePointTask(method="pbe")
    with pytest.raises(ValueError, match="is not empty"):
        task.prepare_working_dir(working_dir, strict=True)

    assert (working_dir / "job.out").read_text() == "stale output"


# ---------------------------------------------------------------------------
# make_input()
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.simpletasks
def test_make_input_returns_a_detached_copy() -> None:
    """The returned input carries the task's settings but is a separate object."""
    task = SinglePointTask(method="pbe", basis_set="def2-svp")
    input_object = task.make_input()

    assert input_object is not task.input
    assert input_object.has_simple_keywords(Task.SP, Dft.PBE, BasisSet.DEF2_SVP) == (
        True,
        True,
        True,
    )


@pytest.mark.unit
@pytest.mark.simpletasks
def test_make_input_copy_shares_no_block_with_the_task() -> None:
    """Editing a block on the returned input leaves the task's own block alone."""
    task = SinglePointTask(method="pbe")
    task.input.add_blocks(BlockScf(maxiter=300))

    input_object = task.make_input()
    input_object.blocks["scf"].maxiter = 99

    assert task.input.blocks["scf"].maxiter == 300


@pytest.mark.unit
@pytest.mark.simpletasks
def test_make_input_applies_resource_overrides() -> None:
    """`ncores` and `memory` are applied to the returned input."""
    task = SinglePointTask(method="pbe")
    input_object = task.make_input(ncores=8, memory=4096)

    assert input_object.ncores == 8
    assert input_object.memory == 4096


@pytest.mark.unit
@pytest.mark.simpletasks
def test_make_input_applies_moinp_override(tmp_path: Path) -> None:
    """`moinp` is applied to the returned input."""
    gbw_file = tmp_path / "job.gbw"
    gbw_file.write_bytes(b"")

    task = SinglePointTask(method="pbe")
    input_object = task.make_input(moinp=gbw_file)

    assert input_object.moinp == gbw_file.resolve()
    assert task.input.moinp is None


@pytest.mark.unit
@pytest.mark.simpletasks
def test_make_input_overrides_do_not_stick_to_the_task() -> None:
    """Per-run overrides stay on the returned copy instead of sticking to the task."""
    task = SinglePointTask(method="pbe")
    task.make_input(ncores=8, memory=4096)

    assert task.input.ncores is None
    assert task.input.memory is None


@pytest.mark.unit
@pytest.mark.simpletasks
def test_make_input_keeps_resources_held_by_the_task() -> None:
    """Values set on the task's own input are used whenever no override is given."""
    task = SinglePointTask(method="pbe")
    task.input.ncores = 2

    assert task.make_input().ncores == 2
    assert task.make_input(ncores=8).ncores == 8
    assert task.input.ncores == 2


# ---------------------------------------------------------------------------
# make_calculator()
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.simpletasks
def test_make_calculator_attaches_structure_and_input(tmp_path: Path, structure: Structure) -> None:
    """The calculator carries the basename, the structure and the task's input."""
    task = SinglePointTask(method="pbe", basis_set="def2-svp")
    calculator = task.make_calculator("job", structure, tmp_path, version_check=False)

    assert calculator.basename == "job"
    assert calculator.structure is structure
    assert calculator.input.has_simple_keywords(Task.SP, Dft.PBE) == (True, True)


@pytest.mark.unit
@pytest.mark.simpletasks
def test_make_calculator_writes_nothing(tmp_path: Path, structure: Structure) -> None:
    """Building the calculator leaves the working directory untouched."""
    task = SinglePointTask(method="pbe")
    task.make_calculator("job", structure, tmp_path, version_check=False)

    assert not any(tmp_path.iterdir())


@pytest.mark.unit
@pytest.mark.simpletasks
def test_make_calculator_forwards_resource_overrides(tmp_path: Path, structure: Structure) -> None:
    """The resource overrides are passed on to `make_input()`."""
    task = SinglePointTask(method="pbe")
    calculator = task.make_calculator(
        "job", structure, tmp_path, ncores=8, memory=4096, version_check=False
    )

    assert calculator.input.ncores == 8
    assert calculator.input.memory == 4096
    assert task.input.ncores is None


@pytest.mark.unit
@pytest.mark.simpletasks
def test_make_calculator_rejects_missing_working_dir(tmp_path: Path, structure: Structure) -> None:
    """`Calculator` requires the working directory to exist, hence prepare_working_dir()."""
    task = SinglePointTask(method="pbe")

    with pytest.raises(ValueError):
        task.make_calculator("job", structure, tmp_path / "RUN", version_check=False)


# ---------------------------------------------------------------------------
# run() — orchestration of the steps
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.simpletasks
def test_run_overrides_do_not_leak_into_the_next_run(
    tmp_path: Path, structure: Structure, no_orca: None
) -> None:
    """An `ncores` passed to one run() call is gone again by the next one."""
    task = SinglePointTask(method="pbe")

    first = task.run("job", structure, working_dir=tmp_path / "RUN", ncores=8)
    second = task.run("job", structure, working_dir=tmp_path / "RUN2")

    assert first.calculator.input.ncores == 8
    assert second.calculator.input.ncores is None


@pytest.mark.unit
@pytest.mark.simpletasks
def test_run_honours_overridden_steps(tmp_path: Path, structure: Structure, no_orca: None) -> None:
    """A subclass can hook into run() by overriding a single step."""
    executed: list[Calculator] = []

    class CustomTask(SinglePointTask):
        def make_input(
            self,
            ncores: int | None = None,
            memory: int | None = None,
            moinp: Path | None = None,
        ) -> Input:
            input_object = super().make_input(ncores=ncores, memory=memory, moinp=moinp)
            input_object.add_simple_keywords(SimpleKeyword("NORI"))
            return input_object

        def execute(self, calculator: Calculator) -> bool:
            executed.append(calculator)
            return True

    task = CustomTask(method="pbe")
    results = task.run("job", structure, working_dir=tmp_path / "RUN")

    assert len(executed) == 1
    assert executed[0].input.has_simple_keywords(SimpleKeyword("NORI")) == (True,)
    assert results.calculator is executed[0]
    # > The overridden execute() never runs ORCA, so nothing was written.
    assert not any((tmp_path / "RUN").iterdir())
