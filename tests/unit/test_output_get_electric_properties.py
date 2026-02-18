import pytest

from opi.output.models.json.property.properties.dipole_moment import DipoleMoment
from opi.output.models.json.property.properties.polarizability import Polarizability
from opi.output.models.json.property.properties.quadrupole_moment import QuadrupoleMoment

"""
Unit tests for Output electric property getters 

This module contains tests for the getters of electric properties such as:
- Dipole Moments
- Quadrupole Moments
- Polarizability
"""


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["led", "rama"])
def test_get_dipole_returns_list_of_dipole_moment(output_object_factory, task: str):
    """Test if `Output.get_dipole()` returns list of `DipoleMoment` objects."""
    output_object = output_object_factory(task)
    for dipole_moment in output_object.get_dipole():
        assert isinstance(dipole_moment, DipoleMoment)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "task, index",
    [("led", 1), ("nmr", 3)],
)
def test_get_dipole_returns_none(output_object_factory, task: str, index: int):
    """Test if `Output.get_dipole()` returns `None` when expected."""
    output_object = output_object_factory(task)
    assert not output_object.get_dipole(index=index)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["pop_analysis"])
def test_get_quadrupole_returns_list_of_quadrupole_moment(output_object_factory, task: str):
    """Test if `Output.get_quadrupole()` returns list of `QuadrupoleMoment` objects."""
    output_object = output_object_factory(task)
    for quadrupole_moment in output_object.get_quadrupole():
        assert isinstance(quadrupole_moment, QuadrupoleMoment)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["pop_analysis"])
def test_get_quadrupole_returns_list_of_correct_length(output_object_factory, task: str):
    """Test if `Output.get_quadrupole()` returns list of correct length"""
    output_object = output_object_factory(task)
    assert len(output_object.get_quadrupole()) == 3


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "task, index",
    [("opt", 0), ("pop_analysis", 3)],
)
def test_get_quadrupole_returns_none(output_object_factory, task: str, index: int):
    """Test if `Output.get_quadrupole()` returns `None` when expected."""
    output_object = output_object_factory(task)
    assert not output_object.get_quadrupole(index=index)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "task",
    ["pop_analysis", "rama"],
)
def test_get_polarizability_returns_list(output_object_factory, task: str):
    """Test if `Output.get_polarizability()` returns list."""
    output_object = output_object_factory(task)
    assert isinstance(output_object.get_polarizability(), list)


@pytest.mark.unit
@pytest.mark.output
def test_get_polarizability_returns_none(empty_output_object):
    """Test if `Output.get_polarizability()` returns None when expected."""
    assert not empty_output_object.get_polarizability()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "task",
    ["pop_analysis", "rama"],
)
def test_get_polarizability_returns_list_of_correct_type(output_object_factory, task: str):
    """Test of Output.get_polarizability() returns list of `Polarizability` type."""
    output_object = output_object_factory(task)
    for polarizability in output_object.get_polarizability():
        assert isinstance(polarizability, Polarizability)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "task, length",
    [("pop_analysis", 3), ("rama", 1)],
)
def test_get_polarizability_returns_list_of_correct_length(
    output_object_factory, task: str, length: int
):
    """Test of Output.get_polarizability() returns list of correct length."""
    output_object = output_object_factory(task)
    assert len(output_object.get_polarizability()) == length
