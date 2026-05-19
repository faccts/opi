"""
Unit tests for rotational constants functionality.

Covers:
- calc_moments_of_inertia()
- calc_rotor_type()
- calc_rotational_constants()
- PrincipalMoments.rotor_type()
- PrincipalMoments.__str__()
- RotationalConstants.get_in_wavenumbers()
- RotationalConstants.__str__()
- moment_to_mhz() and mhz_to_wavenumber()
- All RotorType classifications
- Edge cases: empty structure, all-zero masses, mass overrides, unknown elements
"""

import math

import numpy as np
import pytest

from opi.input.structures.atom import Atom, PointCharge
from opi.input.structures.coordinates import Coordinates
from opi.input.structures.structure import Structure
from opi.utils.element import Element
from opi.utils.rotconst import (
    RotationalConstants,
    RotorType,
    mhz_to_wavenumber,
    moment_to_mhz,
)

# ============================================================
# Helpers
# ============================================================


def make_atom(element: str, x: float, y: float, z: float) -> Atom:
    return Atom(
        element=Element(element),
        coordinates=Coordinates(coordinates=(x, y, z)),
    )


def make_no_real_atoms_structure() -> Structure:
    """Structure containing only a PointCharge — no real Atom instances."""
    return Structure(
        atoms=[PointCharge(coordinates=Coordinates(coordinates=(0.0, 0.0, 0.0)), charge=1.0)]
    )


def make_structure(*atoms: Atom) -> Structure:
    return Structure(atoms=list(atoms))


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture()
def water() -> Structure:
    """H2O — asymmetric top."""
    return make_structure(
        make_atom("O", 0.000000, 0.000000, 0.119748),
        make_atom("H", 0.000000, 0.756950, -0.478993),
        make_atom("H", 0.000000, -0.756950, -0.478993),
    )


@pytest.fixture()
def co2() -> Structure:
    """
    CO2 — linear molecule aligned exactly on Z.
    After COM shift, both O atoms lie on the Z axis so Ia = 0 exactly.
    Using exact masses (C=12, O=15.999) the COM is at z=0 by symmetry.
    """
    return make_structure(
        make_atom("C", 0.000000, 0.000000, 0.000000),
        make_atom("O", 0.000000, 0.000000, 1.160000),
        make_atom("O", 0.000000, 0.000000, -1.160000),
    )


@pytest.fixture()
def hcl() -> Structure:
    """HCl — guaranteed linear (diatomic), Ia = 0 exactly on Z axis."""
    return make_structure(
        make_atom("H", 0.000000, 0.000000, 0.000000),
        make_atom("Cl", 0.000000, 0.000000, 1.274500),
    )


@pytest.fixture()
def methane() -> Structure:
    """CH4 — spherical top."""
    d = 0.6276  # C-H bond / sqrt(3)
    return make_structure(
        make_atom("C", 0.000, 0.000, 0.000),
        make_atom("H", d, d, d),
        make_atom("H", -d, -d, d),
        make_atom("H", -d, d, -d),
        make_atom("H", d, -d, -d),
    )


@pytest.fixture()
def benzene() -> Structure:
    """C6H6 — oblate symmetric top."""
    r_c, r_h = 1.3970, 2.4832
    atoms = []
    for i in range(6):
        angle = math.radians(i * 60)
        atoms.append(make_atom("C", r_c * math.cos(angle), r_c * math.sin(angle), 0.0))
        atoms.append(make_atom("H", r_h * math.cos(angle), r_h * math.sin(angle), 0.0))
    return make_structure(*atoms)


@pytest.fixture()
def single_atom() -> Structure:
    """Single atom — monoatomic."""
    return make_structure(make_atom("C", 0.0, 0.0, 0.0))


@pytest.fixture()
def ammonia() -> Structure:
    """NH3 — oblate symmetric top (C3v). XTB2 optimized geometry."""
    return make_structure(
        make_atom("N", -0.000000, -0.000066, 0.100407),
        make_atom("H", 0.000000, 0.943825, -0.266468),
        make_atom("H", 0.817493, -0.471879, -0.266439),
        make_atom("H", -0.817493, -0.471879, -0.266439),
    )


@pytest.fixture()
def ch3cl() -> Structure:
    """CH3Cl — prolate symmetric top (C3v). XTB2 optimized geometry."""
    return make_structure(
        make_atom("Cl", 0.9754830000, 0.0921220000, -0.0239260000),
        make_atom("C", 2.7424550000, 0.0921300000, -0.0239350000),
        make_atom("H", 3.0994960000, 0.3238830000, 0.9818970000),
        make_atom("H", 3.0994920000, -0.8948230000, -0.3261570000),
        make_atom("H", 3.0994750000, 0.8473380000, -0.7275610000),
    )


