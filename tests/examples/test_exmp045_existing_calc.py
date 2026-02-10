import pytest

from examples.exmp045_existing_calc.job import run_exmp045


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.slow
def test_exmp045_existing_calc() -> None:
    """Ensure OPI can obtain energy from an existing calculation."""
    output = run_exmp045()

    # Assert negative final energy
    assert output.get_final_energy() < 0
