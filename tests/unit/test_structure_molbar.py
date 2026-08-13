"""
Unit tests for MolBar functionality.

MolBar is an optional dependency. All tests in this module are skipped
automatically if MolBar is not installed.

Covers:
- MolBarMode classification
- requires_molbar() decorator
- Structure._validate_molbar_mode()
- Structure._get_molbar_from_coordinates()
- Structure.calculate_molbar()
- Structure.calculate_molbar_data()

Edge cases: invalid mode, empty structure, ghost atom exclusion,
point charge exclusion, mode case-insensitivity.
"""

import pytest

pytest.importorskip("molbar", reason="MolBar not installed")

from importlib.metadata import version

import numpy as np

from opi.input.structures.atom import Atom, GhostAtom, PointCharge
from opi.input.structures.coordinates import Coordinates
from opi.input.structures.structure import Structure
from opi.utils.element import Element
from opi.utils.molbar import MolBarMode, call_molbar, requires_molbar

# > Version of the installed MolBar, read from package metadata rather than a
# > hard-coded literal so the tests stay valid across MolBar releases.
MOLBAR_VERSION = version("molbar")

# ============================================================
# Helpers
# ============================================================


def make_atom(element: str, x: float, y: float, z: float) -> Atom:
    """Convenience helper for building a single `Atom` at given coordinates."""
    return Atom(
        element=Element(element),
        coordinates=Coordinates(coordinates=(x, y, z)),
    )


# > Reference water geometry in list form, matching the XYZ block used by the
# > `water` fixture. Used by the `call_molbar` tests, which need raw
# > coordinates rather than an XYZ string.
_WATER_COORDS = [
    [0.0, 0.0, 0.119748],
    [0.0, 0.756950, -0.478993],
    [0.0, -0.756950, -0.478993],
]
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
def no_real_atoms_structure() -> Structure:
    """Structure containing only a PointCharge — no real Atom instances."""
    return Structure(
        atoms=[PointCharge(coordinates=Coordinates(coordinates=(0.0, 0.0, 0.0)), charge=1.0)]
    )


# ============================================================
# MolBarMode
# ============================================================


@pytest.mark.unit
class TestMolBarMode:
    def test_mb_value(self):
        """`MolBarMode.MB` should have value `"mb"`."""
        assert MolBarMode.MB == "mb"

    def test_topo_value(self):
        """`MolBarMode.TOPO` should have value `"topo"`."""
        assert MolBarMode.TOPO == "topo"

    def test_case_insensitive_mb(self):
        """`MolBarMode` should accept `"MB"` case-insensitively."""
        assert MolBarMode("MB") == MolBarMode.MB

    def test_case_insensitive_topo(self):
        """`MolBarMode` should accept `"TOPO"` case-insensitively."""
        assert MolBarMode("TOPO") == MolBarMode.TOPO

    def test_invalid_mode_raises(self):
        """`MolBarMode` should raise `ValueError` for an invalid mode string."""
        with pytest.raises(ValueError):
            MolBarMode("invalid")


# ============================================================
# requires_molbar decorator
# ============================================================


@pytest.mark.unit
class TestRequiresMolbar:
    def test_decorated_function_runs(self):
        """A function decorated with `requires_molbar()` should run normally when MolBar is installed."""

        @requires_molbar
        def dummy() -> str:
            return "ok"

        assert dummy() == "ok"


# ============================================================
# call_molbar input-type conversion
# ============================================================


@pytest.mark.unit
class TestCallMolbar:
    def test_accepts_element_objects(self):
        """`call_molbar()` should accept a list of `Element` instances."""
        result = call_molbar(
            elements=[Element("O"), Element("H"), Element("H")],
            coordinates=np.array(_WATER_COORDS),
            total_charge=0,
            mode=MolBarMode.MB,
            return_data=False,
        )
        assert isinstance(result, str)

    def test_accepts_string_symbols_and_list_coords(self):
        """`call_molbar()` should accept element-symbol strings and a nested list."""
        result = call_molbar(
            elements=["O", "H", "H"],
            coordinates=_WATER_COORDS,
            total_charge=0,
            mode=MolBarMode.MB,
            return_data=False,
        )
        assert isinstance(result, str)

    def test_element_and_string_inputs_agree(self):
        """Passing `Element` objects vs. strings should give the same barcode."""
        via_elements = call_molbar(
            elements=[Element("O"), Element("H"), Element("H")],
            coordinates=_WATER_COORDS,
            total_charge=0,
            mode=MolBarMode.MB,
            return_data=False,
        )
        via_strings = call_molbar(
            elements=["O", "H", "H"],
            coordinates=_WATER_COORDS,
            total_charge=0,
            mode=MolBarMode.MB,
            return_data=False,
        )
        assert via_elements == via_strings

    def test_array_and_list_coords_agree(self):
        """Passing a NumPy array vs. a nested list of coordinates should agree."""
        via_array = call_molbar(
            elements=["O", "H", "H"],
            coordinates=np.array(_WATER_COORDS),
            total_charge=0,
            mode=MolBarMode.MB,
            return_data=False,
        )
        via_list = call_molbar(
            elements=["O", "H", "H"],
            coordinates=_WATER_COORDS,
            total_charge=0,
            mode=MolBarMode.MB,
            return_data=False,
        )
        assert via_array == via_list


