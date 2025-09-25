#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockSolvator
from opi.input.simple_keywords.solvent import Solvent
from opi.input.structures.structure import Structure
from opi.output.core import Output


def run_exmp036(
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
    calc.structure.charge = 1
    calc.structure.multiplicity = 1
    calc.input.ncores = 16
    calc.input.add_simple_keywords("XTB")
    calc.input.add_simple_keywords(f"ALPB({Solvent.WATER})")
    calc.input.add_blocks(BlockSolvator(nsolv=1))

    calc.write_input()
    calc.run()

    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        sys.exit(1)

    output.parse(read_gbw_json=False)

    print("Solvated xyz file:")
    print(f"\t{output.basename}.solvator.xyz")

    # > Verify output works okay
    # > there is not really much output to be gained from a solvator run
    # > other than the solvator.xyz, solvator.solventbuild.xyz or a final single point energy

    return output


if __name__ == "__main__":
    run_exmp036()
