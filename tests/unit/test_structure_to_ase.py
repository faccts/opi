"""
Unit tests for the ASE interoperability of `Structure`.

ASE is an optional dependency. All tests in this module are skipped
automatically if ASE is not installed.

Covers for `to_ase()`: element symbols and coordinates, charge and multiplicity
transport via `Atoms.info`, exclusion of non-real entries, the no-real-atoms error,
and the round trip through `from_ase()`.

Covers for `from_ase()`: the precedence of explicit arguments over ASE's per-atom
`initial_charges` / `initial_magnetic_moments` arrays over `Atoms.info` over the
neutral closed-shell default.
"""

import pytest

pytest.importorskip("ase", reason="ASE not installed")

import numpy as np
from ase import Atoms as AseAtoms

from opi.input.structures.atom import GhostAtom, PointCharge
from opi.input.structures.coordinates import Coordinates
from opi.input.structures.structure import Structure
from opi.utils.element import Element

# ============================================================
# Fixtures
# ============================================================

_WATER_XYZ_BLOCK = (
    "3\n\n"
    "O   0.000000   0.000000   0.119748\n"
    "H   0.000000   0.756950  -0.478993\n"
    "H   0.000000  -0.756950  -0.478993"
)

# > Reference geometry matching `_WATER_XYZ_BLOCK`, in Angstrom.
_WATER_COORDS = [
    [0.0, 0.0, 0.119748],
    [0.0, 0.756950, -0.478993],
    [0.0, -0.756950, -0.478993],
]


@pytest.fixture()
def water_cation() -> Structure:
    """H2O at a known geometry with a non-trivial charge and multiplicity."""
    return Structure.from_xyz_block(_WATER_XYZ_BLOCK, charge=1, multiplicity=2)


@pytest.fixture()
def no_real_atoms_structure() -> Structure:
    """Structure containing only a PointCharge, i.e. no real Atom instances."""
    return Structure(
        atoms=[PointCharge(coordinates=Coordinates(coordinates=(0.0, 0.0, 0.0)), charge=1.0)]
    )


# ============================================================
# to_ase
# ============================================================


@pytest.mark.ase
@pytest.mark.unit
class TestToAse:
    def test_symbols_and_positions(self, water_cation):
        """`to_ase()` should transfer element symbols and Angstrom coordinates unchanged."""
        ase_atoms = water_cation.to_ase()
        assert isinstance(ase_atoms, AseAtoms)
        assert ase_atoms.get_chemical_symbols() == ["O", "H", "H"]
        assert np.allclose(ase_atoms.get_positions(), _WATER_COORDS)

    def test_charge_and_multiplicity_in_info(self, water_cation):
        """`to_ase()` should carry charge and multiplicity in `Atoms.info`."""
        ase_atoms = water_cation.to_ase()
        assert ase_atoms.info["charge"] == 1
        assert ase_atoms.info["spin"] == 2

    def test_non_real_atoms_excluded(self):
        """`GhostAtom` and `PointCharge` entries should be skipped silently."""
        structure = Structure.from_xyz_block(_WATER_XYZ_BLOCK)
        structure.add_atom(
            GhostAtom(element=Element("C"), coordinates=Coordinates(coordinates=(5.0, 5.0, 5.0)))
        )
        structure.add_atom(
            PointCharge(coordinates=Coordinates(coordinates=(6.0, 6.0, 6.0)), charge=1.0)
        )
        ase_atoms = structure.to_ase()
        assert ase_atoms.get_chemical_symbols() == ["O", "H", "H"]
        assert np.allclose(ase_atoms.get_positions(), _WATER_COORDS)

    def test_raises_for_no_real_atoms(self, no_real_atoms_structure):
        """`to_ase()` should raise `ValueError` if there are no real atoms."""
        with pytest.raises(ValueError, match="no real atoms"):
            no_real_atoms_structure.to_ase()

    def test_round_trip(self, water_cation):
        """`from_ase(to_ase())` should preserve symbols, geometry, charge and multiplicity."""
        restored = Structure.from_ase(water_cation.to_ase())
        assert [atom.element.value for atom in restored.atoms] == ["O", "H", "H"]
        assert np.allclose(restored.get_coordinates(), _WATER_COORDS)
        assert restored.charge == water_cation.charge
        assert restored.multiplicity == water_cation.multiplicity


# ============================================================
# from_ase: charge / multiplicity resolution
# ============================================================


@pytest.mark.ase
@pytest.mark.unit
class TestFromAseChargeAndMultiplicity:
    def test_per_atom_arrays_take_precedence_over_info(self):
        """Set `initial_charges` / magnetic moments should win over `Atoms.info`."""
        ase_atoms = AseAtoms(
            symbols=["O", "H", "H"],
            positions=_WATER_COORDS,
            info={"charge": 1, "spin": 2},
        )
        ase_atoms.set_initial_charges([-1.0, 0.0, 0.0])
        ase_atoms.set_initial_magnetic_moments([2.0, 0.0, 0.0])

        structure = Structure.from_ase(ase_atoms)
        assert structure.charge == -1
        assert structure.multiplicity == 3

    def test_info_used_when_arrays_unset(self):
        """`Atoms.info` should be used when the per-atom arrays were never set."""
        ase_atoms = AseAtoms(
            symbols=["O", "H", "H"],
            positions=_WATER_COORDS,
            info={"charge": 1, "spin": 2},
        )
        structure = Structure.from_ase(ase_atoms)
        assert structure.charge == 1
        assert structure.multiplicity == 2

    def test_defaults_without_arrays_or_info(self):
        """Without per-atom arrays and without `Atoms.info`, a neutral singlet is assumed."""
        ase_atoms = AseAtoms(symbols=["O", "H", "H"], positions=_WATER_COORDS)
        structure = Structure.from_ase(ase_atoms)
        assert structure.charge == 0
        assert structure.multiplicity == 1

    def test_explicit_arguments_win(self):
        """Explicit `charge` / `multiplicity` arguments should override both sources."""
        ase_atoms = AseAtoms(
            symbols=["O", "H", "H"],
            positions=_WATER_COORDS,
            info={"charge": 1, "spin": 2},
        )
        ase_atoms.set_initial_charges([-1.0, 0.0, 0.0])

        structure = Structure.from_ase(ase_atoms, charge=3, multiplicity=4)
        assert structure.charge == 3
        assert structure.multiplicity == 4
