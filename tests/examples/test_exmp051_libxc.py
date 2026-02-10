import pytest

from examples.exmp051_libxc.job import run_exmp051
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.slow
def test_exmp051_libxc(example_input_file, tmp_path) -> None:
    """Run a DFT calculation and verify successful calculation"""
    # Get input file from example folder
    input_file = example_input_file(run_exmp051)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output_object = run_exmp051(structure=structure, working_dir=tmp_path)

    assert output_object
