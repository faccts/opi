import numpy as np
import pytest

from examples.exmp048_loc_gbw.job import run_exmp048
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp048_loc_gbw(example_input_file, tmp_path) -> None:
    """Test localizing orbitals and transforming them into (L)MO basis."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp048)
    structure = Structure.from_xyz(input_file)

    run_exmp048(structure=structure, working_dir=tmp_path)

    # Assert that integral files are on disk

    # > Overlap in MO basis
    assert (tmp_path / "smo.txt").is_file()
    # > Size larger zero
    assert np.loadtxt(tmp_path / "smo.txt").size > 0

    # > Fock matrix in AO basis
    assert (tmp_path / "fao.txt").is_file()
    # > Size larger zero
    assert np.loadtxt(tmp_path / "fao.txt").size > 0

    # > Fock matrix in MO basis
    assert (tmp_path / "fmo.txt").is_file()
    # > Size larger zero
    assert np.loadtxt(tmp_path / "fmo.txt").size > 0

    # > Fock matrix in LMO basis
    assert (tmp_path / "flmo.txt").is_file()
    # > Size larger zero
    assert np.loadtxt(tmp_path / "flmo.txt").size > 0
