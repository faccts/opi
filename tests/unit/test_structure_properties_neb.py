import pytest

from opi.input.structures import Properties

"""
This module contains tests for reading `Properties` from the comment line of NEB XYZ files.
"""

# > Comment line of an ".allxyz" file, which is the only NEB XYZ file that carries the image number
ALLXYZ_BLOCK = """3
Coordinates from ORCA-job job_MEP NEB Path Image 1 E  -7.336370651022
O         -3.56626        1.77639        0.00000
H         -2.59626        1.77639        0.00000
H         -3.88959        1.36040       -0.81444
>
3
Coordinates from ORCA-job job_MEP NEB Path Image 2 E  -7.334880224742
O         -3.56626        1.77639        0.00000
H         -2.59626        1.77639        0.00000
H         -3.88959        1.36040       -0.81444
"""


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize(
    "comment, energy",
    [
        # > "<basename>_MEP_trj.xyz" and friends
        ("Coordinates from ORCA-job job_MEP E  -7.336370651022", -7.336370651022),
        # > A digit in the job name must not be mistaken for the energy
        ("Coordinates from ORCA-job neb_2_MEP E  -7.336370651022", -7.336370651022),
        # > The image number must not be mistaken for the energy
        ("Coordinates from ORCA-job job_MEP NEB Path Image 7 E  -7.336370651022", -7.336370651022),
    ],
)
def test_neb_energies(comment: str, energy: float):
    """Test that the energy is taken from behind the "E" token of a NEB comment line"""
    assert Properties.neb_energies(comment).energy_total == energy


@pytest.mark.unit
@pytest.mark.input
def test_neb_energies_without_energy():
    """Test that a comment line without an energy is rejected"""
    with pytest.raises(ValueError):
        Properties.neb_energies("Coordinates from ORCA-job job_MEP")


@pytest.mark.unit
@pytest.mark.input
def test_neb_from_trj_xyz_block_allxyz():
    """Test that all images of an ".allxyz" block are read with their image number"""
    properties = Properties.from_trj_xyz_block(ALLXYZ_BLOCK, mode="neb", comment_symbols=">")
    assert [prop.structure_id for prop in properties] == [1, 2]
    assert [prop.energy_total for prop in properties] == [-7.336370651022, -7.334880224742]
