from pathlib import Path

import pytest
from pydantic import ValidationError

from opi.input.blocks import BlockScf
from opi.input.simple_keywords import BasisSet, Dft
from opi.input.simple_keywords.scf import Scf
from opi.output.core import Output
from opi.simple_tasks.method_settings import (
    DftSettings,
    DlpnoCcSettings,
    ForceFieldSettings,
    HFSettings,
    MethodSettings,
    SqmSettings,
    WftSettings,
)

"""
Unit tests for MethodSettings and its subclasses:
- Dispatcher (__new__) routing by method keyword
- resolve_method_settings_type classmethod
- DftSettings compound keyword parsing (e.g. "PBE-D3BJ")
- 3c method / ForceField cross-validation dropping basis_set
- scf_stab flag adding SCFSTAB keyword
- Settings merge operator (|)
- Invalid field rejection
- check_convergence: SCF-based method families defer to Output.scf_converged(),
  ForceFieldSettings (no SCF step) always reports True
"""


@pytest.mark.unit
@pytest.mark.simpletasks
@pytest.mark.parametrize(
    "method,expected_cls",
    [
        ("pbe", DftSettings),
        ("gfn2-xtb", SqmSettings),
        ("ccsd(t)", WftSettings),
        ("hf", WftSettings),
        ("gfn-ff", ForceFieldSettings),
    ],
)
def test_method_settings_dispatch(method: str, expected_cls: type) -> None:
    """MethodSettings(method=X) returns the correct concrete subclass."""
    settings = MethodSettings(method=method)
    assert isinstance(settings, expected_cls)


@pytest.mark.unit
@pytest.mark.simpletasks
@pytest.mark.parametrize(
    "method,expected_cls",
    [
        ("pbe", DftSettings),
        ("gfn2-xtb", SqmSettings),
        ("ccsd(t)", WftSettings),
        ("gfn-ff", ForceFieldSettings),
    ],
)
def test_resolve_method_settings_type(method: str, expected_cls: type) -> None:
    """resolve_method_settings_type returns the correct class for each method family."""
    assert MethodSettings.resolve_method_settings_type(method) is expected_cls


@pytest.mark.unit
@pytest.mark.simpletasks
def test_dft_compound_keyword_parsed() -> None:
    """DftSettings splits 'Functional-Dispersion' compound strings like 'PBE-D3BJ'
    into separate `method` and `disp_correction` fields."""
    s = DftSettings(method="PBE-D3BJ")
    assert s.method is not None
    assert s.method.keyword.lower() == "pbe"
    assert s.disp_correction is not None
    assert s.disp_correction.keyword.lower() == "d3bj"


@pytest.mark.unit
@pytest.mark.simpletasks
def test_dft_compound_keyword_multi_dash_functional() -> None:
    """Splitting only on the last '-' handles functionals that themselves contain a dash."""
    s = DftSettings(method="CAM-B3LYP-D3BJ")
    assert s.method is not None
    assert s.method.keyword.lower() == "cam-b3lyp"
    assert s.disp_correction is not None
    assert s.disp_correction.keyword.lower() == "d3bj"


@pytest.mark.unit
@pytest.mark.simpletasks
def test_dft_functional_with_builtin_dispersion_not_split() -> None:
    """Functionals whose registered keyword already contains a dash (and dispersion
    baked into the name) are left untouched rather than being split apart."""
    s = DftSettings(method="wb97x-d3bj")
    assert s.method is not None
    assert s.method.keyword.lower() == "wb97x-d3bj"
    assert s.disp_correction is None


@pytest.mark.unit
@pytest.mark.simpletasks
def test_dft_explicit_disp_correction() -> None:
    """disp_correction can be set directly alongside a plain method."""
    s = DftSettings(method="PBE", disp_correction="D4")
    assert s.method is not None
    assert s.method.keyword.lower() == "pbe"
    assert s.disp_correction is not None
    assert s.disp_correction.keyword.lower() == "d4"


@pytest.mark.unit
@pytest.mark.simpletasks
def test_dft_conflicting_disp_correction_raises() -> None:
    """A compound method string that disagrees with an explicit disp_correction raises."""
    with pytest.raises(ValidationError):
        DftSettings(method="PBE-D3BJ", disp_correction="D4")


@pytest.mark.unit
@pytest.mark.simpletasks
def test_dft_invalid_compound_keyword_raises() -> None:
    """DftSettings raises ValidationError for unrecognised compound method strings."""
    with pytest.raises(ValidationError):
        DftSettings(method="INVALID-NOTALLOWED")


@pytest.mark.unit
@pytest.mark.simpletasks
def test_dft_3c_method_drops_basis_set_with_warning() -> None:
    """3c composite methods silently drop basis_set (they carry their own basis internally)."""
    with pytest.warns(UserWarning):
        s = DftSettings(method="r2scan-3c", basis_set="def2-svp")
    assert s.basis_set is None


@pytest.mark.unit
@pytest.mark.simpletasks
def test_forcefield_drops_basis_set_with_warning() -> None:
    """ForceFieldSettings silently drops basis_set because force fields have no QM basis."""
    with pytest.warns(UserWarning):
        s = ForceFieldSettings(method="gfn-ff", basis_set="def2-svp")
    assert s.basis_set is None


