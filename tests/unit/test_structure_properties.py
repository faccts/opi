import pytest

from opi.input.structures import Atom, GhostAtom, Structure


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
def test_ghost_atom():
    "Test instance of `GhostAtom`."
    atom = GhostAtom("H", coordinates=[-3.88959, 2.36040, 0.81444])
    return atom


@pytest.fixture
def test_atom():
    """Test instance of `Atom`."""
    atom = Atom("H", coordinates=[3.88959, 1.36040, 0.81444])
    return atom


@pytest.mark.unit
def test_nelectrons(structure: Structure):
    """Test to check if `structure.nelectrons` is correct."""
    assert structure.nelectrons == 10


def test_nelectron_ghost(structure: Structure, ghost_atom: GhostAtom):
    """Test to check if `structure.nelectrons` is unchanged by adding ghost atoms."""
    initial_electrons = structure.nelectrons
    structure.add_atom(ghost_atom)
    assert structure.nelectrons == initial_electrons
