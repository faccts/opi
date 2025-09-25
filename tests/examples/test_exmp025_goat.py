import pytest

from examples.exmp025_goat.job import run_exmp025
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.slow
def test_exmp025_goat(example_input_file, tmp_path) -> None:
    """Ensure GOAT example runs successfully."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp025)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    run_exmp025(structure=structure, working_dir=tmp_path)
