import pytest

from examples.exmp032_fragbasis.job import run_exmp032
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp032_fragbasis(example_input_file, tmp_path) -> None:
    """Ensure basis sets for fragments example runs successfully."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp032)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    run_exmp032(structure=structure, working_dir=tmp_path)
