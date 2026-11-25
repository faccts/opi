import pytest

from opi.output.core import Output
from opi.utils.element import ATOMIC_MASSES_FROM_ELEMENT

"""
Unit test for Output thermodynamic property getters.

This module contains tests for getters related to thermodynamic properties such as:
- Inner Energy
- Enthalpy
- Entropy
- Free Energy
- Electronic Energy
- Free Energy delta
- Vibrational frequencies
- PES character checks (minimum, transition state)
"""


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["rama"])
def test_get_inner_energy_returns_float(output_object_factory, task):
    """Test if `Output.get_inner_energy()` returns float."""
    output_object = output_object_factory(task)
    assert isinstance(output_object.get_inner_energy(), float)


@pytest.mark.unit
@pytest.mark.output
def test_get_inner_energy_returns_none(empty_output_object: Output):
    """Test if `Output.get_inner_energy()` returns None when expected."""
    assert not empty_output_object.get_inner_energy()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "task",
    ["rama"],
)
def test_get_enthalpy_returns_float(output_object_factory, task: str):
    """Test if `Output.get_enthalpy()` returns float."""
    output_object = output_object_factory(task)
    assert isinstance(output_object.get_enthalpy(), float)


@pytest.mark.unit
@pytest.mark.output
def test_get_enthalpy_returns_none(empty_output_object: Output):
    """Test if `Output.get_enthalpy()` returns None when expected."""
    assert not empty_output_object.get_enthalpy()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "task",
    ["rama"],
)
def test_get_entropy_returns_float(output_object_factory, task: str):
    """Test if `Output.get_entropy()` returns float."""
    output_object = output_object_factory(task)
    assert isinstance(output_object.get_entropy(), float)


@pytest.mark.unit
@pytest.mark.output
def test_get_entropy_returns_none(empty_output_object: Output):
    """Test if `Output.get_entropy()` returns None when expected."""
    assert not empty_output_object.get_entropy()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "task",
    ["rama"],
)
def test_get_free_energy_returns_float(output_object_factory, task: str):
    """Test if `Output.get_free_energy()` returns float."""
    output_object = output_object_factory(task)
    assert isinstance(output_object.get_free_energy(), float)


@pytest.mark.unit
@pytest.mark.output
def test_get_free_energy_returns_none(empty_output_object: Output):
    """Test if `Output.get_free_energy()` returns None when expected."""
    assert not empty_output_object.get_free_energy()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "task",
    ["rama"],
)
def test_get_el_energy_returns_float(output_object_factory, task: str):
    """Test if `Output.get_el_energy()` returns correct value."""
    output_object = output_object_factory(task)
    assert isinstance(output_object.get_el_energy(), float)


@pytest.mark.unit
@pytest.mark.output
def test_get_el_energy_returns_none(empty_output_object: Output):
    """Test if `Output.get_el_energy()` returns None when expected."""
    assert not empty_output_object.get_el_energy()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "task",
    ["rama"],
)
def test_get_free_energy_delta_returns_float(output_object_factory, task: str):
    """Test if `Output.get_free_energy()` returns correct value."""
    output_object = output_object_factory(task)
    assert isinstance(output_object.get_free_energy_delta(), float)


@pytest.mark.unit
@pytest.mark.output
def test_get_free_energy_delta_returns_none(empty_output_object: Output):
    """Test if `Output.get_free_energy_delta()` returns None when expected."""
    assert not empty_output_object.get_free_energy_delta()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["rama"])
def test_get_frequencies_returns_dict(output_object_factory, task):
    """Test if `Output.get_frequencies()` returns a non-empty dict of floats."""
    output_object = output_object_factory(task)
    frequencies = output_object.get_frequencies()
    assert isinstance(frequencies, dict)
    assert len(frequencies) > 0
    assert all(isinstance(k, int) for k in frequencies)
    assert all(isinstance(v, float) for v in frequencies.values())


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["rama"])
def test_get_normal_modes_returns_dict(output_object_factory, task):
    """Test `Output.get_normal_modes()`: one xyz displacement per atom for every frequency."""
    output_object = output_object_factory(task)
    normal_modes = output_object.get_normal_modes()
    assert isinstance(normal_modes, dict)
    assert normal_modes.keys() == output_object.get_frequencies().keys()
    n_atoms = len(output_object.get_structure())
    for mode in normal_modes.values():
        assert len(mode) == n_atoms
        assert all(len(displacement) == 3 for displacement in mode)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["rama"])
def test_get_normal_modes_mass_weighted_normalized(output_object_factory, task):
    """Test `Output.get_normal_modes()`: vibrational modes satisfy sum_i m_i * |d_i|^2 = 1."""
    output_object = output_object_factory(task)
    normal_modes = output_object.get_normal_modes()
    masses = [
        ATOMIC_MASSES_FROM_ELEMENT[atom.element] for atom in output_object.get_structure().atoms
    ]
    for mode_index, frequency in output_object.get_frequencies().items():
        norm = sum(
            mass * sum(component**2 for component in displacement)
            for mass, displacement in zip(masses, normal_modes[mode_index])
        )
        assert norm == pytest.approx(0.0 if frequency == 0.0 else 1.0, abs=1e-3)


@pytest.mark.unit
@pytest.mark.output
def test_get_normal_modes_returns_none(empty_output_object: Output):
    """Test if `Output.get_normal_modes()` returns None without frequency data."""
    assert empty_output_object.get_normal_modes() is None


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["rama"])
def test_get_imaginary_frequencies_returns_empty_dict_for_minimum(output_object_factory, task):
    """Test if `Output.get_imaginary_frequencies()` returns an empty dict (not None) for a minimum structure."""
    output_object = output_object_factory(task)
    imaginary = output_object.get_imaginary_frequencies()
    assert isinstance(imaginary, dict)
    assert len(imaginary) == 0


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["rama"])
def test_is_pes_minimum_returns_true_for_minimum(output_object_factory, task):
    """Test if `Output.is_pes_minimum()` returns True for a minimum structure."""
    output_object = output_object_factory(task)
    assert output_object.is_pes_minimum() is True


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["rama"])
def test_is_pes_transition_state_returns_false_for_minimum(output_object_factory, task):
    """Test if `Output.is_pes_transition_state()` returns False for a minimum structure."""
    output_object = output_object_factory(task)
    assert output_object.is_pes_transition_state() is False
