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
