#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockAutoCI
from opi.input.simple_keywords import BasisSet, Scf
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp016(
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
    calc.input.add_simple_keywords(BasisSet.DEF2_SVP, Scf.VERYTIGHTSCF)
    calc.input.ncores = 8

    calc.input.add_blocks(BlockAutoCI(citype="CISD"))

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
    run_exmp016()
