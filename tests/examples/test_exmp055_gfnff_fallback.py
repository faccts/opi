import pytest

from examples.exmp055_gfnff_fallback.job import run_exmp055
from opi.input.structures import Structure


@pytest.mark.examples
@pytest.mark.orca
def test_exmp055_gfnff_fallback(example_input_file, tmp_path) -> None:
    """Ensure GFN-FF optimisation example runs and fallback parsing recovers energy and structure."""
    input_file = example_input_file(run_exmp055)
    structure = Structure.from_xyz(input_file)

    output = run_exmp055(structure=structure, working_dir=tmp_path)

    # > GFN-FF writes a property JSON but with no geometry entries, so the
    # > normal JSON path returns nothing and the .out fallback must be used
    assert not output.results_properties.geometries

    energy = output.get_final_energy()
    assert isinstance(energy, float)
    assert energy < 0

    optimized = output.get_structure()
    assert isinstance(optimized, Structure)
    assert len(optimized.atoms) == 3

    gradient = output.get_gradient(index=-2)
    assert isinstance(gradient, list)
    assert len(gradient) == 9  # 3 atoms * 3 components
