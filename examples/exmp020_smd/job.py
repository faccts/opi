#!/usr/bin/env python3

import sys
import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockCpcm, Radius
from opi.input.simple_keywords import Dft, Scf, SolvationModel, Solvent
from opi.input.structures import Structure

if __name__ == "__main__":
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    """
    Run a r²SCAN-3c energy calculation with the SMD solvation model and slightly modified epsilon value 
    for the CPCM part. Also modify the radius for hydrogen. 
    """
    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_xyz("inp.xyz")
    calc.input.add_simple_keywords(
        Scf.NOAUTOSTART, Dft.R2SCAN_3C, SolvationModel.CPCM(Solvent.WATER)
    )

    calc.input.add_blocks(
        BlockCpcm(epsilon=80, smd=True, smdsolvent=Solvent.WATER, radius=Radius(n=1, value=1.5))
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
