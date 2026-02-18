import pytest

from examples.exmp012_nmr.job import run_exmp012
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.json_files
def test_exmp012_nmr(example_input_file, tmp_path, json_files_exporter) -> None:
    """Ensure NMR example runs successfully and produces a final energy."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp012)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp012(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0

    # optional export of json files
    json_files_exporter.export_jsons_from(tmp_path)
