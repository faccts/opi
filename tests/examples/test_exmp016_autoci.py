import pytest

from examples.exmp016_autoci.job import run_exmp016
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.slow
def test_exmp016_autoci(example_input_file, tmp_path) -> None:
    """Ensure AUTOCI analysis example runs successfully and produces a final energy."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp016)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp016(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0
