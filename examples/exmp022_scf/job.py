#!/usr/bin/env python3

import sys
import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockScf
from opi.input.simple_keywords import BasisSet
from opi.input.simple_keywords import Dft
from opi.input.simple_keywords import Scf
from opi.input.simple_keywords import ShellType
from opi.input.structures import Structure

if __name__ == "__main__":
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    """
    Run a PBE0/def2-SVP energy calculation and rotate the initial guess
    """
    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_xyz("inp.xyz")
    calc.input.add_simple_keywords(
        ShellType.UKS,
        Scf.NOAUTOSTART,
        Dft.PBE0,
        BasisSet.DEF2_SVP,
    )

    calc.input.add_blocks(BlockScf(rotate=[19, 20], diis={"start": 0.1}))

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
