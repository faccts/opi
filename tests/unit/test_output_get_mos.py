import pytest

from opi.output.mo_data import MOData
from opi.output.models.json.gbw.properties.mo import MO

"""
Unit tests for Output molecular orbital (MO) property getters.

This module contains tests for the getters of MO-related properties such as:
- Individual MO data
- HOMO 
- LUMO
"""


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", [("led")])
def test_get_mos_returns_dict(output_object_factory, task: str):
    """Test to check if `Output.get_mos()` returns `dict` object."""
    output_object = output_object_factory(task)
    assert isinstance(output_object.get_mos(), dict)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", [("led")])
def test_get_mos_returns_mo(output_object_factory, task: str):
    """Test to check if `Output.get_mos()` returns `dict` with `MO` objects."""
    output_object = output_object_factory(task)
    for value in output_object.get_mos().values():
        assert all(isinstance(mo, MO) for mo in value)


@pytest.mark.unit
@pytest.mark.output
def test_get_mos_returns_none(empty_output_object):
    """Test if `Output.get_mos()` returns `None` when expected."""
    assert not empty_output_object.get_mos()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", [("led")])
def test_get_homo(output_object_factory, task: str):
    """Test to check if `Output.get_homo()` returns `MOData` object."""
    output_object = output_object_factory(task)
    assert isinstance(output_object.get_homo(), MOData)


@pytest.mark.unit
@pytest.mark.output
def test_get_homo_returns_none(empty_output_object):
    """Test if `Output.get_homo()` returns `None` when expected."""
    assert not empty_output_object.get_homo()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", [("led")])
def test_get_lumo(output_object_factory, task: str):
    """Test to check if `Output.get_lumo()` returns `MOData` object."""
    output_object = output_object_factory(task)
    assert isinstance(output_object.get_lumo(), MOData)


@pytest.mark.unit
@pytest.mark.output
def test_get_lumo_returns_none(empty_output_object):
    """Test if `Output.get_lumo()` returns `None` when expected."""
    assert not empty_output_object.get_lumo()
