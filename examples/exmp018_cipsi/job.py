#!/usr/bin/env python3

import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockIce
from opi.input.simple_keywords import BasisSet
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp018(
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
    calc.input.add_simple_keywords(BasisSet.DEF2_SVP)

    calc.input.add_blocks(
        BlockIce(
            nel=10,
            norb=13,
            nroots=1,
            integrals="exact",
            icetype="CFGs",
            tgen=0.0001,
            tvar=0.00000000001,
            etol=0.000001,
        )
    )

    calc.write_input()
    calc.run()
    output = calc.get_output()
    print("FINAL ENERGY")
    # > Does not work at the moment
    print(output.get_final_energy())
    return output


if __name__ == "__main__":
    run_exmp018()
