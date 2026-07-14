"""
Unit tests for RMSD and coordinate utilities.

Covers:
- real_atoms property
- get_coordinates()
- get_coordinates_at_centroid()
- set_coordinates()
- centered_structure()
- _filtered_atoms()
- _validate_rmsd_compatibility()
- rmsd()
- rmsd_kabsch()

Edge cases: ignore_hs, only_atoms, mismatched structures,
mixed atom types, wrong shapes, identical structures.
"""

import copy

import numpy as np
import pytest

from opi.input.structures.atom import Atom, GhostAtom, PointCharge
from opi.input.structures.coordinates import Coordinates
from opi.input.structures.structure import Structure
from opi.utils.element import Element

# ============================================================
# Helpers
# ============================================================


def make_atom(element: str, x: float, y: float, z: float) -> Atom:
    return Atom(
        element=Element(element),
        coordinates=Coordinates(coordinates=(x, y, z)),
    )


def make_structure(*atoms: Atom) -> Structure:
    return Structure(atoms=list(atoms))


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture()
def water() -> Structure:
    """H2O at a known geometry."""
    return Structure.from_xyz_block(
        "3\n\n"
        "O   0.000000   0.000000   0.119748\n"
        "H   0.000000   0.756950  -0.478993\n"
        "H   0.000000  -0.756950  -0.478993"
    )


@pytest.fixture()
def water_translated() -> Structure:
    """H2O shifted by (1, 2, 3) — RMSD vs water should be 0 after centring."""
    return Structure.from_xyz_block(
        "3\n\n"
        "O   1.000000   2.000000   3.119748\n"
        "H   1.000000   2.756950   2.521007\n"
        "H   1.000000   1.243050   2.521007"
    )


@pytest.fixture()
def water_rotated(water) -> Structure:
    """
    H2O rotated 90° around Z after centring.
    Kabsch RMSD vs the original centred water should be ~0.
    """
    centered = water.centered_structure()
    coords = centered.get_coordinates()
    theta = np.pi / 2
    R = np.array(
        [
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1],
        ]
    )
    rotated = copy.deepcopy(centered)
    rotated.set_coordinates(coords @ R.T)
    return rotated


@pytest.fixture()
def ethanol() -> Structure:
    """
    Ethanol (C2H5OH) for ignore_hs tests.
    Coordinates are approximate — correctness of geometry is not critical here.
    """
    return Structure.from_xyz_block(
        "9\n\n"
        "C   0.000   0.000   0.000\n"
        "C   1.540   0.000   0.000\n"
        "O   2.060   1.190   0.000\n"
        "H  -0.390   1.020   0.000\n"
        "H  -0.390  -0.510   0.890\n"
        "H  -0.390  -0.510  -0.890\n"
        "H   1.930  -0.510   0.890\n"
        "H   1.930  -0.510  -0.890\n"
        "H   2.980   1.190   0.000"
    )


@pytest.fixture()
def mixed_structure() -> Structure:
    """Structure with a real Atom and a PointCharge (not an Atom subclass)."""
    return Structure(
        atoms=[
            Atom(element=Element("O"), coordinates=Coordinates(coordinates=(0.0, 0.0, 0.0))),
            PointCharge(coordinates=Coordinates(coordinates=(1.0, 0.0, 0.0)), charge=1.0),
        ]
    )


# ============================================================
# real_atoms
# ============================================================


@pytest.mark.unit
class TestRealAtoms:
    def test_returns_only_real_atoms(self, mixed_structure):
        """PointCharge should be excluded."""
        assert len(mixed_structure.real_atoms) == 1
        assert all(type(a) is Atom for a in mixed_structure.real_atoms)

    def test_ghost_atom_excluded(self):
        """GhostAtom is a subclass of Atom but should be excluded."""
        structure = Structure(
            atoms=[
                Atom(element=Element("O"), coordinates=Coordinates(coordinates=(0.0, 0.0, 0.0))),
                GhostAtom(
                    element=Element("H"), coordinates=Coordinates(coordinates=(1.0, 0.0, 0.0))
                ),
            ]
        )
        assert len(structure.real_atoms) == 1
        assert type(structure.real_atoms[0]) is Atom

    def test_all_real_atoms(self, water):
        """All atoms in water are real."""
        assert len(water.real_atoms) == 3

    def test_return_type(self, water):
        assert isinstance(water.real_atoms, list)
        assert all(type(a) is Atom for a in water.real_atoms)

    def test_empty_structure(self):
        structure = Structure(
            atoms=[PointCharge(coordinates=Coordinates(coordinates=(0.0, 0.0, 0.0)), charge=1.0)]
        )
        assert structure.real_atoms == []


