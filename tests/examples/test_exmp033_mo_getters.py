import pytest

from examples.exmp033_mo_getters.job import run_exmp033
from opi.input.structures import Structure
from opi.output.models.json.gbw.properties.mo import MO


@pytest.mark.examples
@pytest.mark.orca
def test_exmp033_mo_getters(example_input_file, tmp_path) -> None:
    """Ensure MO getters example runs successfully and generates MOs."""
    # Get input file from example folder
    input_file = example_input_file(run_exmp033)
    structure = Structure.from_xyz(input_file)

    # Run the example in tmp_path
    output = run_exmp033(structure=structure, working_dir=tmp_path)

    # Assert MOs
    mos = output.get_mos()
    assert isinstance(mos, dict)
    # Assert all keys are strings
    assert all(isinstance(k, str) for k in mos.keys())
    # Assert all values are list[MO]
    assert all(isinstance(v, list) and all(isinstance(x, MO) for x in v) for v in mos.values())
    # Assert HOMO-LUMO gap
    assert isinstance(output.get_hl_gap(), float)
