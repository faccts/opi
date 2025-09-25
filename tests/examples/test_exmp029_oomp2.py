import pytest

from examples.exmp029_oomp2.job import run_exmp029
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp029_oomp2(example_input_file, tmp_path) -> None:
    """Ensure oo-mp2 example runs successfully and produces an energy."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp029)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp029(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0
    # Assert correlation energy
    assert output.get_energies()["MP2(OO)"]
