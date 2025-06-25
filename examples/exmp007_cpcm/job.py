#!/usr/bin/env python3

import sys
import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.simple_keywords import BasisSet, Dft, Scf, SolvationModel, Solvent
from opi.input.structures import Structure

if __name__ == "__main__":
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_xyz("inp.xyz")
    calc.input.add_simple_keywords(
        Scf.NOAUTOSTART, Dft.BP86, BasisSet.DEF2_SVP, SolvationModel.CPCM(Solvent.WATER)
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

    ngeoms = len(output.results_properties.geometries)
    print("N GEOMETRIES")
    print(ngeoms)
    print("DFT ENERGY")
    print(output.results_properties.geometries[0].dft_energy.finalen)
    print("Solvent")
    print(output.results_properties.geometries[0].solvation_details.solvent)
    print("Epsilon")
    print(output.results_properties.geometries[0].solvation_details.epsilon)
    print("Surface points")
    print(output.results_properties.geometries[0].solvation_details.npoints)
    print("CPCM ENERGY")
    print(output.results_properties.geometries[0].solvation_details.cpcmdielenergy)
