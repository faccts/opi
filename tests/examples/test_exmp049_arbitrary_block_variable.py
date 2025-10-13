import pytest

from examples.exmp049_arbitrary_block_variable.job import run_exmp049
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp048_loc_gbw(example_input_file, tmp_path) -> None:
    """Test ORCA job with arbitrary block variable."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp049)
    structure = Structure.from_xyz(input_file)

    output = run_exmp049(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0
