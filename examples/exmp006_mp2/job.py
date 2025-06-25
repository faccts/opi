#!/usr/bin/env python3

import shutil
from pathlib import Path
import sys

from opi.core import Calculator
from opi.input.simple_keywords import BasisSet, Scf, Wft
from opi.input.structures import Structure

if __name__ == "__main__":
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_xyz("inp.xyz")
    calc.input.add_simple_keywords(
        Scf.NOAUTOSTART,
        Wft.MP2,
        BasisSet.DEF2_QZVPP,
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
