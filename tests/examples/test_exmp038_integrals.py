import numpy as np
import pytest

from examples.exmp038_integrals.job import run_exmp038
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp038_integrals(example_input_file, tmp_path) -> None:
    """Ensure integral example runs successfully and allows access to integrals."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp038)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp038(structure=structure, working_dir=tmp_path)

    # Assert that integrals can be obtained

    # overlap
    overlap = output.get_int_overlap(recreate_json=True)
    assert isinstance(overlap, np.ndarray)
    assert overlap.dtype == np.float64
    assert overlap.ndim == 2

    # hcore
    hcore = output.get_int_hcore(recreate_json=True)
    assert isinstance(hcore, np.ndarray)
    assert hcore.dtype == np.float64
    assert hcore.ndim == 2

    # f (although it rather is g)
    f = output.get_int_f(recreate_json=True)
    assert isinstance(f, np.ndarray)
    assert f.dtype == np.float64
    assert f.ndim == 2

    # j
    j = output.get_int_j(recreate_json=True)
    assert isinstance(j, np.ndarray)
    assert j.dtype == np.float64
    assert j.ndim == 2

    # k
    k = output.get_int_k(recreate_json=True)
    assert isinstance(k, np.ndarray)
    assert k.dtype == np.float64
    assert k.ndim == 2
