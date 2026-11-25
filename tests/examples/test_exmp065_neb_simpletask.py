import pytest

from examples.exmp065_neb_simpletask.job import run_exmp065


@pytest.mark.examples
@pytest.mark.orca
def test_exmp065_neb_simpletask(tmp_path) -> None:
    """Ensure the NEB simple task finds the rotation barrier of ethane."""
    results = run_exmp065(working_dir=tmp_path)

    assert results.status
    structures, energies = results.primary_property
    assert len(structures) == len(energies) == 10
    # > The highest image lies between the endpoints and above both
    assert 0 < results.highest_image_index < len(energies) - 1
    assert results.highest_energy > max(energies[0], energies[-1])
