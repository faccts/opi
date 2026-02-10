import pytest

from opi.output.core import Output

"""
Unit tests for Output system property getters. 

This module contsins tests for getter methods of basic system properties such as:
- Hartree-Fock type
- Molecular charge 
- Spin multiplicity
- Number of electrons
- Number of basis sets 
"""


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "task, expected_values",
    [
        ("opt", "rhf"),
        ("roci", "rohf"),
    ],
)
def test_get_hftype(output_object_factory, task: str, expected_values: str):
    """Test to check if `Output.get_hftype()` returns expected value."""
    output_object = output_object_factory(task)
    assert output_object.get_hftype() == expected_values


@pytest.mark.unit
@pytest.mark.output
def test_get_hftype_nonexistent(empty_output_object):
    """Test to check if `Output.get_hftype()` returns None when expected."""
    assert not empty_output_object.get_hftype()


@pytest.mark.unit
@pytest.mark.output
def test_get_charge_nonexistent(empty_output_object: Output):
    """Test to check if `Output.get_charge()` returns None when expected."""
    assert not empty_output_object.get_charge()


@pytest.mark.unit
@pytest.mark.output
def test_get_mult_nonexistent(empty_output_object: Output):
    """Test to check if `Output.get_mult()` returns None when expected."""
    assert not empty_output_object.get_mult()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "task, expected_values",
    [("opt", 8), ("roci", 11)],
)
def test_get_nelectrons_not_spin_resolved(output_object_factory, task: str, expected_values: int):
    """Test to check if `Output.get_nelectrons()` returns expected values."""
    output_object = output_object_factory(task)
    x, y = output_object.get_nelectrons()
    assert (x == expected_values) and (not y)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    "task, expected_values",
    [
        ("cipsi", (5, 5)),
        ("roci", (6, 5)),
    ],
)
def test_get_nelectrons_spin_resolved(
    output_object_factory, task: str, expected_values: tuple[int, int]
):
    """Test to check if `Output.get_nelectrons()` returns expected values, when `spin_resolved` is True."""
    output_object = output_object_factory(task)
    assert output_object.get_nelectrons(spin_resolved=True) == expected_values


@pytest.mark.unit
@pytest.mark.output
def test_get_nelectrons_nonexistent(empty_output_object: Output):
    """Test to check if `Output.get_nelectrons()` returns None when expected."""
    x, y = empty_output_object.get_nelectrons()
    assert (not x) and (not y)


@pytest.mark.unit
@pytest.mark.output
def test_get_nbf_nonexistent(empty_output_object: Output):
    """Test to check if `Output.get_nbf()` returns None when expected."""
    assert not empty_output_object.get_nbf()