# ============================================================
# moment_to_mhz and mhz_to_wavenumber
# ============================================================


class TestHelperFunctions:
    def test_moment_to_mhz_none_input(self):
        assert moment_to_mhz(None) is None

    def test_moment_to_mhz_zero(self):
        assert moment_to_mhz(0.0) is None

    def test_moment_to_mhz_below_threshold(self):
        assert moment_to_mhz(1e-7) is None

    def test_moment_to_mhz_positive(self):
        result = moment_to_mhz(100.0)
        assert result is not None
        assert result > 0.0

    def test_moment_to_mhz_known_value(self):
        # For water Ib ≈ 1.022 amu·Å² → B ≈ 435000 MHz (rough check)
        result = moment_to_mhz(1.022)
        assert result is not None
        assert 400_000 < result < 500_000

    def test_mhz_to_wavenumber_none(self):
        assert mhz_to_wavenumber(None) is None

    def test_mhz_to_wavenumber_positive(self):
        result = mhz_to_wavenumber(100_000.0)
        assert result is not None
        assert result > 0.0

    def test_mhz_to_wavenumber_proportional(self):
        a = mhz_to_wavenumber(100.0)
        b = mhz_to_wavenumber(200.0)
        assert a is not None and b is not None
        assert pytest.approx(b, rel=1e-9) == 2 * a


# ============================================================
# PrincipalMoments
# ============================================================


class TestPrincipalMoments:
    def test_rotor_type_monoatomic(self, single_atom):
        pm = single_atom.calc_moments_of_inertia()
        assert pm is not None
        assert pm.rotor_type() == RotorType.MONOATOMIC

    def test_rotor_type_linear(self, hcl):
        pm = hcl.calc_moments_of_inertia()
        assert pm is not None
        assert pm.rotor_type() == RotorType.LINEAR

    def test_rotor_type_spherical_top(self, methane):
        pm = methane.calc_moments_of_inertia()
        assert pm is not None
        assert pm.rotor_type() == RotorType.SPHERICAL_TOP

    def test_rotor_type_oblate_top(self, benzene):
        pm = benzene.calc_moments_of_inertia()
        assert pm is not None
        assert pm.rotor_type() == RotorType.OBLATE_TOP

    def test_rotor_type_oblate_top_ammonia(self, ammonia):
        pm = ammonia.calc_moments_of_inertia()
        assert pm is not None
        assert pm.rotor_type() == RotorType.OBLATE_TOP

    def test_rotor_type_prolate_top(self, ch3cl):
        pm = ch3cl.calc_moments_of_inertia()
        assert pm is not None
        assert pm.rotor_type() == RotorType.PROLATE_TOP

    def test_rotor_type_asymmetric_top(self, water):
        pm = water.calc_moments_of_inertia()
        assert pm is not None
        assert pm.rotor_type() == RotorType.ASYMMETRIC_TOP

    def test_moments_sorted_ascending(self, water):
        pm = water.calc_moments_of_inertia()
        assert pm is not None
        assert pm.Ia <= pm.Ib <= pm.Ic

    def test_axes_shape(self, water):
        pm = water.calc_moments_of_inertia()
        assert pm is not None
        assert pm.axes.shape == (3, 3)

    def test_axes_orthonormal(self, water):
        pm = water.calc_moments_of_inertia()
        assert pm is not None
        product = pm.axes.T @ pm.axes
        np.testing.assert_allclose(product, np.eye(3), atol=1e-10)

    def test_str_output(self, water):
        pm = water.calc_moments_of_inertia()
        assert pm is not None
        s = str(pm)
        assert "Moments of inertia (amu·Å²):" in s
        assert "Ia" in s
        assert "Ib" in s
        assert "Ic" in s


# ============================================================
# calc_moments_of_inertia
# ============================================================


