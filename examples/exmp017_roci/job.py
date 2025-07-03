#!/usr/bin/env python3

import sys
import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockRocis
from opi.input.simple_keywords import AuxBasisSet, BasisSet, ShellType
from opi.input.structures import Structure

if __name__ == "__main__":
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_xyz("inp.xyz")
    calc.structure.charge = -1
    calc.structure.multiplicity = 2

    calc.input.add_simple_keywords(
        ShellType.ROHF,
        BasisSet.DEF2_SVP,
        AuxBasisSet.DEF2_SVP_C,
        AuxBasisSet.DEF2_J,
    )

    calc.input.add_blocks(
        BlockRocis(
            nroots=6,
            maxdim=5,
            etol=0.000001,
            rtol=0.000001,
            maxiter=35,
            nguessmat=512,
            docd=True,
        )
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
