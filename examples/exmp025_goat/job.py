#!/usr/bin/env python3

import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockGoat
from opi.input.simple_keywords import Goat, Sqm
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp025(
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
    calc.input.add_simple_keywords(Sqm.GFN2_XTB, Goat.GOAT)
    calc.input.add_blocks(BlockGoat(maxiter=128, explore=True))
    calc.input.ncores = 4

    calc.write_input()
    calc.run()

    # > there is not really much output to be gained from a goat run
    # > other than the finalensemble.xyz or a final single point energy

    return calc.get_output()


if __name__ == "__main__":
    run_exmp025()
