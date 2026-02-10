import pytest

from examples.exmp041_graph.job import run_exmp041
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp041_graph(example_input_file, tmp_path, capsys) -> None:
    """Ensure graph example runs successfully and prints something."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp041)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    run_exmp041(structure=structure, working_dir=tmp_path)

    # Assert that the graph was printed by checking that more than 20 lines were printed
    captured = capsys.readouterr()
    assert len(captured.out.splitlines()) > 20