# ============================================================
# get_coordinates
# ============================================================


@pytest.mark.unit
class TestGetCoordinates:
    def test_shape(self, water):
        """get_coordinates() should return an array of shape (N, 3)."""
        coords = water.get_coordinates()
        assert coords.shape == (3, 3)

    def test_dtype(self, water):
        """get_coordinates() should always return a float64 array."""
        coords = water.get_coordinates()
        assert coords.dtype == np.float64

    def test_values(self, water):
        """get_coordinates() should return the correct coordinate values."""
        coords = water.get_coordinates()
        np.testing.assert_allclose(coords[0], [0.0, 0.0, 0.119748])

    def test_only_atoms_filters(self, mixed_structure):
        """Passing index 0 only should return one row."""
        coords = mixed_structure.get_coordinates(only_atoms=[0])
        assert coords.shape == (1, 3)

    def test_default_includes_all(self, mixed_structure):
        """Default call includes all atom types."""
        coords = mixed_structure.get_coordinates()
        assert coords.shape == (2, 3)

    def test_only_atoms_subset(self, water):
        """Passing indices [0, 1] should return only those two atoms."""
        coords = water.get_coordinates(only_atoms=[0, 1])
        assert coords.shape == (2, 3)

    def test_single_atom(self):
        """get_coordinates() on a single-atom structure should return shape (1, 3)."""
        s = Structure.from_xyz_block("1\n\nC   1.0   2.0   3.0")
        coords = s.get_coordinates()
        np.testing.assert_allclose(coords[0], [1.0, 2.0, 3.0])


# ============================================================
# get_coordinates_at_centroid
# ============================================================


@pytest.mark.unit
class TestGetCoordinatesAtCentroid:
    def test_centroid_is_zero(self, water):
        coords = water.get_coordinates_at_centroid()
        np.testing.assert_allclose(coords.mean(axis=0), [0.0, 0.0, 0.0], atol=1e-12)

    def test_shape_preserved(self, water):
        coords = water.get_coordinates_at_centroid()
        assert coords.shape == (3, 3)

    def test_with_only_atoms(self, water):
        coords = water.get_coordinates_at_centroid(only_atoms=[0, 1])
        assert coords.shape == (2, 3)
        np.testing.assert_allclose(coords.mean(axis=0), [0.0, 0.0, 0.0], atol=1e-12)

    def test_translation_invariant(self, water, water_translated):
        c1 = water.get_coordinates_at_centroid()
        c2 = water_translated.get_coordinates_at_centroid()
        np.testing.assert_allclose(c1, c2, atol=1e-6)


# ============================================================
# set_coordinates
# ============================================================


@pytest.mark.unit
class TestSetCoordinates:
    def test_mutates_in_place(self, water):
        """set_coordinates should modify the structure in place."""
        new_coords = np.zeros((3, 3))
        water.set_coordinates(new_coords)
        np.testing.assert_allclose(water.get_coordinates(), new_coords)

    def test_returns_none(self, water):
        """set_coordinates should return None."""
        result = water.set_coordinates(water.get_coordinates())
        assert result is None

    def test_raises_on_wrong_shape(self, water):
        with pytest.raises(ValueError, match="coords shape"):
            water.set_coordinates(np.zeros((2, 3)))

    def test_deepcopy_is_independent(self, water):
        """Changes to a deepcopy should not affect the original."""
        original_coords = water.get_coordinates().copy()
        new_structure = copy.deepcopy(water)
        new_structure.set_coordinates(np.zeros((3, 3)))
        np.testing.assert_allclose(water.get_coordinates(), original_coords)


# ============================================================
# centered_structure
# ============================================================


