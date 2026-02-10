import pytest

from examples.exmp027_constraints.job import run_exmp027
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp027_scan(example_input_file, tmp_path) -> None:
    """Ensure constraint example runs successfully."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp027)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    run_exmp027(structure=structure, working_dir=tmp_path)
