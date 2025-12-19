from io import StringIO
from pathlib import Path

import numpy as np
import pytest

from opi.input.structures import Structure
from opi.utils.element import Element
from opi.utils.textio import TrackingTextIO


@pytest.fixture
def xyz_single_file(tmp_path: Path) -> Path:
    """Returns a test .xyz file."""
    xyz_file = tmp_path / "water.xyz"
    content = """3

O         -3.56626        1.77639        0.00000
H         -2.59626        1.77639        0.00000
H         -3.88959        1.36040       -0.81444"""
    xyz_file.write_text(content)
    return xyz_file


@pytest.fixture
def xyz_multi_file(tmp_path: Path) -> Path:
    """Returns a test .xyz file with multiple structures."""
    xyz_file = tmp_path / "methane.xyz"
    content = """8
Coordinates from ORCA-job job_MEP E  -7.336370651022
  C      -0.760629     -0.000001      0.000004
  C       0.760629      0.000001     -0.000004
  H      -1.143478      0.820497     -0.602830
  H      -1.143477     -0.932323     -0.409146
  H      -1.143466      0.111822      1.011998
  H       1.143466     -0.111824     -1.011998
  H       1.143477      0.932324      0.409145
  H       1.143478     -0.820496      0.602831
8
Coordinates from ORCA-job job_MEP E  -7.334880224742
  C      -0.761966     -0.000001      0.000005
  C       0.761966      0.000001     -0.000005
  H      -1.148621      0.923495     -0.423332
  H      -1.148621     -0.828372     -0.588093
  H      -1.148610     -0.095125      1.011448
  H       1.148611     -0.313659     -0.966278
  H       1.148618      0.993646      0.211490
  H       1.148623     -0.679984      0.754765"""

    xyz_file.write_text(content)
    return xyz_file


@pytest.fixture
def xyz_buffer_single_structure(xyz_single_file: Path):
    """Returns a test buffer of a single structure .xyz file"""
    with xyz_single_file.open("r") as f:
        tracking_text = TrackingTextIO(StringIO(f.read()))

    return tracking_text


def test_from_xyz_single_structure_created(xyz_single_file: Path):
    """Test to check if `Structure` object is created correctly from .xyz file"""
    structure = Structure.from_xyz(xyz_single_file)
    assert isinstance(structure, Structure)


def test_from_xyz_single_structure_correct_number_of_atoms(xyz_single_file: Path):
    """Test to check if Structure file created has the correct number of atoms"""
    structure = Structure.from_xyz(xyz_single_file)
    assert len(structure.atoms) == 3


def test_from_xyz_single_structure_correct_atoms(xyz_single_file: Path):
    """Test to check if order of atoms is preserved"""
    structure = Structure.from_xyz(xyz_single_file)
    structure_symbols = [atom.element for atom in structure.atoms]
    assert structure_symbols == [Element.O, Element.H, Element.H]


def test_from_xyz_single_structure_nonexistent_file(tmp_path: Path):
    """Test to check if `Structure.from_xyz()` correctly raises error in case of nonexistent file"""
    nonexistent_file = tmp_path / "nonexistent.xyz"
    with pytest.raises(FileNotFoundError):
        Structure.from_xyz(nonexistent_file)


def test_from_xyz_single_structure_check_coordinates(xyz_single_file: Path):
    """Test to check if Structure file created has the correct coordinates"""
    structure = Structure.from_xyz(xyz_single_file)
    assert np.allclose(
        structure.atoms[0].coordinates.coordinates,
        np.array([-3.56626, 1.77639, 0.00000]),
        atol=1e-5,
    )


def test_from_xyz_multi_structure_object_created(xyz_multi_file: Path):
    """Test to check if `Structure.from_xyz()` works correctly in case of multi structure .xyz file"""
    structure = Structure.from_xyz(xyz_multi_file)
    assert isinstance(structure, Structure)


def test_from_trj_xyz_structure_created(xyz_multi_file: Path):
    """Test to check if `Structure.from_trj_xyz()` correctly creates list of Structure objects"""
    structures = Structure.from_trj_xyz(xyz_multi_file)
    assert all(isinstance(structure, Structure) for structure in structures)


def test_from_trj_xyz_correct_number_of_structures(xyz_multi_file: Path):
    """Test to check if correct number of structures are created"""
    structures = Structure.from_trj_xyz(xyz_multi_file)
    assert len(structures) == 2


def test_from_trj_xyz_struc_limit(xyz_multi_file: Path):
    """Test to check if `struc_limit` parameter is enforced correctly"""
    structures = Structure.from_trj_xyz(xyz_multi_file, struc_limit=1)
    assert len(structures) == 1


def test_from_trj_xyz_nonexistent_file(tmp_path: Path):
    """Test to check if `Structure.from_trj_xyz()` correctly raises error in case of nonexistent file"""
    nonexistent_file = tmp_path / "nonexistent.xyz"
    with pytest.raises(FileNotFoundError):
        Structure.from_trj_xyz(nonexistent_file)


def test_from_xyz_buffer(xyz_buffer_single_structure):
    """Test to check if `Structure` object is created from xyz buffer"""
    structure = Structure.from_xyz_buffer(xyz_buffer_single_structure)
    assert isinstance(structure, Structure)


def test_from_xyz_buffer_empty():
    """Test to check if `Structure.from_xyz_buffer()` returns None in case of empty buffer."""
    structure = Structure.from_xyz_buffer(TrackingTextIO(StringIO("")))
    assert not structure


def test_from_xyz_buffer_raises_on_invalid_header():
    """Text to check if `Structure.from_xyz_buffer()` raises error on invalid header"""
    xyz_text = """NotAnInteger
Comment line
O 0.0 0.0 0.0
"""
    buffer = TrackingTextIO(StringIO(xyz_text))
    with pytest.raises(ValueError):
        Structure.from_xyz_buffer(buffer)
