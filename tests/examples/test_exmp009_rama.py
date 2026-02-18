import pytest

from examples.exmp009_rama.job import run_exmp009
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.json_files
def test_exmp009_rama(example_input_file, tmp_path, json_files_exporter) -> None:
    """Ensure Raman example runs successfully and produces a final energy."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp009)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp009(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0

    # optional export of json files
    json_files_exporter.export_jsons_from(tmp_path)
