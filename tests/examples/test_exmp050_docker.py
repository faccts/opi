import pytest

from examples.exmp049_docker.job import run_exmp049
from opi.input.structures import Properties, Structure


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.slow
def test_exmp049_docker(example_input_file, tmp_path) -> None:
    """Run a docker calculation and gather the resulting structures."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp049)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    structures, properties_list = run_exmp049(structure=structure, working_dir=tmp_path)

    # Assert that docker structures are present
    assert len(structures) >= 10
    assert all(isinstance(x, Structure) for x in structures)
    assert all(isinstance(x, Properties) for x in properties_list)
