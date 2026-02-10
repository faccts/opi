import pytest

from examples.exmp011_epr.job import run_exmp011
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp011_epr(example_input_file, tmp_path) -> None:
    """Ensure EPR example runs successfully and produces a final energy."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp011)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp011(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0
