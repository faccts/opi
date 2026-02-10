import pytest

from examples.exmp017_roci.job import run_exmp017
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp017_roci(example_input_file, tmp_path) -> None:
    """Ensure ROCIS analysis example runs successfully and produces a final energy."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp017)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp017(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0
