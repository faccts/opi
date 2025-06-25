#!/usr/bin/env python3

import sys
import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockMdci
from opi.input.simple_keywords import BasisSet, Wft
from opi.input.structures import Structure

# > Perform a EOM-CCSD/def2-SVP calculation for the first five excited states
if __name__ == "__main__":
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_xyz("inp.xyz")
    calc.input.add_simple_keywords(Wft.EOM_CCSD, BasisSet.DEF2_SVP)

    calc.input.add_blocks(BlockMdci(nroots=5))

    calc.write_input()
    calc.run()

    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()
