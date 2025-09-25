import pytest

from examples.exmp036_solvator.job import run_exmp036
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.slow
def test_exmp036_solvator(example_input_file, tmp_path) -> None:
    """Ensure solvator example runs."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp036)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    run_exmp036(structure=structure, working_dir=tmp_path)
