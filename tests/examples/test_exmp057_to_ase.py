# ruff: noqa: E402
import pytest

# > example57 requires ase, which is not installed by default
# > skip test if ase is not available
pytest.importorskip("ase", reason="requires ase")
from ase import Atoms

from examples.exmp057_to_ase.job import run_exmp057


@pytest.mark.ase
@pytest.mark.examples
@pytest.mark.orca
def test_exmp057_to_ase(tmp_path) -> None:
    """Ensure the to_ase example runs and yields an ASE Atoms object carrying charge info."""
    output = run_exmp057(working_dir=tmp_path)

    structure = output.get_structure()
    assert structure is not None
    ase_atoms = structure.to_ase()
    assert isinstance(ase_atoms, Atoms)
    assert ase_atoms.get_chemical_symbols() == ["O", "H", "H"]
    assert ase_atoms.info["charge"] == 1
    assert ase_atoms.info["spin"] == 2
