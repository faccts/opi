#!/usr/bin/env python3
"""
Example: Generate ORCA force field files (`*.ORCAFF.prms`) with `orca_mm` and run a QM/MM
calculation.

A simple force field is generated for a solute (methanol) and a solvent (water) with
`orca_mm -makeff`, using GFN2-xTB partial charges. The water force field is repeated
three times (`-repeatff`) and merged with the solute force field (`-mergeff`), as done
when solvating a molecule. Standard bond lengths to hydrogen, needed for link atoms in
QM/MM calculations, are generated for the solute (`-getHDist`), and the merged force
field is split back into solute and solvent (`-splitff`) to demonstrate the reverse step.

Finally, a QM/MM single point is run on the solvated system with the merged force field:
methanol is treated with HF/def2-SVP, the water molecules with the force field.
"""

import copy
import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.execution.orca_mm import OrcaMmRunner
from opi.input.blocks import BlockQmmm
from opi.input.simple_keywords import BasisSet, Method, Qmmm
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp064(
    structure: Structure | None = None, working_dir: Path | None = Path("RUN")
) -> Output:
    # > recreate the working dir
    shutil.rmtree(working_dir, ignore_errors=True)
    working_dir.mkdir()

    # > if no structure is given read the solute structure from inp.xyz
    if structure is None:
        structure = Structure.from_xyz("inp.xyz")
    water = Structure.from_xyz(Path(__file__).parent / "water.xyz")

    # > `orca_mm` reads structures from files, so write them to the working dir
    (working_dir / "solute.xyz").write_text(structure.to_xyz_block())
    (working_dir / "water.xyz").write_text(water.to_xyz_block())

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
    n_waters = 3
    solvent_ff = runner.run_repeatff(water_ff, n_waters)
    print(f"Repeated solvent force field: {solvent_ff.name}")

    # > Merge solute and solvent into a single force field (`orca_mm -mergeff`).
    # > The order of the files defines the atom order of the merged force field.
    merged_ff = runner.run_mergeff(solute_ff, solvent_ff)
    print(f"Merged force field: {merged_ff.name}")

    # > Split the merged force field back into solute and solvent (`orca_mm -splitff`).
    # > The split point is the (1-based) index of the first atom of the new part.
    split_ffs = runner.run_splitff(merged_ff, len(structure) + 1)
    print(f"Split force fields: {', '.join(path.name for path in split_ffs)}")

    # > Build the solvated system with the same atom order as the merged force field:
    # > the solute followed by the water molecules, each shifted by 3 Angstrom.
    solvated = structure
    for shift in ((3.0, 0.0, 0.0), (-3.0, 0.0, 0.0), (0.0, 0.0, 3.0))[:n_waters]:
        water_copy = copy.deepcopy(water)
        water_copy.set_coordinates(water_copy.get_coordinates() + shift)
        solvated = Structure.combine_molecules(solvated, water_copy)

    # > Run a QM/MM single point with the merged force field.
    # > The solute (0-based atom indices) forms the QM region, the water molecules the MM region.
    calc = Calculator(basename="job", working_dir=working_dir)
    calc.structure = solvated
    calc.input.add_simple_keywords(Qmmm.QMMM, Method.HF, BasisSet.DEF2_SVP)
    calc.input.add_blocks(
        BlockQmmm(qmatoms=list(range(len(structure))), orcafffilename=merged_ff.name)
    )

    calc.write_input()
    calc.run()

    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        print(output.error_message())
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()

    # > The final energy is the total QM/MM energy.
    # > The structure in the output only contains the QM region.
    print("FINAL QM/MM ENERGY")
    print(output.get_final_energy())
    print("QM REGION")
    print(output.get_structure().to_xyz_block())

    return output


if __name__ == "__main__":
    run_exmp064()
