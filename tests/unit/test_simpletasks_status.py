import typing
from functools import partial
from pathlib import Path

import pytest

from opi.core import Calculator
from opi.input.structures import Structure
from opi.output.core import Output
from opi.simple_tasks import (
    DftSettings,
    ForceFieldSettings,
    MethodSettings,
    OptResults,
    OptTask,
    SinglePointResults,
    SinglePointTask,
    SqmSettings,
    simple_task,
)
from opi.simple_tasks.simple_task import TaskResults

"""
Unit tests for the method-specific job-completion checks wired up in
`TaskResults.status` / `OptResults.status`:
- TaskResults.status combines Output.terminated_normally() with
  MethodSettings.check_convergence()
- OptResults.status combines Output.geometry_optimization_converged() with
  MethodSettings.check_convergence() instead of terminated_normally()
- SimpleTask.run() picks the method family (or falls back to the base
  MethodSettings when raw `input=` bypassed the typed settings system) and
  threads it through to the returned TaskResults

`TaskResults.output` is monkeypatched to a bare, unparsed `Output` pointing at
a hand-written ``.out`` file, since the health-check methods it relies on
(`terminated_normally`, `scf_converged`, `geometry_optimization_converged`)
only need the raw output file, never `Output.parse()`.
"""

# > The health checks are unscoped, case-sensitive, per-line substring searches over
# > the whole ".out" file, so each fixture below is exactly the sentinel its check
# > greps for -- ORCA's surrounding banner text plays no part. Note the asterisks in
# > `TERMINATED_NORMALLY` are part of the searched string, unlike the other two.
# > `SCF_NOT_CONVERGED` is what ORCA prints when the SCF fails; that check keys off
# > the *absence* of "SUCCESS", so its content only has to not contain it.

SCF_CONVERGED = "SUCCESS\n"
SCF_NOT_CONVERGED = "SCF NOT CONVERGED AFTER 1 CYCLES\n"
OPT_CONVERGED = "HURRAY\n"
TERMINATED_NORMALLY = "****ORCA TERMINATED NORMALLY****\n"

_RT = typing.TypeVar("_RT", bound=TaskResults)


def _patch_output(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, contents: str) -> None:
    (tmp_path / "job.out").write_text(contents)
    output = Output("job", working_dir=tmp_path)
    monkeypatch.setattr(TaskResults, "output", property(lambda self: output))


