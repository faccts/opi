#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockElprop
from opi.input.simple_keywords import AuxBasisSet, BasisSet, Dft, Task
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp009(
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
    calc.input.add_simple_keywords(Dft.PBE0, BasisSet.DEF2_SVP, AuxBasisSet.DEF2_J, Task.FREQ)

    calc.input.ncores = 4
    calc.input.add_blocks(BlockElprop(polar="analytic"))

    calc.write_input()
    calc.run()

    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()
    return output


if __name__ == "__main__":
    run_exmp009()
