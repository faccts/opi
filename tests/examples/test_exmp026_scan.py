import pytest

from examples.exmp026_scan.job import run_exmp026
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.slow
def test_exmp026_scan(example_input_file, tmp_path) -> None:
    """Ensure scan example runs successfully and produces an energy."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp026)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp026(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0
