import pytest

from examples.exmp058_write_gbw.job import run_exmp058
from opi.input.structures import Structure
from opi.output.core import Output


@pytest.mark.examples
@pytest.mark.orca
def test_exmp058_write_gbw(example_input_file, tmp_path) -> None:
    """Ensure the gbw file written from the parsed data is accepted by ORCA as SCF guess."""
    input_file = example_input_file(run_exmp058)
    structure = Structure.from_xyz(input_file)

    output = run_exmp058(structure=structure, working_dir=tmp_path)

    # Assert the gbw file was written from the parsed data
    gbw_file = tmp_path / "from_results.gbw"
    assert gbw_file.is_file()
    assert gbw_file.stat().st_size > 0

    # Assert ORCA took the initial guess from that file
    assert "INITIAL GUESS: MOREAD" in output.get_outfile().read_text()

    # Assert the guess leads to the energy of the calculation the gbw file was written from
    reference = Output("job", working_dir=tmp_path, parse=True)
    assert output.get_final_energy() < 0
    assert output.get_final_energy() == pytest.approx(reference.get_final_energy(), abs=1e-6)
