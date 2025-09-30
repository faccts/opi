import pytest

from examples.exmp047_trj.job import run_exmp047
from opi.output.core import Output


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.slow
def test_exmp047_trj() -> None:
    """Ensure that OPI can read multi-xyz (trj) files and run single-point energy calculations on all structures."""
    output_list = run_exmp047()

    # Assert that 10 outputs are present
    assert len(output_list) == 10
    assert all(isinstance(x, Output) for x in output_list)
