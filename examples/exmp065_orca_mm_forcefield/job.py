#!/usr/bin/env python3
"""
Example: Generate and manipulate ORCA force field files (`*.ORCAFF.prms`) with `orca_mm`.

A simple force field is generated for a solute (methanol) and a solvent (water) with
`orca_mm -makeff`, using GFN2-xTB partial charges. The water force field is repeated
three times (`-repeatff`) and merged with the solute force field (`-mergeff`), as done
when solvating a molecule. The merged force field is then split back into solute and
solvent (`-splitff`). Standard bond lengths to hydrogen, needed for link atoms in
QM/MM calculations, are generated for the solute (`-getHDist`).
"""

import shutil
from pathlib import Path

from opi.execution.orca_mm import OrcaMmRunner
from opi.input.structures import Structure


def run_exmp065(
    structure: Structure | None = None, working_dir: Path | None = Path("RUN")
) -> dict[str, Path | list[Path]]:
    # > recreate the working dir
    shutil.rmtree(working_dir, ignore_errors=True)
    working_dir.mkdir()

    # > if no structure is given read the solute structure from inp.xyz
    if structure is None:
        structure = Structure.from_xyz("inp.xyz")
    solvent = Structure.from_xyz(Path(__file__).parent / "water.xyz")

    # > `orca_mm` reads structures from files, so write them to the working dir
    (working_dir / "solute.xyz").write_text(structure.to_xyz_block())
    (working_dir / "water.xyz").write_text(solvent.to_xyz_block())

    # > `orca_mm` is executed inside `working_dir`, relative paths are resolved against it.
    # > Every `run_*` method raises `OrcaMmError` if `orca_mm` fails and returns the
    # > path(s) of the generated file(s).
    runner = OrcaMmRunner(working_dir=working_dir)

    # > Generate standard bond lengths to hydrogen for the solute (`orca_mm -getHDist`).
    # > This file can be modified and used to define link atoms in QM/MM calculations.
    # > This runs first, because `makeff` with a charge calculation deletes its input file.
    h_dist = runner.run_get_h_dist("solute.xyz")
    print(f"Hydrogen distances: {h_dist.name}")

    # > Create simple force fields with GFN2-xTB partial charges (`orca_mm -makeff`).
    # > Note: with a charge calculation, `makeff` deletes the input structure file.
    solute_ff = runner.run_makeff(
        "solute.xyz",
        charge=structure.charge,
        multiplicity=structure.multiplicity,
        charge_option="XTB",
    )
    water_ff = runner.run_makeff("water.xyz", charge=0, multiplicity=1, charge_option="XTB")
    print(f"Solute force field:  {solute_ff.name}")
    print(f"Solvent force field: {water_ff.name}")

    # > Repeat the solvent force field three times (`orca_mm -repeatff`).
    solvent_ff = runner.run_repeatff(water_ff, 3)
    print(f"Repeated solvent force field: {solvent_ff.name}")

    # > Merge solute and solvent into a single force field (`orca_mm -mergeff`).
    # > The order of the files defines the atom order of the merged force field.
    merged_ff = runner.run_mergeff(solute_ff, solvent_ff)
    print(f"Merged force field: {merged_ff.name}")

    # > Split the merged force field back into solute and solvent (`orca_mm -splitff`).
    # > The split point is the (1-based) index of the first atom of the new part.
    split_ffs = runner.run_splitff(merged_ff, len(structure) + 1)
    print(f"Split force fields: {', '.join(path.name for path in split_ffs)}")

    return {
        "solute_ff": solute_ff,
        "water_ff": water_ff,
        "solvent_ff": solvent_ff,
        "merged_ff": merged_ff,
        "split_ffs": split_ffs,
        "h_dist": h_dist,
    }


if __name__ == "__main__":
    run_exmp065()
