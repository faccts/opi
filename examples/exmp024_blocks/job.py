#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockMethod
from opi.input.simple_keywords import (
    BasisSet,
    DispersionCorrection,
    Method,
    Scf,
    SolvationModel,
    Solvent,
    Task,
)
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp024(
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
    calc.input.add_simple_keywords(
        Scf.NOAUTOSTART,
        Method.HF,
        BasisSet.DEF2_SVP,
        Task.SP,
        SolvationModel.CPCM(Solvent.WATER),
        DispersionCorrection.D3,
    )

    # Test if specific simple keywords were added
    keywordlist = [Scf.NOAUTOSTART, Task.FREQ, "GOAT", "noAutoStart"]
    checks = calc.input.has_simple_keywords(*keywordlist)
    for keyword, check in zip(keywordlist, checks):
        print(f"keyword {keyword} has {'been added' if check else 'not been added'}")

    # add block, get it, modify it, and add it back to the Calculator
    calc.input.add_blocks(BlockMethod(d3s6=0.64, d3a1=0.3065, d3s8=0.9147, d3a2=5.0570))
    block = calc.input.get_blocks(BlockMethod)
    # modify the %method block
    block[BlockMethod].d3s6 = 0.4
    calc.write_input()
    calc.run()

    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()

    print("FINAL SINGLE POINT ENERGY")
    print(output.results_properties.geometries[0].single_point_data.finalenergy)
    return output


if __name__ == "__main__":
    run_exmp024()
