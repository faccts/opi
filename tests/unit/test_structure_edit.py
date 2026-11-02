import numpy as np
import pytest

from opi.input.structures import Atom, Structure

"""
This module contains tests for structure-related operations such as:
- Adding `Atom` to `Structure` object.
- Deleting `Atom` from `Structure` object.
- Replacing `Atom` in `Structure` object.
- Extracting Coordinate information from `Structure` object.
- Extracting substructure.
"""


@pytest.fixture
def new_coord_block() -> np.ndarray:
    """Empty coordinate block."""
    coord_block = np.zeros(shape=(3, 3), dtype=np.float64)
    return coord_block


@pytest.fixture(params=[-2, 4])
def invalid_position(request) -> int:
    """Provide different keyword combinations for parameterized testing."""
    return request.param


@pytest.mark.unit
@pytest.mark.input
def test_add_atom(water_structure: Structure, test_h_atom: Atom):
    """Test to check if `Structure.add_atom()` works correctly."""
    water_structure.add_atom(test_h_atom)
    assert water_structure.atoms[-1] == test_h_atom


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize("positions", [0, 2, 3])
def test_add_atom_with_position(water_structure: Structure, test_h_atom: Atom, positions: int):
    """Test to check if `Structure.add_atom()` works correctly given positions."""
    water_structure.add_atom(test_h_atom, positions)
    assert water_structure.atoms[positions] == test_h_atom


@pytest.mark.unit
@pytest.mark.input
def test_add_atom_invalid_position(
    water_structure: Structure, test_h_atom: Atom, invalid_position: int
):
    """Test to check if `Structure.add_atom()` correctly raises errors given invalid positions."""
    with pytest.raises(ValueError):
        water_structure.add_atom(test_h_atom, invalid_position)


@pytest.mark.unit
@pytest.mark.input
def test_delete_atom(water_structure: Structure):
    """Test to check if `Structure.delete_atom()` works correctly."""
    atom_to_delete = water_structure.atoms[1]
    water_structure.delete_atom(1)
    assert atom_to_delete not in water_structure.atoms


@pytest.mark.unit
@pytest.mark.input
def test_delete_atom_invalid_position(water_structure: Structure, invalid_position: int):
    """Test to check if `Structure.delete_atom()` correctly raises errors given invalid positions."""
    with pytest.raises(ValueError):
        water_structure.delete_atom(invalid_position)


@pytest.mark.unit
@pytest.mark.input
def test_replace_atom(water_structure: Structure, test_h_atom: Atom):
    """Test to check if `Structure.replace_atom()` works correctly."""
    water_structure.replace_atom(test_h_atom, index=1)
    assert water_structure.atoms[1] == test_h_atom


@pytest.mark.unit
@pytest.mark.input
def test_replace_atom_invalid_position(
    water_structure: Structure, test_h_atom: Atom, invalid_position: int
):
    """Test to check if `Structure.replace_atom()` correctly raises errors given invalid positions."""
    with pytest.raises(ValueError):
        water_structure.replace_atom(test_h_atom, invalid_position)


@pytest.mark.unit
@pytest.mark.input
def test_update_coordinates(water_structure: Structure, new_coord_block: np.ndarray):
    """Test to check if `Structure.update_coordinates()` works correctly."""
    water_structure.update_coordinates(new_coord_block)
    for atom in water_structure.atoms:
        np.testing.assert_array_equal(atom.coordinates.coordinates, np.zeros(3))


@pytest.mark.unit
@pytest.mark.input
def test_update_coordinates_invalid_array(water_structure: Structure):
    """Test to check if `Structure.update_coordinates()` correctly raises errors given invalid array."""
    with pytest.raises(ValueError):
        water_structure.update_coordinates(np.zeros((3, 2)))


@pytest.mark.unit
@pytest.mark.input
def test_extract_substructure(water_structure: Structure):
    """Test to check if `Structure.extract_substructure()` correctly creates a `Structure` object."""
    substructure = water_structure.extract_substructure([0, 1])
    assert isinstance(substructure, Structure)


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize("index_range", [[0, 2], [0, 1, 2], [2]])
def test_extract_substructure_correct_size(water_structure: Structure, index_range: list[int]):
    """Test to check if `Structure.extract_substructure()` creates a `Structure` object of the correct size."""
    substructure = water_structure.extract_substructure(index_range)
    assert len(substructure) == len(index_range)


@pytest.mark.unit
@pytest.mark.input
def test_extract_substructure_invalid_index(water_structure: Structure):
    """Test to check if `Structure.extract_substructure()` correctly raises errors given invalid index."""
    with pytest.raises(IndexError):
        water_structure.extract_substructure([len(water_structure.atoms) + 1])
