#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.simple_keywords import BasisSet, Method, Scf, Task
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp038(
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
    calc.input.add_simple_keywords(
        Scf.NOAUTOSTART,
        Method.HF,
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

    print("Printing overlap integrals")
    print(output.get_int_overlap(recreate_json=True))
    print("Printing Hcore integrals")
    print(output.get_int_hcore(recreate_json=True))
    print("Printing F two-electron integrals")
    print(output.get_int_f(recreate_json=True))
    print("Printing Coulomb matrix J")
    print(output.get_int_j(recreate_json=True))
    print("Printing Exchange matrix K")
    print(output.get_int_k(recreate_json=True))

    return output


if __name__ == "__main__":
    run_exmp038()
