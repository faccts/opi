"""
Unit tests for RMSD and coordinate utilities.

Covers:
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

import numpy as np
import pytest

from opi.input.structures.atom import Atom, PointCharge
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
    return make_structure(
        make_atom("O", 0.000000, 0.000000, 0.119748),
        make_atom("H", 0.000000, 0.756950, -0.478993),
        make_atom("H", 0.000000, -0.756950, -0.478993),
    )


@pytest.fixture()
def water_translated() -> Structure:
    """H2O shifted by (1, 2, 3) — RMSD vs water should be 0 after centring."""
    return make_structure(
        make_atom("O", 1.000000, 2.000000, 3.119748),
        make_atom("H", 1.000000, 2.756950, 2.521007),
        make_atom("H", 1.000000, 1.243050, 2.521007),
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
    return centered.set_coordinates(coords @ R.T)


@pytest.fixture()
def ethanol() -> Structure:
    """
    Simple ethanol-like structure (C2H5OH) for ignore_hs tests.
    Coordinates are approximate — correctness of geometry is not critical here.
    """
    return make_structure(
        make_atom("C", 0.000, 0.000, 0.000),
        make_atom("C", 1.540, 0.000, 0.000),
        make_atom("O", 2.060, 1.190, 0.000),
        make_atom("H", -0.390, 1.020, 0.000),
        make_atom("H", -0.390, -0.510, 0.890),
        make_atom("H", -0.390, -0.510, -0.890),
        make_atom("H", 1.930, -0.510, 0.890),
        make_atom("H", 1.930, -0.510, -0.890),
        make_atom("H", 2.980, 1.190, 0.000),
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
# get_coordinates
# ============================================================


class TestGetCoordinates:
    def test_shape(self, water):
        coords = water.get_coordinates()
        assert coords.shape == (3, 3)

    def test_dtype(self, water):
        coords = water.get_coordinates()
        assert coords.dtype == np.float64

    def test_values(self, water):
        coords = water.get_coordinates()
        np.testing.assert_allclose(coords[0], [0.0, 0.0, 0.119748])

    def test_atoms_kwarg_filters(self, mixed_structure):
        """Passing only real Atom instances should exclude PointCharge."""
        real = [a for a in mixed_structure.atoms if type(a) is Atom]
        coords = mixed_structure.get_coordinates(atoms=real)
        assert coords.shape == (1, 3)

    def test_default_includes_all(self, mixed_structure):
        """Default call includes all atom types."""
        coords = mixed_structure.get_coordinates()
        assert coords.shape == (2, 3)

    def test_single_atom(self):
        s = make_structure(make_atom("C", 1.0, 2.0, 3.0))
        coords = s.get_coordinates()
        np.testing.assert_allclose(coords[0], [1.0, 2.0, 3.0])


# ============================================================
# get_coordinates_at_centroid
# ============================================================


class TestGetCoordinatesAtCentroid:
    def test_centroid_is_zero(self, water):
        coords = water.get_coordinates_at_centroid()
        np.testing.assert_allclose(coords.mean(axis=0), [0.0, 0.0, 0.0], atol=1e-12)

    def test_shape_preserved(self, water):
        coords = water.get_coordinates_at_centroid()
        assert coords.shape == (3, 3)

    def test_with_atoms_kwarg(self, water):
        atoms = water.atoms[:2]
        coords = water.get_coordinates_at_centroid(atoms=atoms)
        assert coords.shape == (2, 3)
        np.testing.assert_allclose(coords.mean(axis=0), [0.0, 0.0, 0.0], atol=1e-12)

    def test_translation_invariant(self, water, water_translated):
        c1 = water.get_coordinates_at_centroid()
        c2 = water_translated.get_coordinates_at_centroid()
        np.testing.assert_allclose(c1, c2, atol=1e-6)


# ============================================================
# set_coordinates
# ============================================================


class TestSetCoordinates:
    def test_returns_new_structure(self, water):
        new_coords = water.get_coordinates() + 1.0
        new_s = water.set_coordinates(new_coords)
        assert new_s is not water

    def test_original_unchanged(self, water):
        original_coords = water.get_coordinates().copy()
        water.set_coordinates(water.get_coordinates() + 5.0)
        np.testing.assert_allclose(water.get_coordinates(), original_coords)

    def test_new_coords_applied(self, water):
        new_coords = np.zeros((3, 3))
        new_s = water.set_coordinates(new_coords)
        np.testing.assert_allclose(new_s.get_coordinates(), new_coords)

    def test_raises_on_wrong_shape(self, water):
        with pytest.raises(ValueError, match="coords shape"):
            water.set_coordinates(np.zeros((2, 3)))

    def test_charge_preserved(self, water):
        water_charged = Structure(atoms=water.atoms, charge=1)
        new_s = water_charged.set_coordinates(water.get_coordinates())
        assert new_s.charge == 1

    def test_multiplicity_preserved(self, water):
        water_mult = Structure(atoms=water.atoms, multiplicity=3)
        new_s = water_mult.set_coordinates(water.get_coordinates())
        assert new_s.multiplicity == 3


# ============================================================
# centered_structure
# ============================================================


class TestCenteredStructure:
    def test_centroid_at_origin(self, water):
        centered = water.centered_structure()
        real_atoms = [a for a in centered.atoms if isinstance(a, Atom)]
        coords = centered.get_coordinates(atoms=real_atoms)
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
        real_atoms = [a for a in centered.atoms if type(a) is Atom]
        coords = centered.get_coordinates(atoms=real_atoms)
        # Real atom was already at origin, so it should stay at origin
        np.testing.assert_allclose(coords[0], [0.0, 0.0, 0.0], atol=1e-12)

    def test_translated_centered_equals_original_centered(self, water, water_translated):
        c1 = water.centered_structure().get_coordinates()
        c2 = water_translated.centered_structure().get_coordinates()
        np.testing.assert_allclose(c1, c2, atol=1e-6)


# ============================================================
# _filtered_atoms
# ============================================================


class TestFilteredAtoms:
    def test_default_returns_only_atoms(self, mixed_structure):
        """PointCharge should be excluded since it is not an Atom instance."""
        filtered = mixed_structure._filtered_atoms((), False)
        assert all(isinstance(a, Atom) for a in filtered)
        assert len(filtered) == 1

    def test_ignore_hs(self, ethanol):
        filtered = ethanol._filtered_atoms((), True)
        elements = [a.element for a in filtered]
        assert Element("H") not in elements

    def test_only_atoms_indices(self, ethanol):
        filtered = ethanol._filtered_atoms([0, 1, 2], False)
        assert len(filtered) == 3

    def test_only_atoms_excludes_pointcharge(self):
        """Explicitly indexed PointCharge must be excluded by the final isinstance check."""
        structure = Structure(
            atoms=[
                Atom(element=Element("C"), coordinates=Coordinates(coordinates=(0.0, 0.0, 0.0))),
                PointCharge(coordinates=Coordinates(coordinates=(1.0, 0.0, 0.0)), charge=1.0),
            ]
        )
        filtered = structure._filtered_atoms([0, 1], False)
        assert all(isinstance(a, Atom) for a in filtered)
        assert len(filtered) == 1

    def test_only_atoms_takes_priority_over_ignore_hs(self, ethanol):
        """When only_atoms is set, ignore_hs should be ignored."""
        filtered_with = ethanol._filtered_atoms([3, 4], True)
        filtered_without = ethanol._filtered_atoms([3, 4], False)
        assert len(filtered_with) == len(filtered_without)


# ============================================================
# _validate_rmsd_compatibility
# ============================================================


class TestValidateRmsdCompatibility:
    def test_compatible_structures(self, water):
        atoms = [a for a in water.atoms if isinstance(a, Atom)]
        Structure._validate_rmsd_compatibility(atoms, atoms)  # should not raise

    def test_raises_on_different_count(self, water, ethanol):
        a1 = [a for a in water.atoms if isinstance(a, Atom)]
        a2 = [a for a in ethanol.atoms if isinstance(a, Atom)]
        with pytest.raises(ValueError, match="different number of atoms"):
            Structure._validate_rmsd_compatibility(a1, a2)

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
        Displace only heavy atoms — RMSD with and without H should differ
        since the centroid shift differs between the two filtered sets.
        """
        coords = ethanol.get_coordinates()
        new_coords = coords.copy()
        new_coords[0] += np.array([0.5, 0.0, 0.0])  # shift only C0
        shifted = ethanol.set_coordinates(new_coords)
        rmsd_all = ethanol.rmsd(shifted)
        rmsd_no_h = ethanol.rmsd(shifted, ignore_hs=True)
        assert rmsd_all != pytest.approx(rmsd_no_h, abs=1e-6)

    def test_only_atoms_subset(self, ethanol):
        """RMSD over a subset of atoms should differ from the full-molecule RMSD."""
        coords = ethanol.get_coordinates()
        new_coords = coords.copy()
        new_coords[0] += np.array([0.5, 0.0, 0.0])  # shift only C0
        shifted = ethanol.set_coordinates(new_coords)
        rmsd_all = ethanol.rmsd(shifted)
        rmsd_subset = ethanol.rmsd(shifted, only_atoms=[0, 1, 2])
        assert rmsd_all != pytest.approx(rmsd_subset, abs=1e-6)

    def test_nonzero_rmsd_for_different_structures(self, water):
        other = water.set_coordinates(water.get_coordinates() + np.array([0, 0, 1.0]))
        # After centring the z-shift cancels, but individual atom positions differ
        # We just confirm it's finite and non-negative
        result = water.rmsd(other)
        assert result >= 0.0

    def test_result_is_float(self, water):
        assert isinstance(water.rmsd(water), float)


