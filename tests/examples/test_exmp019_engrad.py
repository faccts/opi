import pytest

from examples.exmp019_engrad.job import run_exmp019
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp019_engrad(example_input_file, tmp_path) -> None:
    """Ensure ENGRAD example runs successfully and produces an energy and a gradient."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp019)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp019(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0
    # Assert that the gradient is a list
    gradient = output.get_gradient()
    assert isinstance(gradient, list)
    # Assert that gradient contains floats
    assert all(isinstance(x, float) for x in gradient)
