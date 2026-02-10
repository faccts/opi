import pytest

from examples.exmp039_neb.job import run_exmp039


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.slow
def test_exmp039_neb(example_input_file, tmp_path) -> None:
    """Ensure NEB example runs successfully."""
    run_exmp039(working_dir=tmp_path)
