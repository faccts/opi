#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.simple_keywords import AuxBasisSet, BasisSet, Scf, Wft
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp029(
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
        Scf.NOAUTOSTART, Wft.OO_RI_MP2, BasisSet.DEF2_QZVPP, AuxBasisSet.DEF2_QZVPP_C
    )
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

    ngeoms = len(output.results_properties.geometries)
    print("N GEOMETRIES")
    print(ngeoms)
    print("HF ENERGY")
    print(output.results_properties.geometries[0].energy[1].refenergy[0][0])
    print("CORRELATION ENERGY")
    print(output.results_properties.geometries[0].energy[1].correnergy[0][0])
    print("TOTAL ENERGY")
    print(output.results_properties.geometries[0].energy[1].totalenergy[0][0])

    return output
