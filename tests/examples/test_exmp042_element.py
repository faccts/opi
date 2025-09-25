import pytest

from examples.exmp042_element.job import run_exmp042
from opi.input.structures import Structure


@pytest.mark.examples
def test_exmp042_element(example_input_file, tmp_path) -> None:
    """Ensure element example runs successfully."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp042)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    run_exmp042(structure=structure, working_dir=tmp_path)
