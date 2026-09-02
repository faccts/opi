import pytest

from opi.output.core import Output

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
