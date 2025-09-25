import pytest

from examples.exmp037_s2.job import run_exmp037
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.slow
def test_exmp037_s2(example_input_file, tmp_path) -> None:
    """Ensure S² over scan example runs successfully and allows access to S² values."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp037)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp037(structure=structure, working_dir=tmp_path)

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
