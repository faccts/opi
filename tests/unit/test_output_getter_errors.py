"""
Unit tests for the errors raised by the `Output` getters.

The getters return None if a value is not in the output, but raise if they are used incorrectly:
- `OpiOutputNotParsedError` if the JSON files were not parsed
- `OpiOutputIndexError` if the requested geometry or gbw index does not exist
- `OpiOutputMissingValueError` for any missing value if `raise_on_missing` is set
"""

import pytest

from opi.core import Calculator
from opi.exceptions import OpiOutputIndexError, OpiOutputMissingValueError, OpiOutputNotParsedError
from opi.output.core import Output


@pytest.mark.unit
@pytest.mark.output
def test_not_parsed_error_points_to_parse(empty_output_object: Output):
    """Test that the error for unparsed output tells the user to call `Output.parse()`."""
    with pytest.raises(OpiOutputNotParsedError, match=r"Output\.parse\(\)"):
        empty_output_object.get_dipole()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["led"])
def test_not_parsed_error_for_gbw_results_only(output_object_factory, task: str):
    """Test that only gbw getters raise if just the gbw JSON was not parsed."""
    output_object = output_object_factory(task)
    output_object.results_gbw = None
    with pytest.raises(OpiOutputNotParsedError, match="gbw"):
        output_object.get_mos()
    assert output_object.get_dipole() is not None


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["led"])
def test_index_error_for_gbw_index(output_object_factory, task: str):
    """Test that a gbw index out of range raises `OpiOutputIndexError`."""
    output_object = output_object_factory(task)
    with pytest.raises(OpiOutputIndexError, match="gbw results"):
        output_object.get_mos(gbw_index=len(output_object.results_gbw))


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["led"])
def test_index_error_for_negative_index(output_object_factory, task: str):
    """Test that negative indices work within range and raise `OpiOutputIndexError` outside of it."""
    output_object = output_object_factory(task)
    n_geometries = len(output_object.results_properties.geometries)
    assert output_object.get_dipole(index=-n_geometries) is not None
    with pytest.raises(OpiOutputIndexError, match="geometries"):
        output_object.get_dipole(index=-n_geometries - 1)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["led"])
def test_index_error_when_fallback_finds_nothing(output_object_factory, task: str):
    """Test that an index out of range still raises if the `.out` file fallback finds nothing."""
    output_object = output_object_factory(task)
    with pytest.raises(OpiOutputIndexError):
        output_object.get_final_energy(index=len(output_object.results_properties.geometries))


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["led"])
def test_empty_geometry_list_returns_none(output_object_factory, task: str):
    """Test that an output without geometries (e.g. GFN-FF) returns None instead of raising."""
    output_object = output_object_factory(task)
    output_object.results_properties.geometries = []
    assert output_object.get_dipole() is None


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["opt"])
def test_raise_on_missing(output_object_factory, task: str):
    """Test that with `raise_on_missing` a missing value raises, while available values are returned."""
    output_object = output_object_factory(task)
    output_object.raise_on_missing = True
    assert isinstance(output_object.get_final_energy(), float)
    with pytest.raises(OpiOutputMissingValueError, match="get_quadrupole"):
        output_object.get_quadrupole(index=0)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["opt"])
def test_raise_on_missing_names_called_getter(output_object_factory, task: str):
    """Test that with `raise_on_missing` only the getter called by the user raises, not internal ones."""
    output_object = output_object_factory(task)
    output_object.raise_on_missing = True
    with pytest.raises(OpiOutputMissingValueError, match="get_free_energy_delta"):
        output_object.get_free_energy_delta()


@pytest.mark.unit
@pytest.mark.output
def test_raise_on_missing_after_other_error(empty_output_object: Output):
    """Test that `raise_on_missing` still works for the next getter after a getter raised another error."""
    empty_output_object.raise_on_missing = True
    with pytest.raises(OpiOutputNotParsedError):
        empty_output_object.get_dipole()
    with pytest.raises(OpiOutputMissingValueError, match="get_charge"):
        empty_output_object.get_charge()


@pytest.mark.unit
@pytest.mark.output
def test_calculator_passes_raise_on_missing():
    """Test that `Calculator.get_output()` passes `raise_on_missing` to the `Output`."""
    calc = Calculator("test", version_check=False)
    assert calc.get_output(raise_on_missing=True).raise_on_missing
    assert not calc.get_output().raise_on_missing
