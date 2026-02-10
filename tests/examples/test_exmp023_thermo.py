import pytest

from examples.exmp023_thermo.job import run_exmp023
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp023_thermo(example_input_file, tmp_path) -> None:
    """Ensure thermo block example runs successfully and produces a free energy."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp023)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp023(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0
    # Assert finite temperature for thermostatistical corrections
    assert output.results_properties.geometries[0].thermochemistry_energies[0].temperature > 0
