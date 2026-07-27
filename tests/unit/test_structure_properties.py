import pytest

from opi.input.structures import GhostAtom, Structure


@pytest.mark.unit
def test_nelectrons(water_structure: Structure):
    """Test to check if `structure.nelectrons` is correct."""
    assert water_structure.nelectrons == 10


def test_nelectron_ghost(water_structure: Structure, ghost_h_atom: GhostAtom):
    """Test to check if `structure.nelectrons` is unchanged by adding ghost atoms."""
    initial_electrons = water_structure.nelectrons
    water_structure.add_atom(ghost_h_atom)
    assert water_structure.nelectrons == initial_electrons