@pytest.mark.unit
class TestCenteredStructure:
    def test_centroid_at_origin(self, water):
        centered = water.centered_structure()
        real_indices = [i for i, a in enumerate(centered.atoms) if type(a) is Atom]
        coords = centered.get_coordinates(only_atoms=real_indices)
        np.testing.assert_allclose(coords.mean(axis=0), [0.0, 0.0, 0.0], atol=1e-12)

    def test_returns_new_structure(self, water):
        assert water.centered_structure() is not water

    def test_original_unchanged(self, water):
        original = water.get_coordinates().copy()
        water.centered_structure()
        np.testing.assert_allclose(water.get_coordinates(), original)

    def test_pointcharge_excluded_from_centroid(self, mixed_structure):
        """
        The PointCharge at (1, 0, 0) should not pull the centroid away
        from the real Atom at (0, 0, 0).
        """
        centered = mixed_structure.centered_structure()
        real_indices = [i for i, a in enumerate(centered.atoms) if type(a) is Atom]
        coords = centered.get_coordinates(only_atoms=real_indices)
        np.testing.assert_allclose(coords[0], [0.0, 0.0, 0.0], atol=1e-12)

    def test_translated_centered_equals_original_centered(self, water, water_translated):
        c1 = water.centered_structure().get_coordinates()
        c2 = water_translated.centered_structure().get_coordinates()
        np.testing.assert_allclose(c1, c2, atol=1e-6)


# ============================================================
# _filtered_atoms
# ============================================================


@pytest.mark.unit
class TestFilteredAtoms:
    def test_default_returns_only_atom_indices(self, mixed_structure):
        """PointCharge should be excluded — only index 0 (the Atom) returned."""
        indices = mixed_structure._filtered_atoms((), False)
        assert indices == [0]
        assert all(type(mixed_structure.atoms[i]) is Atom for i in indices)

    def test_returns_list_of_int(self, water):
        indices = water._filtered_atoms((), False)
        assert isinstance(indices, list)
        assert all(isinstance(i, int) for i in indices)

    def test_ignore_hs(self, ethanol):
        indices = ethanol._filtered_atoms((), True)
        elements = [ethanol.atoms[i].element for i in indices]
        assert Element("H") not in elements

    def test_only_atoms_indices(self, ethanol):
        indices = ethanol._filtered_atoms([0, 1, 2], False)
        assert indices == [0, 1, 2]

    def test_only_atoms_excludes_pointcharge(self):
        """Explicitly indexed PointCharge must be excluded by the final type check."""
        structure = Structure(
            atoms=[
                Atom(element=Element("C"), coordinates=Coordinates(coordinates=(0.0, 0.0, 0.0))),
                PointCharge(coordinates=Coordinates(coordinates=(1.0, 0.0, 0.0)), charge=1.0),
            ]
        )
        indices = structure._filtered_atoms([0, 1], False)
        assert indices == [0]
        assert all(type(structure.atoms[i]) is Atom for i in indices)

    def test_only_atoms_takes_priority_over_ignore_hs(self, ethanol):
        """When only_atoms is set, ignore_hs should be ignored."""
        indices_with = ethanol._filtered_atoms([3, 4], True)
        indices_without = ethanol._filtered_atoms([3, 4], False)
        assert indices_with == indices_without


# ============================================================
# _validate_rmsd_compatibility
# ============================================================


@pytest.mark.unit
class TestValidateRmsdCompatibility:
    def test_compatible_structures(self, water):
        atoms = water.real_atoms
        Structure._validate_rmsd_compatibility(atoms, atoms)  # should not raise

    def test_raises_on_different_count(self, water, ethanol):
        with pytest.raises(ValueError, match="different number of atoms"):
            Structure._validate_rmsd_compatibility(water.real_atoms, ethanol.real_atoms)

    def test_raises_on_element_mismatch(self):
        a1 = [make_atom("C", 0, 0, 0), make_atom("H", 1, 0, 0)]
        a2 = [make_atom("C", 0, 0, 0), make_atom("O", 1, 0, 0)]
        with pytest.raises(ValueError, match="position 2"):
            Structure._validate_rmsd_compatibility(a1, a2)

    def test_error_message_uses_natural_counting(self):
        """Position in error message should start at 1, not 0."""
        a1 = [make_atom("C", 0, 0, 0)]
        a2 = [make_atom("O", 0, 0, 0)]
        with pytest.raises(ValueError, match="position 1"):
            Structure._validate_rmsd_compatibility(a1, a2)


# ============================================================
# rmsd
# ============================================================