# ============================================================
# _validate_molbar_mode
# ============================================================


@pytest.mark.unit
class TestValidateMolbarMode:
    def test_valid_string_mb(self, water):
        """`_validate_molbar_mode()` should accept `"mb"` and return `MolBarMode.MB`."""
        assert water._validate_molbar_mode("mb") == MolBarMode.MB

    def test_valid_string_topo(self, water):
        """`_validate_molbar_mode()` should accept `"topo"` and return `MolBarMode.TOPO`."""
        assert water._validate_molbar_mode("topo") == MolBarMode.TOPO

    def test_valid_enum(self, water):
        """`_validate_molbar_mode()` should accept a `MolBarMode` instance directly."""
        assert water._validate_molbar_mode(MolBarMode.MB) == MolBarMode.MB

    def test_case_insensitive(self, water):
        """`_validate_molbar_mode()` should be case-insensitive."""
        assert water._validate_molbar_mode("MB") == MolBarMode.MB
        assert water._validate_molbar_mode("Topo") == MolBarMode.TOPO

    def test_invalid_mode_raises(self, water):
        """`_validate_molbar_mode()` should raise `ValueError` for an invalid mode."""
        with pytest.raises(ValueError, match="Invalid mode"):
            water._validate_molbar_mode("invalid")


# ============================================================
# _get_molbar_from_coordinates
# ============================================================


@pytest.mark.unit
class TestGetMolbarFromCoordinates:
    def test_raises_for_no_real_atoms(self, no_real_atoms_structure):
        """`_get_molbar_from_coordinates()` should raise `ValueError` if there are no real atoms."""
        with pytest.raises(ValueError, match="no real atoms"):
            no_real_atoms_structure._get_molbar_from_coordinates(MolBarMode.MB, return_data=False)

    def test_returns_string(self, water):
        """`_get_molbar_from_coordinates()` with `return_data=False` should return a string."""
        result = water._get_molbar_from_coordinates(MolBarMode.MB, return_data=False)
        assert isinstance(result, str)

    def test_returns_tuple_with_data(self, water):
        """`_get_molbar_from_coordinates()` with `return_data=True` should return a tuple."""
        result = water._get_molbar_from_coordinates(MolBarMode.MB, return_data=True)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert isinstance(result[1], dict)


# ============================================================
# calculate_molbar
# ============================================================