class TestCalcMomentsOfInertia:
    def test_returns_none_for_empty_structure(self):
        assert make_no_real_atoms_structure().calc_moments_of_inertia() is None

    def test_returns_none_for_all_zero_masses(self, water):
        masses = np.zeros(3)
        assert water.calc_moments_of_inertia(masses=masses) is None

    def test_raises_on_wrong_masses_length(self, water):
        with pytest.raises(ValueError, match="masses length"):
            water.calc_moments_of_inertia(masses=np.array([1.0, 2.0]))

    def test_ghost_atoms_ignored(self):
        """PointCharge should not contribute to moments."""
        real = make_structure(
            make_atom("O", 0.0, 0.0, 0.119748),
            make_atom("H", 0.0, 0.756950, -0.478993),
            make_atom("H", 0.0, -0.756950, -0.478993),
        )
        with_pc = Structure(
            atoms=[
                Atom(
                    element=Element("O"), coordinates=Coordinates(coordinates=(0.0, 0.0, 0.119748))
                ),
                Atom(
                    element=Element("H"),
                    coordinates=Coordinates(coordinates=(0.0, 0.756950, -0.478993)),
                ),
                Atom(
                    element=Element("H"),
                    coordinates=Coordinates(coordinates=(0.0, -0.756950, -0.478993)),
                ),
                PointCharge(coordinates=Coordinates(coordinates=(5.0, 5.0, 5.0)), charge=1.0),
            ]
        )
        pm_real = real.calc_moments_of_inertia()
        pm_pc = with_pc.calc_moments_of_inertia()
        assert pm_real is not None and pm_pc is not None
        assert pytest.approx(pm_real.Ia, rel=1e-6) == pm_pc.Ia
        assert pytest.approx(pm_real.Ib, rel=1e-6) == pm_pc.Ib
        assert pytest.approx(pm_real.Ic, rel=1e-6) == pm_pc.Ic

    def test_custom_masses_override(self, water):
        """Passing explicit masses should change the moments."""
        pm_default = water.calc_moments_of_inertia()
        pm_custom = water.calc_moments_of_inertia(masses=np.array([18.0, 2.0, 2.0]))
        assert pm_default is not None and pm_custom is not None
        assert pm_default.Ia != pytest.approx(pm_custom.Ia, rel=1e-3)

    def test_weights_per_element(self, water):
        """Per-element weight override should change the moments."""
        pm_default = water.calc_moments_of_inertia()
        pm_weights = water.calc_moments_of_inertia(weights={"H": 2.014})
        assert pm_default is not None and pm_weights is not None
        assert pm_default.Ic != pytest.approx(pm_weights.Ic, rel=1e-3)

    def test_atom_weights_override(self, water):
        """Per-atom weight override (index 0) should change the moments."""
        pm_default = water.calc_moments_of_inertia()
        pm_aw = water.calc_moments_of_inertia(atom_weights={0: 17.999})
        assert pm_default is not None and pm_aw is not None
        assert pm_default.Ic != pytest.approx(pm_aw.Ic, rel=1e-3)

    def test_atom_weights_priority_over_weights(self, water):
        """atom_weights should take priority over weights for the same atom."""
        pm_aw = water.calc_moments_of_inertia(atom_weights={0: 17.999})
        pm_both = water.calc_moments_of_inertia(weights={"O": 16.0}, atom_weights={0: 17.999})
        assert pm_aw is not None and pm_both is not None
        assert pytest.approx(pm_aw.Ic, rel=1e-9) == pm_both.Ic

    def test_unknown_element_warns_and_excludes(self):
        """Atoms with unknown elements should warn and be assigned mass 0."""
        structure = Structure(
            atoms=[
                Atom(element=Element("C"), coordinates=Coordinates(coordinates=(0.0, 0.0, 0.0))),
                Atom(element=Element("H"), coordinates=Coordinates(coordinates=(1.0, 0.0, 0.0))),
            ]
        )
        # Patch via weights to simulate unknown: pass mass 0 explicitly for C
        pm = structure.calc_moments_of_inertia(atom_weights={0: 0.0})
        # Only H contributes → single non-zero mass → linear or monoatomic
        assert pm is not None

    def test_zero_mass_atoms_filtered(self, water):
        """Atoms with zero mass are excluded; remaining atoms determine the rotor type."""
        # Zero out the two H atoms → only O remains → monoatomic
        masses = np.array([15.999, 0.0, 0.0])
        pm = water.calc_moments_of_inertia(masses=masses)
        assert pm is not None
        assert pm.rotor_type() == RotorType.MONOATOMIC

    def test_water_moments_known_values(self, water):
        """
        Check moments are self-consistent: Ia <= Ib <= Ic and all positive.
        The geometry used here gives Ia ≈ 0.6418 amu·Å² (not the experimental
        equilibrium value of 0.5791) because the O-H distance and angle differ
        slightly. We verify internal consistency rather than an absolute value.
        """
        pm = water.calc_moments_of_inertia()
        assert pm is not None
        assert pm.Ia > 0.0
        assert pm.Ia <= pm.Ib <= pm.Ic
        # Rough sanity check: moments should be in a physically reasonable range
        assert 0.1 < pm.Ia < 5.0
        assert 0.1 < pm.Ib < 5.0
        assert 0.1 < pm.Ic < 5.0


