import pytest

from opi.input.structures import Atom, GhostAtom, Structure


@pytest.fixture
def water_structure() -> Structure:
    """Test instance of Water `Structure`."""
    content = """3

    O         -3.56626        1.77639        0.00000
    H         -2.59626        1.77639        0.00000
    H         -3.88959        1.36040       -0.81444"""

    structure = Structure.from_xyz_block(content)
    return structure


@pytest.fixture
def test_h_atom():
    """Test instance of H `Atom`."""
    atom = Atom("H", coordinates=[3.88959, 1.36040, 0.81444])
    return atom


@pytest.fixture
def test_ghost_h_atom():
    "Test instance of H `GhostAtom`."
    atom = GhostAtom("H", coordinates=[-3.88959, 2.36040, 0.81444])
    return atom
