#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.simple_keywords import Dft, Scf, Task
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp037(
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
    calc.structure.multiplicity = 3
    calc.input.add_simple_keywords(Scf.NOAUTOSTART, Dft.R2SCAN_3C, Task.OPT)
    calc.input.ncores = 4

    calc.write_input()
    calc.run()

    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()

    # > Verify that SCF converged
    if not output.scf_converged():
        print(f"ORCA SCF failed to converge, see output file: {output.get_outfile()}")
        sys.exit(1)

    # > Verify that geometry optimization converged
    if not output.geometry_optimization_converged():
        print(
            f"ORCA geometry optimization failed to converge, see output file: {output.get_outfile()}"
        )
        sys.exit(1)

    ngeoms = len(output.results_properties.geometries)
    print("N GEOMETRIES")
    print(ngeoms)
    print("FINAL SINGLE POINT ENERGY")
    print(output.get_final_energy())
    print("SCF Energy along trajectory")
    # > Geometry index starts from 0 to *ngeom*
    for igeom in range(0, ngeoms):
        print(f"{igeom})", output.get_final_energy(index=igeom))
    print("S² expectation value along optimization (expec, ideal):")
    # > Geometry index starts from 0 to *ngeom*
    for igeom in range(0, ngeoms):
        print(f"{igeom})", output.get_s2(index=igeom))

    return output


if __name__ == "__main__":
    run_exmp037()
