#!/usr/bin/env python3

import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockGoat
from opi.input.simple_keywords import Sqm, Goat
from opi.input.structures import Structure

if __name__ == "__main__":
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_xyz("inp.xyz")
    calc.input.add_simple_keywords(Sqm.GFN2_XTB, Goat.GOAT)
    calc.input.add_blocks(BlockGoat(maxiter=128, explore=True))
    calc.input.ncores = 4

    calc.write_input()
    calc.run()

    # > there is not really much output to be gained from a goat run
    # > other than the finalensemble.xyz or a final single point energy
