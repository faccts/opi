import pytest

from examples.exmp013_bs.job import run_exmp013
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp013_bs(example_input_file, tmp_path) -> None:
    """Ensure broken symmetry example runs successfully and produces a final energy."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp013)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp013(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0

    # Assert S² data
    result_s2 = output.get_s2()
    # It is a tuple
    assert isinstance(result_s2, tuple)
    # of length 2
    assert len(result_s2) == 2
    # containing floats
    assert all(isinstance(x, float) for x in result_s2)
    # Ideal value is (for SCF methods) always equal or smaller than calculated
    assert result_s2[0] >= result_s2[1]
