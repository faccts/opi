import numpy as np
import pytest

from opi.input.structures import Atom, Structure


@pytest.fixture
def structure() -> Structure:
    """Test instance of `Structure`."""
    content = """3

    O         -3.56626        1.77639        0.00000
    H         -2.59626        1.77639        0.00000
    H         -3.88959        1.36040       -0.81444"""

    structure = Structure.from_xyz_block(content)
    return structure


@pytest.fixture
def test_atom():
    """Test instance of `Atom`."""
    atom = Atom("H", coordinates=[3.88959, 1.36040, 0.81444])
    return atom


@pytest.fixture
def new_coord_block() -> np.ndarray:
    """Empty coordinate block."""
    coord_block = np.zeros(shape=(3, 3), dtype=np.float64)
    return coord_block


@pytest.fixture(params=[-2, 4])
def invalid_position(request) -> int:
    """Provide different keyword combinations for parameterized testing."""
    return request.param


def test_add_atom(structure: Structure, test_atom: Atom):
    """Test to check if `Structure.add_atom()` works correctly."""
    structure.add_atom(test_atom)
    assert structure.atoms[-1] == test_atom


@pytest.mark.parametrize("positions", [0, 2, 3])
def test_add_atom_with_position(structure: Structure, test_atom: Atom, positions: int):
    """Test to check if `Structure.add_atom()` works correctly given positions."""
    structure.add_atom(test_atom, positions)
    assert structure.atoms[positions] == test_atom


def test_add_atom_invalid_position(structure: Structure, test_atom: Atom, invalid_position: int):
    """Test to check if `Structure.add_atom()` correctly raises errors given invalid positions."""
    with pytest.raises(ValueError):
        structure.add_atom(test_atom, invalid_position)


def test_delete_atom(structure: Structure):
    """Test to check if `Structure.delete_atom()` works correctly."""
    atom_to_delete = structure.atoms[1]
    structure.delete_atom(1)
    assert atom_to_delete not in structure.atoms


def test_delete_atom_invalid_position(structure: Structure, invalid_position: int):
    """Test to check if `Structure.delete_atom()` correctly raises errors given invalid positions."""
    with pytest.raises(ValueError):
        structure.delete_atom(invalid_position)


def test_replace_atom(structure: Structure, test_atom: Atom):
    """Test to check if `Structure.replace_atom()` works correctly."""
    structure.replace_atom(test_atom, index=1)
    assert structure.atoms[1] == test_atom


def test_replace_atom_invalid_position(
    structure: Structure, test_atom: Atom, invalid_position: int
):
    """Test to check if `Structure.replace_atom()` correctly raises errors given invalid positions."""
    with pytest.raises(ValueError):
        structure.replace_atom(test_atom, invalid_position)


def test_update_coordinates(structure: Structure, new_coord_block: np.ndarray):
    """Test to check if `Structure.update_coordinates()` works correctly."""
    structure.update_coordinates(new_coord_block)
    for atom in structure.atoms:
        np.testing.assert_array_equal(atom.coordinates.coordinates, np.zeros(3))


def test_update_coordinates_invalid_array(structure: Structure):
    """Test to check if `Structure.update_coordinates()` correctly raises errors given invalid array."""
    with pytest.raises(ValueError):
        structure.update_coordinates(np.zeros((3, 2)))


def test_extract_substructure(structure: Structure):
    """Test to check if `Structure.extract_substructure()` correctly creates a `Structure` object."""
    substructure = structure.extract_substructure([0, 1])
    assert isinstance(substructure, Structure)


@pytest.mark.parametrize("index_range", [[0, 2], [0, 1, 2], [2]])
def test_extract_substructure_correct_size(structure: Structure, index_range: list[int]):
    """Test to check if `Structure.extract_substructure()` creates a `Structure` object of the correct size."""
    substructure = structure.extract_substructure(index_range)
    assert len(substructure) == len(index_range)


def test_extract_substructure_invalid_index(structure: Structure):
    """Test to check if `Structure.extract_substructure()` correctly raises errors given invalid index."""
    with pytest.raises(IndexError):
        structure.extract_substructure([len(structure.atoms) + 1])
