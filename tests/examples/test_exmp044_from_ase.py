# ruff: noqa: E402
import pytest

# > example44 requires ase, which is not installed by default
# > skip test if ase is not available
pytest.importorskip("ase", reason="requires ase")
from examples.exmp044_from_ase.job import run_exmp044


@pytest.mark.ase
@pytest.mark.examples
@pytest.mark.orca
def test_exmp044_from_ase(example_input_file, tmp_path) -> None:
    """Ensure from_ase example runs successfully and produces an energy."""
    # Run the example in tmp_path
    output = run_exmp044(working_dir=tmp_path)

    # Assert negative final energy
    assert output.get_final_energy() < 0
