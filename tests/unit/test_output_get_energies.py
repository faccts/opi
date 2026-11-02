import pytest

from opi.output.core import Output
from opi.output.energy_type import EnergyType
from opi.output.models.json.property.properties.ci_psi import CiPsi
from opi.output.models.json.property.properties.energy import Energy
from opi.output.models.json.property.properties.gcp_energy import GcpEnergy
from opi.output.models.json.property.properties.mp2_energy import Mp2Energy
from opi.output.models.json.property.properties.roci_en import RoCisEnergy
from opi.output.models.json.property.properties.scf_energy import ScfEnergy
from opi.output.models.json.property.properties.van_der_waals_correction import VdwCorrection

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
@pytest.mark.parametrize(
    "task, expected_keys",
    [("opt", ("SCF", "VdW")), ("engrad", ("SCF", "VdW", "gCP"))],
)
def test_get_final_energy_components_sum_to_final_energy(
    output_object_factory, task: str, expected_keys: tuple[str, ...]
):
    """Test that `Output.get_final_energy_components()` reports the corrections on top of the
    energies of `Output.get_energies()` and that all contributions add up to the final energy."""
    output_object = output_object_factory(task)
    energy_components = output_object.get_final_energy_components()
    assert set(energy_components) == set(expected_keys)
    # > the corrections are not part of the energy list of the JSON output
    assert set(output_object.get_energies()) == {"SCF"}
    total = sum(energy_components[key].energy for key in expected_keys)
    assert total == pytest.approx(output_object.get_final_energy())


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["roci"])
def test_get_rocis_energies(output_object_factory, task: str):
    """Test that `Output.get_rocis_energies()` returns the ROCIS energies."""
    output_object = output_object_factory(task)
    rocis_energies = output_object.get_rocis_energies()
    assert isinstance(rocis_energies, RoCisEnergy)
    # > the total energy is the one of the lowest root and the final energy of the calculation
    assert rocis_energies.totalenergy == pytest.approx(output_object.get_final_energy())
    assert len(rocis_energies.energies) == rocis_energies.numofroots


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["cipsi"])
def test_get_cipsi_energies(output_object_factory, task: str):
    """Test that `Output.get_cipsi_energies()` returns the CIPSI energies."""
    output_object = output_object_factory(task)
    cipsi_energies = output_object.get_cipsi_energies()
    assert isinstance(cipsi_energies, CiPsi)
    assert cipsi_energies.finalenergy == pytest.approx(output_object.get_final_energy())
    assert len(cipsi_energies.energies) == cipsi_energies.numofroots


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["engrad"])
def test_get_corrections(output_object_factory, task: str):
    """Test that the correction getters return the models behind the `VdW` and `gCP` entries of
    `Output.get_final_energy_components()`."""
    output_object = output_object_factory(task)
    energy_components = output_object.get_final_energy_components()
    vdw_correction = output_object.get_vdw_correction()
    gcp_correction = output_object.get_gcp_correction()
    assert isinstance(vdw_correction, VdwCorrection)
    assert isinstance(gcp_correction, GcpEnergy)
    assert vdw_correction.vdw == energy_components["VdW"].energy
    assert gcp_correction.gcp_energy == energy_components["gCP"].energy


@pytest.mark.unit
@pytest.mark.output
def test_get_energies_outside_energy_list_nonexistent(empty_output_object: Output):
    """Test that the getters for the energies outside of the energy list return None when expected."""
    assert empty_output_object.get_vdw_correction() is None
    assert empty_output_object.get_gcp_correction() is None
    assert empty_output_object.get_rocis_energies() is None
    assert empty_output_object.get_cipsi_energies() is None


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "task, key_name", [("engrad", "SCF"), ("engrad", "VdW"), ("engrad", "gCP"), ("mp2", "MP2")]
)
def test_energy_scalar_accessor(output_object_factory, task: str, key_name: str):
    """Test that `Energy.energy` returns the total energy of the entry as a plain float."""
    energy = output_object_factory(task).get_final_energy_components()[key_name]
    assert energy.energy == energy.totalenergy[0][0]


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task, key_name", [("mp2", "MP2"), ("autoci", "AUTOCI")])
def test_correlated_energy_scalar_accessors(output_object_factory, task: str, key_name: str):
    """Test the scalar accessors of the correlated energies."""
    energy = output_object_factory(task).get_energies()[key_name]
    assert energy.correlation_energy == energy.correnergy[0][0]
    assert energy.reference_energy == energy.refenergy[0][0]
    # > the correlation energy is the difference between the total and the reference energy
    assert energy.reference_energy + energy.correlation_energy == pytest.approx(energy.energy)


@pytest.mark.unit
@pytest.mark.output
def test_energy_scalar_accessor_without_energy():
    """Test that `Energy.energy` returns None instead of raising if there is no energy."""
    assert Energy().energy is None
    assert Energy(totalenergy=[[]]).energy is None


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task, energy_type", [("engrad", EnergyType.SCF), ("mp2", EnergyType.MP2)])
def test_energy_type_usable_as_key(output_object_factory, task: str, energy_type: EnergyType):
    """Test that the `EnergyType` members can be used to look up energies directly."""
    energies = output_object_factory(task).get_energies()
    assert energies[energy_type] is energies[str(energy_type)]


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


@pytest.mark.unit
@pytest.mark.output
def test_get_final_energy_fallback(output_no_json):
    """Test that `get_final_energy()` falls back to grepping the .out file when no JSON is present."""
    energy = output_no_json.get_final_energy()
    assert isinstance(energy, float)


@pytest.mark.unit
@pytest.mark.output
def test_get_final_energy_fallback_index(output_no_json):
    """Test that grepper fallback respects the index argument and returns different values per geometry."""
    e0 = output_no_json.get_final_energy(index=0)
    e_last = output_no_json.get_final_energy(index=-1)
    assert isinstance(e0, float)
    assert isinstance(e_last, float)
    assert e0 != e_last


@pytest.mark.unit
@pytest.mark.output
def test_get_final_energy_no_fallback(output_no_json):
    """Test that `get_final_energy(fallback=False)` returns None when no JSON is present."""
    assert output_no_json.get_final_energy(fallback=False) is None