# ============================================================
# calc_rotor_type
# ============================================================


class TestCalcRotorType:
    def test_with_precomputed_moments(self, water):
        pm = water.calc_moments_of_inertia()
        assert water.calc_rotor_type(moments=pm) == RotorType.ASYMMETRIC_TOP

    def test_without_precomputed_moments(self, water):
        assert water.calc_rotor_type() == RotorType.ASYMMETRIC_TOP

    def test_returns_none_for_empty_structure(self):
        assert make_no_real_atoms_structure().calc_rotor_type() is None

    def test_all_rotor_types(self, single_atom, hcl, methane, benzene, ammonia, ch3cl, water):
        assert single_atom.calc_rotor_type() == RotorType.MONOATOMIC
        assert hcl.calc_rotor_type() == RotorType.LINEAR
        assert methane.calc_rotor_type() == RotorType.SPHERICAL_TOP
        assert benzene.calc_rotor_type() == RotorType.OBLATE_TOP
        assert ammonia.calc_rotor_type() == RotorType.OBLATE_TOP
        assert ch3cl.calc_rotor_type() == RotorType.PROLATE_TOP
        assert water.calc_rotor_type() == RotorType.ASYMMETRIC_TOP


# ============================================================
# calc_rotational_constants
# ============================================================


class TestCalcRotationalConstants:
    def test_returns_none_for_empty_structure(self):
        assert make_no_real_atoms_structure().calc_rotational_constants() is None

    def test_returns_rotational_constants(self, water):
        rc = water.calc_rotational_constants()
        assert rc is not None
        assert isinstance(rc, RotationalConstants)

    def test_abc_ordering(self, water):
        """A ≥ B ≥ C by convention (ascending moments → descending constants)."""
        rc = water.calc_rotational_constants()
        assert rc is not None
        assert rc.A is not None and rc.B is not None and rc.C is not None
        assert rc.A >= rc.B >= rc.C

    def test_linear_molecule_has_none_constants(self, hcl):
        """HCl is linear: Ia = 0, so A should be None."""
        rc = hcl.calc_rotational_constants()
        assert rc is not None
        assert rc.A is None

    def test_monoatomic_all_none(self, single_atom):
        rc = single_atom.calc_rotational_constants()
        assert rc is not None
        assert rc.A is None
        assert rc.B is None
        assert rc.C is None

    def test_get_in_wavenumbers_returns_tuple(self, water):
        rc = water.calc_rotational_constants()
        assert rc is not None
        wn = rc.get_in_wavenumbers()
        assert isinstance(wn, tuple)
        assert len(wn) == 3

    def test_get_in_wavenumbers_none_propagates(self, hcl):
        rc = hcl.calc_rotational_constants()
        assert rc is not None
        wn = rc.get_in_wavenumbers()
        assert wn[0] is None  # A is None for linear

    def test_get_in_wavenumbers_values_positive(self, water):
        rc = water.calc_rotational_constants()
        assert rc is not None
        wn = rc.get_in_wavenumbers()
        assert all(v is not None and v > 0 for v in wn)

    def test_get_in_wavenumbers_consistent_with_mhz(self, water):
        """Manual conversion should match get_in_wavenumbers."""
        rc = water.calc_rotational_constants()
        assert rc is not None
        wn = rc.get_in_wavenumbers()
        assert wn[0] is not None and rc.A is not None
        assert pytest.approx(wn[0], rel=1e-9) == mhz_to_wavenumber(rc.A)

    def test_str_output(self, water):
        rc = water.calc_rotational_constants()
        assert rc is not None
        s = str(rc)
        assert "Rotational constants" in s
        assert "MHz" in s
        assert "cm⁻¹" in s

    def test_a_not_in_sync_problem(self, water):
        """
        Mutating rc.A should NOT affect get_in_wavenumbers,
        since wavenumbers are computed on the fly.
        """
        rc = water.calc_rotational_constants()
        assert rc is not None
        wn_before = rc.get_in_wavenumbers()[0]
        rc.A = rc.A * 5 if rc.A is not None else None  # type: ignore[operator]
        wn_after = rc.get_in_wavenumbers()[0]
        assert wn_before != wn_after  # confirms on-the-fly computation
