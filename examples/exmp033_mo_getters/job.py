#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.simple_keywords import BasisSet, Dft, Scf, Task
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp033(
    structure: Structure | None = None, working_dir: Path | None = Path("RUN")
) -> Output:
    # > recreate the working dir
    shutil.rmtree(working_dir, ignore_errors=True)
    working_dir.mkdir()

    # > if no structure is given read structure from inp.xyz
    if structure is None:
        structure = Structure.from_xyz("inp.xyz")

    calc = Calculator(basename="job", working_dir=working_dir)
    calc.structure = structure
    calc.structure.charge = 1
    calc.structure.multiplicity = 2
    calc.input.add_simple_keywords(
        Scf.NOAUTOSTART,
        Dft.PBE0,
        BasisSet.DEF2_SVP,
        Task.SP,
    )

    calc.write_input()
    calc.run()

    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()

    # check for convergence of the SCF
    if output.results_properties.geometries[0].single_point_data.converged:
        print("SCF CONVERGED")
    else:
        print("SCF DID NOT CONVERGE")
        sys.exit(1)

    print(output.get_hftype())
    print(output.get_nelectrons())
    output.get_mos()
    homo_data = output.get_homo()
    lumo_data = output.get_lumo()
    print(f"HOMO {homo_data.index}({homo_data.channel}) energy: {homo_data.orbitalenergy:.8f} Eh")
    print(f"LUMO {lumo_data.index}({lumo_data.channel}) energy: {lumo_data.orbitalenergy:.8f} Eh")
    print(f"HOMO-LUMO gap: {output.get_hl_gap():.2f} eV")

    return output


if __name__ == "__main__":
    run_exmp033()
