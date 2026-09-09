import pytest

from opi.input import Input
from opi.input.arbitrary_string import ArbitraryStringPos
from opi.input.blocks import BlockGeom, BlockScf
from opi.input.simple_keywords import BasisSet, Dft, Goat, SimpleKeyword, Task
from opi.input.simple_keywords.opt import Opt
from opi.simple_tasks import (
    EngradTask,
    FreqTask,
    GoatSettings,
    GoatTask,
    OptSettings,
    OptTask,
    SinglePointTask,
)
from opi.simple_tasks.method_settings import DftSettings, SqmSettings

"""
Unit tests for SimpleTask subclasses and TaskSettings:
- Constructor argument validation (method dispatch, dict args, no-method error)
- input builds correct simple keywords for each task type
- OptSettings flag combinations (opt_h / lopt / optrigid / opt_maxiter)
- GoatSettings boolean flags (goat_react / goat_diversity / goat_explore)
- OptTask convenience property forwarding to task_settings
- Method-family switching (same family and cross-family)
- basis_set getter / setter round-trip
"""


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.simpletasks
def test_simple_task_no_method_raises() -> None:
    """Creating a task without a method or method_settings raises ValueError."""
    with pytest.raises(ValueError):
        SinglePointTask()


@pytest.mark.unit
@pytest.mark.simpletasks
@pytest.mark.parametrize(
    "method,expected_cls",
    [
        ("pbe", DftSettings),
        ("gfn2-xtb", SqmSettings),
    ],
)
def test_simple_task_method_dispatch(method: str, expected_cls: type) -> None:
    """Task constructor routes to the correct MethodSettings subclass by method string."""
    task = SinglePointTask(method=method)
    assert isinstance(task.method_settings, expected_cls)


@pytest.mark.unit
@pytest.mark.simpletasks
def test_simple_task_dict_method_settings() -> None:
    """A plain dict passed as method_settings is validated and dispatched correctly."""
    task = SinglePointTask(method_settings={"method": "pbe"})
    assert isinstance(task.method_settings, DftSettings)


@pytest.mark.unit
@pytest.mark.simpletasks
def test_simple_task_dict_task_settings() -> None:
    """A plain dict passed as task_settings is validated against the task's settings type."""
    task = SinglePointTask(method="pbe", task_settings={})
    assert task.task_settings is not None


# ---------------------------------------------------------------------------
# input — task keyword
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.simpletasks
@pytest.mark.parametrize(
    "task_cls,expected_kw",
    [
        (SinglePointTask, Task.SP),
        (OptTask, Task.OPT),
        (FreqTask, Task.FREQ),
        (EngradTask, Task.ENGRAD),
        (GoatTask, Goat.GOAT),
    ],
)
def test_input_has_task_keyword(task_cls: type, expected_kw: SimpleKeyword) -> None:
    """input contains the primary task keyword for each task type."""
    inp = task_cls(method="pbe").input
    assert inp.has_simple_keywords(expected_kw) == (True,)


@pytest.mark.unit
@pytest.mark.simpletasks
def test_input_has_method_and_basis_set() -> None:
    """input contains the task keyword, method, and basis-set keywords."""
    inp = SinglePointTask(method="pbe", basis_set="def2-svp").input
    assert inp.has_simple_keywords(Task.SP, Dft.PBE, BasisSet.DEF2_SVP) == (True, True, True)


# ---------------------------------------------------------------------------
# OptSettings.map_to_input — flag combinations
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.simpletasks
@pytest.mark.parametrize(
    "opt_h,lopt,expected_kw",
    [
        (True, False, Opt.OPTH),
        (False, True, Opt.L_OPT),
        (True, True, Opt.L_OPTH),
    ],
)
def test_opt_mode_keywords(opt_h: bool, lopt: bool, expected_kw: SimpleKeyword) -> None:
    """OptSettings flag combinations map to the correct ORCA optimisation-mode keyword."""
    inp = OptSettings(opt_h=opt_h, lopt=lopt).map_to_input()
    assert inp.has_simple_keywords(expected_kw) == (True,)


@pytest.mark.unit
@pytest.mark.simpletasks
def test_opt_no_mode_flags_adds_no_mode_keyword() -> None:
    """Default OptSettings (no flags) does not add OPT_H / L_OPT / L_OPT_H."""
    inp = OptSettings().map_to_input()
    for kw in (Opt.OPTH, Opt.L_OPT, Opt.L_OPTH):
        assert inp.has_simple_keywords(kw) == (False,)