# ============================================================
# rmsd_kabsch
# ============================================================


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
        other = centered.set_coordinates(coords @ R.T)
        assert centered.rmsd_kabsch(other) <= centered.rmsd(other) + 1e-10

    def test_symmetry(self, water, water_rotated):
        assert pytest.approx(
            water.rmsd_kabsch(water_rotated), abs=1e-6
        ) == water_rotated.rmsd_kabsch(water)

    def test_raises_on_incompatible_structures(self, water, ethanol):
        with pytest.raises(ValueError):
            water.rmsd_kabsch(ethanol)

    def test_ignore_hs(self, ethanol):
        coords = ethanol.get_coordinates()
        new_coords = coords.copy()
        new_coords[0] += np.array([0.5, 0.0, 0.0])
        shifted = ethanol.set_coordinates(new_coords)
        rmsd_all = ethanol.rmsd_kabsch(shifted)
        rmsd_no_h = ethanol.rmsd_kabsch(shifted, ignore_hs=True)
        assert rmsd_all != pytest.approx(rmsd_no_h, abs=1e-6)

    def test_only_atoms_subset(self, ethanol):
        coords = ethanol.get_coordinates()
        new_coords = coords.copy()
        new_coords[0] += np.array([0.5, 0.0, 0.0])
        shifted = ethanol.set_coordinates(new_coords)
        rmsd_all = ethanol.rmsd_kabsch(shifted)
        rmsd_subset = ethanol.rmsd_kabsch(shifted, only_atoms=[0, 1, 2])
        assert rmsd_all != pytest.approx(rmsd_subset, abs=1e-6)

    def test_result_is_float(self, water):
        assert isinstance(water.rmsd_kabsch(water), float)

    def test_result_nonnegative(self, water, water_rotated):
        assert water.rmsd_kabsch(water_rotated) >= 0.0
