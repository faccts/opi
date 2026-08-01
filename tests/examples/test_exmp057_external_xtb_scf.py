import pytest

from examples.exmp057_external_xtb_scf.job import run_exmp057
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp057_external_xtb_scf(example_input_file, tmp_path) -> None:
    """Ensure external xTB calculation example runs and scf_converged detects convergence."""
    input_file = example_input_file(run_exmp057)
    structure = Structure.from_xyz(input_file)

    output = run_exmp057(structure=structure, working_dir=tmp_path)
    assert output.scf_converged() is True