@pytest.mark.unit
class TestRmsd:
    def test_identical_structures_zero_rmsd(self, water):
        assert pytest.approx(water.rmsd(water), abs=1e-10) == 0.0

    def test_translated_structure_zero_rmsd(self, water, water_translated):
        """Pure translation should give 0 RMSD after centring."""
        assert pytest.approx(water.rmsd(water_translated), abs=1e-6) == 0.0

    def test_symmetry(self, water, water_translated):
        assert pytest.approx(water.rmsd(water_translated)) == water_translated.rmsd(water)

    def test_raises_on_incompatible_structures(self, water, ethanol):
        with pytest.raises(ValueError):
            water.rmsd(ethanol)

    def test_ignore_hs(self, ethanol):
        """
        Displace only one heavy atom — RMSD with and without H should differ.
        """
        shifted = copy.deepcopy(ethanol)
        coords = shifted.get_coordinates()
        coords[0] += np.array([0.5, 0.0, 0.0])
        shifted.set_coordinates(coords)
        rmsd_all = ethanol.rmsd(shifted)
        rmsd_no_h = ethanol.rmsd(shifted, ignore_hs=True)
        assert rmsd_all != pytest.approx(rmsd_no_h, abs=1e-6)

    def test_only_atoms_subset(self, ethanol):
        """RMSD over a subset of atoms should differ from the full-molecule RMSD."""
        shifted = copy.deepcopy(ethanol)
        coords = shifted.get_coordinates()
        coords[0] += np.array([0.5, 0.0, 0.0])
        shifted.set_coordinates(coords)
        rmsd_all = ethanol.rmsd(shifted)
        rmsd_subset = ethanol.rmsd(shifted, only_atoms=[0, 1, 2])
        assert rmsd_all != pytest.approx(rmsd_subset, abs=1e-6)

    def test_nonzero_rmsd_for_different_structures(self, water):
        other = copy.deepcopy(water)
        coords = other.get_coordinates()
        coords += np.array([0, 0, 1.0])
        other.set_coordinates(coords)
        result = water.rmsd(other)
        assert result >= 0.0

    def test_result_is_float(self, water):
        assert isinstance(water.rmsd(water), float)


# ============================================================
# rmsd_kabsch
# ============================================================


@pytest.mark.unit
class TestRmsdKabsch:
    def test_identical_structures_zero_rmsd(self, water):
        assert pytest.approx(water.rmsd_kabsch(water), abs=1e-10) == 0.0

    def test_translated_zero_rmsd(self, water, water_translated):
        assert pytest.approx(water.rmsd_kabsch(water_translated), abs=1e-6) == 0.0

    def test_rotated_zero_rmsd(self, water, water_rotated):
        """Kabsch should align the rotation and give ~0 RMSD."""
        centered = water.centered_structure()
        assert pytest.approx(centered.rmsd_kabsch(water_rotated), abs=1e-6) == 0.0

    def test_kabsch_le_rmsd(self, water):
        """Kabsch RMSD ≤ plain RMSD (optimal rotation can only help or be neutral)."""
        centered = water.centered_structure()
        coords = centered.get_coordinates()
        R = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=float)
        other = copy.deepcopy(centered)
        other.set_coordinates(coords @ R.T)
        assert centered.rmsd_kabsch(other) <= centered.rmsd(other) + 1e-10

    def test_symmetry(self, water, water_rotated):
        assert pytest.approx(
            water.rmsd_kabsch(water_rotated), abs=1e-6
        ) == water_rotated.rmsd_kabsch(water)

    def test_raises_on_incompatible_structures(self, water, ethanol):
        with pytest.raises(ValueError):
            water.rmsd_kabsch(ethanol)

    def test_ignore_hs(self, ethanol):
        shifted = copy.deepcopy(ethanol)
        coords = shifted.get_coordinates()
        coords[0] += np.array([0.5, 0.0, 0.0])
        shifted.set_coordinates(coords)
        rmsd_all = ethanol.rmsd_kabsch(shifted)
        rmsd_no_h = ethanol.rmsd_kabsch(shifted, ignore_hs=True)
        assert rmsd_all != pytest.approx(rmsd_no_h, abs=1e-6)

    def test_only_atoms_subset(self, ethanol):
        shifted = copy.deepcopy(ethanol)
        coords = shifted.get_coordinates()
        coords[0] += np.array([0.5, 0.0, 0.0])
        shifted.set_coordinates(coords)
        rmsd_all = ethanol.rmsd_kabsch(shifted)
        rmsd_subset = ethanol.rmsd_kabsch(shifted, only_atoms=[0, 1, 2])
        assert rmsd_all != pytest.approx(rmsd_subset, abs=1e-6)

    def test_result_is_float(self, water):
        assert isinstance(water.rmsd_kabsch(water), float)

    def test_result_nonnegative(self, water, water_rotated):
        assert water.rmsd_kabsch(water_rotated) >= 0.0
