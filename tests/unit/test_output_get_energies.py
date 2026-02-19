import pytest

from opi.output.core import Output
from opi.output.models.json.property.properties.mp2_energy import Mp2Energy
from opi.output.models.json.property.properties.scf_energy import ScfEnergy

"""
Unit tests for Output energy property getters.

This module contains tests for the getter methods of energy-related attributes such as :
- Final energy values at specific geometry indices
- Energy dictionaries containing multiple energy types (SCF, MP2, etc.)
- Zero-point energy (ZPE) values

"""


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["mp2", "rama"])
def test_get_final_energy_invalid_index(output_object_factory, task: str):
    """Test to check if `Output.get_final_energy()` returns None when given invalid index."""
    output_object = output_object_factory(task)
    assert not output_object.get_final_energy(
        index=len(output_object.results_properties.geometries)
    )


@pytest.mark.unit
@pytest.mark.output
def test_get_final_energy_nonexistent(empty_output_object: Output):
    """Test to check if `Output.get_final_energy()` returns None when expected."""
    assert not empty_output_object.get_final_energy()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "task, key_name,expected_type",
    [("epr", "SCF", ScfEnergy), ("mp2", "MP2", Mp2Energy)],
)
def test_get_energies_type_no_index(output_object_factory, task: str, key_name: str, expected_type):
    """Test to check if `Output.get_energies()` returns expected type."""
    output_object = output_object_factory(task)
    assert isinstance(output_object.get_energies()[key_name], expected_type)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["rama"])
def test_get_zpe_returns_correct_type(output_object_factory, task: str):
    """Test if `Output.get_zpe()` returns correct type."""
    output_object = output_object_factory(task)
    assert isinstance(output_object.get_zpe(), float)


@pytest.mark.unit
@pytest.mark.output
def test_get_zpe_returns_correct_none(empty_output_object):
    """Test if `Output.get_zpe()` returns None when expected."""
    assert not empty_output_object.get_zpe()