def _make_results(results_type: type[_RT], method_family: type[MethodSettings]) -> _RT:
    """Build a results object for a status check.

    `calculator` is left unset because `_patch_output` replaces
    `TaskResults.output`, the only member that reads it.
    """
    return results_type(calculator=None, _method_family=method_family)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# TaskResults.status
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.simpletasks
def test_status_true_when_terminated_normally_and_scf_converged(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """SCF-based method family: status is True when both checks pass."""
    _patch_output(monkeypatch, tmp_path, SCF_CONVERGED + TERMINATED_NORMALLY)
    results = _make_results(SinglePointResults, DftSettings)
    assert results.status is True


@pytest.mark.unit
@pytest.mark.simpletasks
def test_status_false_when_not_terminated_normally(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Missing 'ORCA TERMINATED NORMALLY' fails status even if the SCF converged."""
    _patch_output(monkeypatch, tmp_path, SCF_CONVERGED)
    results = _make_results(SinglePointResults, DftSettings)
    assert results.status is False


@pytest.mark.unit
@pytest.mark.simpletasks
def test_status_false_when_scf_not_converged(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Normal termination with a non-converged SCF fails status for SCF-based methods."""
    _patch_output(monkeypatch, tmp_path, SCF_NOT_CONVERGED + TERMINATED_NORMALLY)
    results = _make_results(SinglePointResults, DftSettings)
    assert results.status is False


@pytest.mark.unit
@pytest.mark.simpletasks
def test_status_true_for_forcefield_without_scf(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """ForceFieldSettings has no SCF step, so status only requires normal termination."""
    _patch_output(monkeypatch, tmp_path, TERMINATED_NORMALLY)
    results = _make_results(SinglePointResults, ForceFieldSettings)
    assert results.status is True


# ---------------------------------------------------------------------------
# OptResults.status
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.simpletasks
def test_opt_status_true_when_optimization_and_method_converged(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """OptResults.status is True when geometry optimization and SCF both converged."""
    _patch_output(monkeypatch, tmp_path, SCF_CONVERGED + OPT_CONVERGED + TERMINATED_NORMALLY)
    results = _make_results(OptResults, DftSettings)
    assert results.status is True


@pytest.mark.unit
@pytest.mark.simpletasks
def test_opt_status_false_when_optimization_not_converged(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """OptResults.status is False without 'HURRAY', even if the SCF converged."""
    _patch_output(monkeypatch, tmp_path, SCF_CONVERGED + TERMINATED_NORMALLY)
    results = _make_results(OptResults, DftSettings)
    assert results.status is False


@pytest.mark.unit
@pytest.mark.simpletasks
def test_opt_status_false_when_method_check_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """OptResults.status is False when the geometry converged but the SCF did not."""
    _patch_output(monkeypatch, tmp_path, SCF_NOT_CONVERGED + OPT_CONVERGED + TERMINATED_NORMALLY)
    results = _make_results(OptResults, DftSettings)
    assert results.status is False


@pytest.mark.unit
@pytest.mark.simpletasks
def test_opt_status_true_for_forcefield_without_scf(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """ForceFieldSettings has no SCF step, so OptResults.status only needs 'HURRAY'."""
    _patch_output(monkeypatch, tmp_path, OPT_CONVERGED + TERMINATED_NORMALLY)
    results = _make_results(OptResults, ForceFieldSettings)
    assert results.status is True


@pytest.mark.unit
@pytest.mark.simpletasks
def test_opt_status_does_not_use_terminated_normally(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """OptResults.status ignores terminated_normally(): 'HURRAY' alone is enough."""
    _patch_output(monkeypatch, tmp_path, OPT_CONVERGED)
    results = _make_results(OptResults, MethodSettings)
    assert results.output.terminated_normally() is False
    assert results.status is True


# ---------------------------------------------------------------------------
# SimpleTask.run() — method family propagation
# ---------------------------------------------------------------------------


@pytest.fixture
def structure() -> Structure:
    return Structure.from_lists(["H", "H"], [(0.0, 0.0, 0.0), (0.0, 0.0, 0.74)])


@pytest.fixture
def no_orca(monkeypatch: pytest.MonkeyPatch) -> None:
    """Skip contacting the ORCA binary.

    `SimpleTask.run()` builds its own `Calculator` internally without exposing
    `version_check`, so the `version_check=False` convention used elsewhere in
    this suite (e.g. `test_input_blocks.py`) is applied by patching the name
    `simple_task` resolves at call time; `write_and_run` is stubbed separately
    since it always executes ORCA regardless of `version_check`.
    """
    monkeypatch.setattr(simple_task, "Calculator", partial(Calculator, version_check=False))
    monkeypatch.setattr(Calculator, "write_and_run", lambda self: True)


@pytest.mark.unit
@pytest.mark.simpletasks
def test_run_threads_method_family_from_method_settings(
    tmp_path: Path, structure: Structure, no_orca: None
) -> None:
    """run() passes the concrete MethodSettings subclass through to the results object."""
    task = SinglePointTask(method="pbe")
    results = task.run("job", structure, working_dir=tmp_path / "RUN")
    assert results._method_family is DftSettings


@pytest.mark.unit
@pytest.mark.simpletasks
def test_run_defaults_to_base_method_settings_with_raw_input(
    tmp_path: Path, structure: Structure, no_orca: None
) -> None:
    """Raw `input=` bypasses the typed settings system, so run() falls back to the
    base MethodSettings (whose check_convergence() always reports True)."""
    task = SinglePointTask(input="! SP PBE def2-SVP")
    assert task.method_settings is None
    results = task.run("job", structure, working_dir=tmp_path / "RUN")
    assert results._method_family is MethodSettings


@pytest.mark.unit
@pytest.mark.simpletasks
def test_run_threads_method_family_for_opt_task(
    tmp_path: Path, structure: Structure, no_orca: None
) -> None:
    """OptTask.run() also threads the method family through to OptResults."""
    task = OptTask(method="gfn2-xtb")
    results = task.run("job", structure, working_dir=tmp_path / "RUN")
    assert results._method_family is SqmSettings
