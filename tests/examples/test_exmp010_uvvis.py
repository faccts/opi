import pytest

from examples.exmp010_uvvis.job import run_exmp010
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.json_files
def test_exmp010_uvvis(example_input_file, tmp_path, json_files_exporter) -> None:
    """Ensure TD-DFT example runs successfully and produces a final energy."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp010)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp010(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0

    # Plot the hole NTO of the dominant NTO pair of the first excited state, which is the
    # highest occupied NTO
    nelectrons, _ = output.get_nelectrons()
    nto = output.plot_nto(nelectrons // 2 - 1, state=1, resolution=20)

    # Assert that the cube file exists
    assert nto is not None
    assert nto.path.exists()

    # optional export of json files
    json_files_exporter.export_jsons_from(tmp_path)
