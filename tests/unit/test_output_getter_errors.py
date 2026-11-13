"""
Unit tests for the errors raised by the `Output` getters.

The getters return None if a value is not in the output, but raise if they are used incorrectly:
- `OpiOutputNotParsedError` if the JSON files were not parsed
- `OpiOutputIndexError` if the requested geometry or gbw index does not exist
- `TypeError` if the requested geometry or gbw index is not an integer
"""

import shutil
from pathlib import Path

import numpy as np
import pytest

from opi.exceptions import OpiOutputIndexError, OpiOutputNotParsedError
from opi.output.core import Output

FALLBACK_OUT = Path(__file__).parents[1] / "fixtures" / "job_fallback.out"


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
    with pytest.raises(OpiOutputNotParsedError, match="read_gbw_json"):
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
@pytest.mark.parametrize("getter", ["get_final_energy", "get_structure"])
def test_index_error_when_fallback_has_more_blocks(
    output_object_factory, tmp_path: Path, task: str, getter: str
):
    """
    Test that an index out of range for the JSON geometries raises, even if the `.out` file
    contains more blocks (e.g. from a final evaluation) that the fallback would find.
    """
    output_object = output_object_factory(task)
    shutil.copy(FALLBACK_OUT, tmp_path / f"{output_object.basename}.out")
    output_object.working_dir = tmp_path
    n_geometries = len(output_object.results_properties.geometries)
    # > The `.out` file has a value for this index, the JSON output does not
    assert FALLBACK_OUT.read_text().count("FINAL SINGLE POINT ENERGY") > n_geometries
    with pytest.raises(OpiOutputIndexError, match="geometries"):
        getattr(output_object, getter)(index=n_geometries)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["led"])
def test_empty_geometry_list_returns_none(output_object_factory, task: str):
    """
    Test that an output without geometries returns None instead of raising.
    ORCA writes an empty geometry list to the property JSON for e.g. GFN-FF.
    """
    output_object = output_object_factory(task)
    output_object.results_properties.geometries = []
    assert output_object.get_dipole() is None


@pytest.mark.unit
@pytest.mark.output
def test_missing_value_in_fallback_file_returns_none(output_no_json: Output):
    """Test that a value missing from an existing `.out` file returns None for unparsed output."""
    assert output_no_json.get_final_energy() is not None
    assert output_no_json.get_final_energy(index=10**6) is None


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["led"])
@pytest.mark.parametrize("getter", ["get_structure", "get_gradient"])
def test_index_error_for_fallback_getters(output_object_factory, task: str, getter: str):
    """Test that the other getters with a `.out` file fallback raise for an index out of range."""
    output_object = output_object_factory(task)
    with pytest.raises(OpiOutputIndexError, match="geometries"):
        getattr(output_object, getter)(index=len(output_object.results_properties.geometries))


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["led"])
def test_negative_gbw_index(output_object_factory, task: str):
    """Test that negative gbw indices work within range and raise `OpiOutputIndexError` outside of it."""
    output_object = output_object_factory(task)
    n_gbw = len(output_object.results_gbw)
    assert output_object.get_mos(gbw_index=-n_gbw) == output_object.get_mos(gbw_index=0)
    with pytest.raises(OpiOutputIndexError, match="gbw results"):
        output_object.get_mos(gbw_index=-n_gbw - 1)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["opt"])
def test_numpy_integer_index(output_object_factory, task: str):
    """Test that numpy integers (e.g. from `numpy.argmin()`) are accepted as index."""
    output_object = output_object_factory(task)
    energies = output_object.get_energies(index=0)
    assert energies is not None
    assert output_object.get_energies(index=np.int64(0)) == energies
    assert output_object.get_final_energy(index=np.int64(0)) == output_object.get_final_energy(
        index=0
    )
    with pytest.raises(OpiOutputIndexError):
        output_object.get_energies(index=np.int64(len(output_object.results_properties.geometries)))


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["opt"])
@pytest.mark.parametrize("index", [0.0, "0", None])
def test_type_error_for_non_integer_index(output_object_factory, task: str, index):
    """Test that an index that is not an integer raises a `TypeError` instead of returning None."""
    output_object = output_object_factory(task)
    with pytest.raises(TypeError, match="integer"):
        output_object.get_energies(index=index)
    with pytest.raises(TypeError, match="integer"):
        output_object.get_final_energy(index=index)
    with pytest.raises(TypeError, match="integer"):
        output_object.get_mos(gbw_index=index)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("index", [0.0, "0", None])
def test_type_error_for_non_integer_index_without_parsed_output(
    output_no_json: Output, empty_output_object: Output, index
):
    """
    Test that an index that is not an integer raises a `TypeError` also if the output is not
    parsed, both for getters with `.out` file fallback and without.
    """
    with pytest.raises(TypeError, match="integer"):
        output_no_json.get_final_energy(index=index)
    with pytest.raises(TypeError, match="integer"):
        empty_output_object.get_dipole(index=index)
