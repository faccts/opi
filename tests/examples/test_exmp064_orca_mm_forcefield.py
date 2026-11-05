from pathlib import Path

import pytest

from examples.exmp064_orca_mm_forcefield.job import run_exmp064
from opi.input.structures import Structure


def _count_ff_atoms(orcaff_file: Path) -> int:
    """Return the number of atoms in the `$atoms` section of an ORCA forcefield file."""
    lines = orcaff_file.read_text().splitlines()
    return int(lines[lines.index("$atoms") + 1].split()[0])


@pytest.mark.examples
@pytest.mark.orca
def test_exmp064_orca_mm_forcefield(example_input_file, tmp_path) -> None:
    """Ensure the forcefield files are generated and the QM/MM calculation uses the merged one."""
    input_file = example_input_file(run_exmp064)
    structure = Structure.from_xyz(input_file)
    n_solute = len(structure)
    n_solvent = 3 * 3

    output = run_exmp064(structure=structure, working_dir=tmp_path)

    # > Forcefield files contain the expected number of atoms
    assert (tmp_path / "solute.H_DIST.prms").is_file()
    assert _count_ff_atoms(tmp_path / "solute.ORCAFF.prms") == n_solute
    assert _count_ff_atoms(tmp_path / "water.ORCAFF.prms") == 3
    assert _count_ff_atoms(tmp_path / "water_repeat3.ORCAFF.prms") == n_solvent
    assert _count_ff_atoms(tmp_path / "solute_merged.ORCAFF.prms") == n_solute + n_solvent

    # > Splitting after the solute recovers solute and solvent
    assert _count_ff_atoms(tmp_path / "solute_merged_split1.ORCAFF.prms") == n_solute
    assert _count_ff_atoms(tmp_path / "solute_merged_split2.ORCAFF.prms") == n_solvent

    # > The QM/MM calculation ran with the solute as QM region
    assert output.terminated_normally()
    assert output.get_final_energy() < 0
    assert len(output.get_structure()) == n_solute