@pytest.mark.unit
@pytest.mark.simpletasks
def test_opt_rigid_body_keyword() -> None:
    """OptSettings(optrigid=True) adds the RIGIDBODYOPT keyword."""
    inp = OptSettings(optrigid=True).map_to_input()
    assert inp.has_simple_keywords(Opt.RIGIDBODYOPT) == (True,)


@pytest.mark.unit
@pytest.mark.simpletasks
def test_opt_maxiter_creates_geom_block() -> None:
    """OptSettings(opt_maxiter=N) creates a %geom block with MaxIter set."""
    inp = OptSettings(opt_maxiter=100).map_to_input()
    assert inp.has_blocks(BlockGeom) == (True,)
    assert inp.blocks["geom"].maxiter == 100


# ---------------------------------------------------------------------------
# GoatSettings.map_to_input — boolean flags
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.simpletasks
@pytest.mark.parametrize(
    "flag,expected_kw",
    [
        ("goat_react", Goat.GOAT_REACT),
        ("goat_diversity", Goat.GOAT_DIVERSITY),
        ("goat_explore", Goat.GOAT_EXPLORE),
    ],
)
def test_goat_flag_keywords(flag: str, expected_kw: SimpleKeyword) -> None:
    """GoatSettings boolean flags produce the correct ORCA GOAT-variant keyword."""
    inp = GoatSettings(**{flag: True}).map_to_input()
    assert inp.has_simple_keywords(expected_kw) == (True,)


# ---------------------------------------------------------------------------
# OptTask convenience property forwarding
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.simpletasks
def test_opt_task_properties_forward_to_task_settings() -> None:
    """Setting OptTask properties propagates to the underlying OptSettings object."""
    opt = OptTask(method="pbe")

    opt.optrigid = True
    assert opt.task_settings.optrigid is True

    opt.opt_h = True
    assert opt.task_settings.opt_h is True

    opt.lopt = True
    assert opt.task_settings.lopt is True

    opt.opt_maxiter = 100
    assert opt.task_settings.opt_maxiter == 100


# ---------------------------------------------------------------------------
# Method switching
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.simpletasks
def test_method_switch_same_family_updates_in_place() -> None:
    """Switching to a method in the same family updates the existing settings object."""
    task = SinglePointTask(method="pbe")
    task.method = "tpss"
    assert isinstance(task.method_settings, DftSettings)
    assert task.method == Dft.TPSS


@pytest.mark.unit
@pytest.mark.simpletasks
def test_method_switch_cross_family_warns_about_dropped_fields() -> None:
    """Switching method family warns about settings fields that cannot be transferred."""
    task = SinglePointTask(method_settings=DftSettings(method="pbe", scf_maxiter=500))
    with pytest.warns(UserWarning, match="scf_maxiter"):
        task.method = "gfn2-xtb"
    assert isinstance(task.method_settings, SqmSettings)


# ---------------------------------------------------------------------------
# basis_set getter / setter
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.simpletasks
def test_basis_set_getter_and_setter() -> None:
    """basis_set property reads and writes through to method_settings correctly."""
    task = SinglePointTask(method="pbe", basis_set="def2-svp")
    assert task.basis_set == BasisSet.DEF2_SVP

    task.basis_set = "def2-tzvp"
    assert task.basis_set == BasisSet.DEF2_TZVP


# ---------------------------------------------------------------------------
# input caching
# ---------------------------------------------------------------------------


# @pytest.mark.unit
# @pytest.mark.simpletasks
# def test_input_is_cached() -> None:
#     """Accessing input twice returns the same object instance."""
#     task = SinglePointTask(method="pbe")
#     assert task.input is task.input


@pytest.mark.unit
@pytest.mark.simpletasks
def test_user_added_keyword_persists() -> None:
    """A keyword added directly to input is visible on every subsequent access."""
    task = SinglePointTask(method="pbe")
    kw = SimpleKeyword("NORI")
    task.input.add_simple_keywords(kw)
    assert task.input.has_simple_keywords(kw) == (True,)
    assert task.input.has_simple_keywords(kw) == (True,)


@pytest.mark.unit
@pytest.mark.simpletasks
def test_user_added_block_persists() -> None:
    """A block added directly to input is visible on every subsequent access."""
    task = SinglePointTask(method="pbe")
    block = BlockScf(maxiter=500)
    task.input.add_blocks(block)
    assert task.input.has_blocks(BlockScf()) == (True,)
    assert task.input.blocks["scf"].maxiter == 500


