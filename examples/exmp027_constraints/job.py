#!/usr/bin/env python3

import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockGeom
from opi.input.simple_keywords import BasisSet, Method, Scf, Task
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp027(
    structure: Structure | None = None, working_dir: Path | None = Path("RUN")
) -> Output:
    # > recreate the working dir
    shutil.rmtree(working_dir, ignore_errors=True)
    working_dir.mkdir()

    # > if no structure is given read structure from inp.xyz
    if structure is None:
        structure = Structure.from_xyz("inp.xyz")

    calc_bond = Calculator(basename="job", working_dir=working_dir)
    calc_bond.structure = structure
    calc_bond.input.add_simple_keywords(
        Scf.NOAUTOSTART,
        Method.HF,
        BasisSet.DEF2_SVP,
        Task.OPT,
    )

    constraints = ["B  0 1 1.5 C", "A  1 0 2 115.0 C", "D 6 1 0 2 60 C"]

    # > Constraint bonds, angles, dihedral
    calc_bond.input.add_blocks(BlockGeom(constraints=constraints))
    calc_bond.write_input()
    calc_bond.run()

    return calc_bond.get_output()


if __name__ == "__main__":
    run_exmp027()
