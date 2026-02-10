import pytest

from examples.exmp005_dft.job import run_exmp005
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp005_dft(example_input_file, tmp_path) -> None:
    """Ensure DFT example runs successfully and produces a final energy."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp005)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp005(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0
