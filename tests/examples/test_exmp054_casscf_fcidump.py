import pytest

from examples.exmp054_casscf_fcidump.job import run_exmp054
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp054_casscf_fcidump(example_input_file, tmp_path) -> None:
    """Test the FCIDUMP export from a CASSCF calculation."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp054)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp054(structure=structure, working_dir=tmp_path)

    fcidump_file = output.get_outfile().with_suffix(".fcidump")

    assert fcidump_file.exists() and fcidump_file.is_file()
