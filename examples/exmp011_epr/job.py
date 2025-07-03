#!/usr/bin/env python3

import sys
import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import (
    BlockEprnmr,
    Nuclei,
    NucleiFlag,
)
from opi.input.simple_keywords import AuxBasisSet, BasisSet, Dft
from opi.input.structures import Structure
from opi.utils.element import Element

if __name__ == "__main__":
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_xyz("inp.xyz")
    calc.structure.multiplicity = 2
    calc.input.add_simple_keywords(Dft.B3LYP, BasisSet.EPR_II, AuxBasisSet.AUTOAUX)

    calc.input.add_blocks(
        BlockEprnmr(
            gtensor=True,
            nuclei=Nuclei(atom=Element.HYDROGEN, flags=NucleiFlag(adip=True,aiso=True,aorb=True)),
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