@pytest.mark.unit
class TestCalculateMolbar:
    def test_returns_string(self, water):
        """`calculate_molbar()` should return a string."""
        assert isinstance(water.calculate_molbar(), str)

    def test_known_barcode(self, water):
        """
        `calculate_molbar()` should return the expected barcode for water.
        The version field is checked against the installed MolBar version; the
        spectra are pinned from a verified run and are stable for this geometry.
        """
        barcode = water.calculate_molbar()
        assert barcode == (
            f"MolBar | {MOLBAR_VERSION} | OH2 | 0 | -84 20 344 | 80 | -47 12 315 | 0 "
        )

    def test_barcode_structure(self, water):
        """
        `calculate_molbar()` output should have the expected field structure and
        carry the installed MolBar version, independent of the numeric spectra.
        """
        fields = [f.strip() for f in water.calculate_molbar().split("|")]
        assert fields[0] == "MolBar"
        assert fields[1] == MOLBAR_VERSION
        assert fields[2] == "OH2"

    def test_topo_mode(self, water):
        """
        `calculate_molbar()` with `mode="topo"` should return the topology-only barcode.
        The version field is checked against the installed MolBar version.
        """
        assert water.calculate_molbar(mode="topo") == (
            f"TopoBar | {MOLBAR_VERSION} | OH2 | -84 20 344 | 80"
        )

    def test_mode_case_insensitive(self, water):
        """`calculate_molbar()` should accept mode strings case-insensitively."""
        assert water.calculate_molbar(mode="MB") == water.calculate_molbar(mode="mb")

    def test_raises_for_no_real_atoms(self, no_real_atoms_structure):
        """`calculate_molbar()` should raise `ValueError` if there are no real atoms."""
        with pytest.raises(ValueError, match="no real atoms"):
            no_real_atoms_structure.calculate_molbar()

    def test_raises_for_invalid_mode(self, water):
        """`calculate_molbar()` should raise `ValueError` for an invalid mode."""
        with pytest.raises(ValueError, match="Invalid mode"):
            water.calculate_molbar(mode="invalid")

    def test_ghost_atom_excluded(self):
        """
        A `GhostAtom` should not affect the barcode — result should be identical
        to the same structure without the ghost atom.
        """
        plain = Structure.from_xyz_block(
            "3\n\n"
            "O   0.000000   0.000000   0.119748\n"
            "H   0.000000   0.756950  -0.478993\n"
            "H   0.000000  -0.756950  -0.478993"
        )
        with_ghost = Structure(
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
                GhostAtom(
                    element=Element("C"), coordinates=Coordinates(coordinates=(5.0, 5.0, 5.0))
                ),
            ]
        )
        assert plain.calculate_molbar() == with_ghost.calculate_molbar()

    def test_point_charge_excluded(self):
        """
        A `PointCharge` should not affect the barcode — result should be identical
        to the same structure without the point charge.
        """
        plain = Structure.from_xyz_block(
            "3\n\n"
            "O   0.000000   0.000000   0.119748\n"
            "H   0.000000   0.756950  -0.478993\n"
            "H   0.000000  -0.756950  -0.478993"
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
        assert plain.calculate_molbar() == with_pc.calculate_molbar()


# ============================================================
# calculate_molbar_data
# ============================================================


@pytest.mark.unit
class TestCalculateMolbarData:
    def test_returns_tuple(self, water):
        """`calculate_molbar_data()` should return a tuple of length 2."""
        result = water.calculate_molbar_data()
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_first_element_is_string(self, water):
        """`calculate_molbar_data()` first element should be the barcode string."""
        barcode, _ = water.calculate_molbar_data()
        assert isinstance(barcode, str)

    def test_second_element_is_dict(self, water):
        """`calculate_molbar_data()` second element should be a dictionary."""
        _, data = water.calculate_molbar_data()
        assert isinstance(data, dict)

    def test_barcode_matches_calculate_molbar(self, water):
        """The barcode in `calculate_molbar_data()` should match `calculate_molbar()`."""
        barcode, _ = water.calculate_molbar_data()
        assert barcode == water.calculate_molbar()

    def test_data_keys(self, water):
        """
        `calculate_molbar_data()` data dictionary should contain the expected top-level keys.
        Keys verified against MolBar 1.1.3.
        """
        _, data = water.calculate_molbar_data()
        expected_keys = {
            "MolBar",
            "topology_spectrum",
            "heavy_atom_topology_spectrum",
            "topography_spectrum",
            "absolute_configuration_spectrum",
            "unified_coulomb_matrix",
            "final_energies",
            "timings",
            "elements",
            "atomic_numbers",
            "degrees",
            "priorities",
            "fragment_priorities",
            "vsepr_classes",
            "single_bonds",
            "double_bonds",
            "triple_bonds",
            "cycles",
            "fragment_data",
        }
        assert set(data.keys()) == expected_keys

    def test_raises_for_no_real_atoms(self, no_real_atoms_structure):
        """`calculate_molbar_data()` should raise `ValueError` if there are no real atoms."""
        with pytest.raises(ValueError, match="no real atoms"):
            no_real_atoms_structure.calculate_molbar_data()

    def test_raises_for_invalid_mode(self, water):
        """`calculate_molbar_data()` should raise `ValueError` for an invalid mode."""
        with pytest.raises(ValueError, match="Invalid mode"):
            water.calculate_molbar_data(mode="invalid")

    def test_topo_mode(self, water):
        """`calculate_molbar_data()` with `mode="topo"` should return the topology barcode."""
        barcode, _ = water.calculate_molbar_data(mode="topo")
        assert barcode == f"TopoBar | {MOLBAR_VERSION} | OH2 | -84 20 344 | 80"
