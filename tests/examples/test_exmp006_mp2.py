import pytest

from examples.exmp006_mp2.job import run_exmp006
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp006_mp2(example_input_file, tmp_path) -> None:
    """Ensure MP2 example runs successfully and produces a final energy and correlation energy."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp006)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp006(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0
    # Assert MP2 correlation energy
    assert output.get_energies()["MP2"].correnergy[0][0] < 0
