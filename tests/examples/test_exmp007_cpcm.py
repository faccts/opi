import pytest

from examples.exmp007_cpcm.job import run_exmp007
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp007_cpcm(example_input_file, tmp_path) -> None:
    """Ensure CPCM example runs successfully and produces a final energy and solvent information."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp007)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp007(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0
    # Assert solvent information
    assert isinstance(output.results_properties.geometries[0].solvation_details.solvent, str)
    assert output.results_properties.geometries[0].solvation_details.epsilon > 0
    assert output.results_properties.geometries[0].solvation_details.npoints > 0
    assert output.results_properties.geometries[0].solvation_details.cpcmdielenergy < 0
