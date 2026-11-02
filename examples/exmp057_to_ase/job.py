#!/usr/bin/env python3
"""
Example: hand an ORCA-optimised structure over to ASE.
"""

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.simple_keywords import BasisSet, Method, Task
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp057(working_dir: Path | None = Path("RUN")) -> Output:
    # > Water radical cation with a slightly distorted start geometry.
    # > Positions in Ångström, charge +1 and a doublet ground state.
    structure = Structure.from_xyz_block(
        "3\n\n"
        "O   0.000000   0.000000   0.000000\n"
        "H   0.000000   0.000000   1.020000\n"
        "H   0.960000   0.000000  -0.200000\n",
        charge=1,
        multiplicity=2,
    )

    shutil.rmtree(working_dir, ignore_errors=True)
    working_dir.mkdir()

    calc = Calculator(basename="job", working_dir=working_dir)
    calc.structure = structure
    calc.input.add_simple_keywords(Method.HF, BasisSet.DEF2_SVP, Task.OPT)

    calc.write_input()
    calc.run()

    output = calc.get_output()
    if not output.terminated_normally() and output.geometry_optimization_converged():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        print(output.error_message())
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()

    print("FINAL SINGLE POINT ENERGY")
    print(output.get_final_energy())

    # > Optimised structure, including charge and multiplicity from the output
    optimized = output.get_structure()
    if optimized is None:
        print("No structure available in the output")
        sys.exit(1)
    # << END OF IF

    print("OPTIMIZED STRUCTURE")
    print(optimized.to_xyz_block())

    # > Convert the OPI structure into an ASE Atoms object
    ase_atoms = optimized.to_ase()
    print("ASE ATOMS OBJECT")
    print(ase_atoms)

    # > Charge and multiplicity are carried in Atoms.info, not in the per-atom
    # > initial_charges / initial_magnetic_moments arrays.
    print(f"Charge from Atoms.info: {ase_atoms.info['charge']}")
    print(f"Multiplicity from Atoms.info: {ase_atoms.info['spin']}")

    # > Everything below is computed by ASE itself
    print(f"Chemical formula: {ase_atoms.get_chemical_formula()}")
    d_oh1 = ase_atoms.get_distance(0, 1)
    d_oh2 = ase_atoms.get_distance(0, 2)
    print(f"O-H bond lengths [Angstrom]: {d_oh1:.4f} {d_oh2:.4f}")
    print(f"H-O-H angle [degree]: {ase_atoms.get_angle(1, 0, 2):.2f}")
    print(f"Center of mass [Angstrom]: {ase_atoms.get_center_of_mass()}")

    # > Round trip back into OPI
    round_trip = Structure.from_ase(ase_atoms)
    print("STRUCTURE AFTER ROUND TRIP THROUGH ASE")
    print(round_trip.to_xyz_block())
    print(f"Charge after round trip: {round_trip.charge}")
    print(f"Multiplicity after round trip: {round_trip.multiplicity}")

    return output


if __name__ == "__main__":
    run_exmp057()
