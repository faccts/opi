import pytest

from examples.exmp043_dummy_atom.job import run_exmp043
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp043_dummy_atom(example_input_file, tmp_path) -> None:
    """Ensure dummy atom example runs successfully and produces an energy."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp043)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp043(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0