@pytest.mark.unit
@pytest.mark.simpletasks
def test_settings_block_option_restored_after_user_modification() -> None:
    """A settings-controlled block option modified on input is restored on the next access."""
    task = OptTask(method="pbe", task_settings={"opt_maxiter": 50})
    task.input.blocks["geom"].maxiter = 99
    assert task.input.blocks["geom"].maxiter == 50


@pytest.mark.unit
@pytest.mark.simpletasks
def test_settings_keyword_restored_after_user_removal() -> None:
    """A method-controlled keyword removed from input is re-added on the next access."""
    task = SinglePointTask(method="pbe", basis_set="def2-svp")
    task.input.remove_simple_keywords(BasisSet.DEF2_SVP)
    assert task.input.has_simple_keywords(BasisSet.DEF2_SVP) == (True,)


@pytest.mark.unit
@pytest.mark.simpletasks
def test_user_set_ncores_persists() -> None:
    """Setting ncores on input is preserved across accesses."""
    task = SinglePointTask(method="pbe")
    task.input.ncores = 8
    assert task.input.ncores == 8


@pytest.mark.unit
@pytest.mark.simpletasks
def test_user_set_memory_persists() -> None:
    """Setting memory on input is preserved across accesses."""
    task = SinglePointTask(method="pbe")
    task.input.memory = 4096
    assert task.input.memory == 4096


@pytest.mark.unit
@pytest.mark.simpletasks
def test_user_added_arbitrary_string_persists() -> None:
    """An arbitrary string added to input is preserved across accesses."""
    task = SinglePointTask(method="pbe")
    task.input.add_arbitrary_string("% some custom block\nend", pos=ArbitraryStringPos.BOTTOM)
    assert len(task.input.arbitrary_strings) == 1
    assert len(task.input.arbitrary_strings) == 1


@pytest.mark.unit
@pytest.mark.simpletasks
def test_multiple_user_modifications_all_persist() -> None:
    """Multiple independent modifications to input all survive repeated accesses."""
    task = SinglePointTask(method="pbe")
    kw = SimpleKeyword("RIJCOSX")
    block = BlockScf(maxiter=300)

    task.input.add_simple_keywords(kw)
    task.input.add_blocks(block)
    task.input.ncores = 4

    inp = task.input
    assert inp.has_simple_keywords(kw) == (True,)
    assert inp.has_blocks(BlockScf()) == (True,)
    assert inp.blocks["scf"].maxiter == 300
    assert inp.ncores == 4


# ---------------------------------------------------------------------------
# expert mode — an input passed at init takes precedence
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.simpletasks
def test_expert_mode_adds_no_default_settings() -> None:
    """An input passed on its own bypasses the typed settings system entirely."""
    inp = Input()
    inp.add_simple_keywords(SimpleKeyword("B3LYP"))
    task = SinglePointTask(input=inp)

    assert task.task_settings is None
    assert task.method_settings is None
    assert task.input.has_simple_keywords(Task.SP) == (False,)


@pytest.mark.unit
@pytest.mark.simpletasks
def test_expert_mode_applies_settings_passed_alongside_input() -> None:
    """Settings given next to an input are still applied on top of it."""
    task = SinglePointTask(method="pbe", basis_set="def2-svp", input=Input())

    assert task.input.has_simple_keywords(Dft.PBE, BasisSet.DEF2_SVP) == (True, True)


@pytest.mark.unit
@pytest.mark.simpletasks
def test_expert_mode_input_block_option_wins_over_settings() -> None:
    """A block option set in the input passed at init overrides the settings."""
    inp = Input()
    inp.add_blocks(BlockGeom(maxiter=99))
    task = OptTask(method="pbe", task_settings={"opt_maxiter": 50}, input=inp)

    assert task.input.blocks["geom"].maxiter == 99
    # > Re-accessing re-does the merge, so the input has to keep winning.
    assert task.input.blocks["geom"].maxiter == 99


@pytest.mark.unit
@pytest.mark.simpletasks
def test_expert_mode_input_ncores_wins_over_settings() -> None:
    """`ncores` set in the input passed at init survives the merge with the settings."""
    inp = Input()
    inp.ncores = 8
    task = SinglePointTask(method="pbe", input=inp)

    assert task.input.ncores == 8
    assert task.input.ncores == 8
