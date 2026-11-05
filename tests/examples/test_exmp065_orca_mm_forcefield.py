from pathlib import Path

import pytest

from examples.exmp065_orca_mm_forcefield.job import run_exmp065
from opi.input.structures import Structure


def _count_ff_atoms(orcaff_file: Path) -> int:
    """Return the number of atoms in the `$atoms` section of an ORCA forcefield file."""
    lines = orcaff_file.read_text().splitlines()
    return int(lines[lines.index("$atoms") + 1].split()[0])


@pytest.mark.examples
@pytest.mark.orca
def test_exmp065_orca_mm_forcefield(example_input_file, tmp_path) -> None:
    """Ensure the generated, repeated, merged and split forcefields contain the expected atoms."""
    input_file = example_input_file(run_exmp065)
    structure = Structure.from_xyz(input_file)
    n_solute = len(structure)
    n_solvent = 3 * 3

    files = run_exmp065(structure=structure, working_dir=tmp_path)

    assert files["h_dist"].is_file()
    assert _count_ff_atoms(files["solute_ff"]) == n_solute
    assert _count_ff_atoms(files["water_ff"]) == 3
    assert _count_ff_atoms(files["solvent_ff"]) == n_solvent
    assert _count_ff_atoms(files["merged_ff"]) == n_solute + n_solvent

    # > Splitting after the solute recovers solute and solvent
    solute_part, solvent_part = files["split_ffs"]
    assert _count_ff_atoms(solute_part) == n_solute
    assert _count_ff_atoms(solvent_part) == n_solvent