@pytest.mark.unit
@pytest.mark.simpletasks
def test_dft_scf_stab_adds_scfstab_keyword() -> None:
    """DftSettings with scf_stab=True adds the SCFSTAB keyword to the input."""
    s = DftSettings(method="pbe", scf_stab=True)
    inp = s.map_to_input()
    assert inp.has_simple_keywords(Scf.SCFSTAB) == (True,)


@pytest.mark.unit
@pytest.mark.simpletasks
def test_dft_scf_stab_false_no_scfstab_keyword() -> None:
    """DftSettings with scf_stab=False (default) does not add SCFSTAB."""
    s = DftSettings(method="pbe")
    inp = s.map_to_input()
    assert inp.has_simple_keywords(Scf.SCFSTAB) == (False,)


@pytest.mark.unit
@pytest.mark.simpletasks
def test_settings_merge_right_wins_left_preserved() -> None:
    """Settings | other: right-hand fields override, unset left-hand fields are preserved."""
    s1 = DftSettings(method="pbe", basis_set="def2-svp")
    s2 = DftSettings(method="tpss")
    merged_settings = s1 | s2
    assert merged_settings.method == Dft.TPSS
    assert merged_settings.basis_set == BasisSet.DEF2_SVP


@pytest.mark.unit
@pytest.mark.simpletasks
def test_settings_merge_right_overrides_both() -> None:
    """Settings | other: right-hand basis_set overrides left-hand basis_set."""
    s1 = DftSettings(method="pbe", basis_set="def2-svp")
    s2 = DftSettings(method="tpss", basis_set="def2-tzvp")
    merged = s1 | s2
    assert merged.method == Dft.TPSS
    assert merged.basis_set == BasisSet.DEF2_TZVP


@pytest.mark.unit
@pytest.mark.simpletasks
def test_dft_invalid_field_raises_validation_error() -> None:
    """DftSettings rejects unknown fields with a clear ValidationError."""
    with pytest.raises(ValidationError):
        DftSettings(method="pbe", invalid_field="x")  # type: ignore[call-arg]


@pytest.mark.unit
@pytest.mark.simpletasks
@pytest.mark.parametrize(
    "field,text_value,expected_kw",
    [
        ("method", "pbe", Dft.PBE),
        ("method", "PBE", Dft.PBE),
        ("basis_set", "def2-svp", BasisSet.DEF2_SVP),
        ("basis_set", "DEF2-SVP", BasisSet.DEF2_SVP),
    ],
)
def test_string_fields_converted_to_simple_keyword(
    field: str, text_value: str, expected_kw: object
) -> None:
    """String field values are validated and converted to the matching SimpleKeyword (case-insensitively)."""
    s = DftSettings(**{field: text_value})  # type: ignore[arg-type]
    assert getattr(s, field) == expected_kw


@pytest.mark.unit
@pytest.mark.simpletasks
@pytest.mark.parametrize(
    "settings_cls,settings_kwargs,field,value,block_attr",
    [
        (DftSettings, {"method": "pbe", "scf_maxiter": 300}, "scf_maxiter", 300, "maxiter"),
        (SqmSettings, {"method": "gfn2-xtb", "scf_maxiter": 500}, "scf_maxiter", 500, "maxiter"),
    ],
)
def test_block_option_stored_and_mapped(
    settings_cls: type,
    settings_kwargs: dict,  # type: ignore[type-arg]
    field: str,
    value: int,
    block_attr: str,
) -> None:
    """Block-option fields are stored in settings and map to the correct block attribute in the input."""
    s = settings_cls(**settings_kwargs)
    assert getattr(s, field) == value

    inp = s.map_to_input()
    assert inp.has_blocks(BlockScf()) == (True,)
    assert getattr(inp.blocks["scf"], block_attr) == value


@pytest.mark.unit
@pytest.mark.simpletasks
def test_base_method_settings_check_convergence_defaults_true(tmp_path: Path) -> None:
    """MethodSettings.check_convergence() with no override is True regardless of the output."""
    (tmp_path / "job.out").write_text("nothing SCF related in here")
    output = Output("job", working_dir=tmp_path)
    assert MethodSettings.check_convergence(output) is True


@pytest.mark.unit
@pytest.mark.simpletasks
def test_force_field_check_convergence_ignores_missing_scf(tmp_path: Path) -> None:
    """ForceFieldSettings has no SCF step, so check_convergence() stays True without a 'SUCCESS' line."""
    (tmp_path / "job.out").write_text("force field run, no SCF here")
    output = Output("job", working_dir=tmp_path)
    assert ForceFieldSettings.check_convergence(output) is True


@pytest.mark.unit
@pytest.mark.simpletasks
@pytest.mark.parametrize(
    "settings_cls",
    [DftSettings, SqmSettings, WftSettings, HFSettings, DlpnoCcSettings],
)
@pytest.mark.parametrize(
    "out_contents,expected",
    [
        ("SCF ITERATIONS\n... SUCCESS ...", True),
        ("SCF ITERATIONS\n... did not converge ...", False),
    ],
)
def test_scf_based_check_convergence_matches_scf_converged(
    tmp_path: Path,
    settings_cls: type[MethodSettings],
    out_contents: str,
    expected: bool,
) -> None:
    """SCF-based method families report check_convergence() based on Output.scf_converged()."""
    (tmp_path / "job.out").write_text(out_contents)
    output = Output("job", working_dir=tmp_path)
    assert settings_cls.check_convergence(output) is expected
