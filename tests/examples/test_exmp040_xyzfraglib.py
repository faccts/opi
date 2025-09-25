import pytest

from examples.exmp040_xzyfraglib.job import run_exmp040


@pytest.mark.examples
@pytest.mark.orca
def test_exmp040_xyzfraglib(example_input_file, tmp_path) -> None:
    """Ensure fragment library example runs successfully."""
    run_exmp040(working_dir=tmp_path)
