import pytest

from examples.exmp018_cipsi.job import run_exmp018
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp018_cipsi(example_input_file, tmp_path) -> None:
    """Ensure ICE-CI example runs successfully."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp018)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    run_exmp018(structure=structure, working_dir=tmp_path)
