import numpy as np
import pytest

from examples.exmp054_casscf_fcidump.job import run_exmp054
from opi.input.structures import Structure


def _naive_eri(two_electron: dict, norb: int) -> np.ndarray:
    """Independent, unvectorized reference implementation for differential testing."""
    tensor = np.zeros((norb,) * 4)
    for (i, j, k, ll), val in two_electron.items():
        a, b, c, d = i - 1, j - 1, k - 1, ll - 1
        for p, q, r, s in [
            (a, b, c, d),
            (b, a, c, d),
            (a, b, d, c),
            (b, a, d, c),
            (c, d, a, b),
            (d, c, a, b),
            (c, d, b, a),
            (d, c, b, a),
        ]:
            tensor[p, q, r, s] = val
    return tensor


@pytest.mark.examples
@pytest.mark.orca
def test_exmp054_casscf_fcidump(example_input_file, tmp_path) -> None:
    """Test the FCIDUMP export from a CASSCF calculation."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp054)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp054(structure=structure, working_dir=tmp_path)

    fcidump = output.get_fcidump()
    assert fcidump is not None

    fcidump_file = fcidump.path
    assert fcidump_file.exists() and fcidump_file.is_file()

    norb = fcidump.norb
    assert fcidump.hcore_matrix.shape == (norb, norb)
    assert fcidump.eri_tensor.shape == (norb, norb, norb, norb)

    # hcore must be symmetric
    assert np.allclose(fcidump.hcore_matrix, fcidump.hcore_matrix.T)

    # differential test: vectorized eri_tensor must match an independently
    # written, unvectorized reference implementation on this same real data;
    # catches an all-zero or misplaced tensor at every symmetry-equivalent position
    assert np.allclose(fcidump.eri_tensor, _naive_eri(fcidump.two_electron, norb))
