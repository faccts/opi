import pytest

from examples.exmp034_strucfile.job import run_exmp034


@pytest.mark.examples
@pytest.mark.orca
def test_exmp034_strucfile(tmp_path) -> None:
    """Ensure structure file example runs successfully and produces an energy."""
    output = run_exmp034(working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0
