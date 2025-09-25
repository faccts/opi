import pytest

from examples.exmp002_scf_ccsdt.job import run_exmp002
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp002_scf(example_input_file, tmp_path) -> None:
    """Ensure CCSD(T) example runs successfully and produces a final energy."""

    # Get input file from example folder
    input_file = example_input_file(run_exmp002)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp002(structure=structure, working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0
    # Assert correlation energy
    assert output.get_energies()["MDCI(SD(T))"].correnergy[0][0] < 0
