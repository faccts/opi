import pytest

from examples.exmp003_opt.job import run_exmp003
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp003_opt(example_input_file, tmp_path) -> None:
    """Ensure optimization example runs successfully and produces a final energy and structure."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp003)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp003(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0
    # > Assert that a structure is available
    structure = output.get_structure()
    assert isinstance(structure, Structure), f"Expected Structure, got {type(structure).__name__}"
