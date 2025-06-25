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
from opi.input.simple_keywords import (
    AuxBasisSet,
    BasisSet,
    Property,
    SolvationModel,
    Solvent,
    Wft,
)
from opi.input.structures import Structure
from opi.utils.element import Element

if __name__ == "__main__":
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_xyz("inp.xyz")
    calc.input.add_simple_keywords(
        Wft.RIMP2,
        BasisSet.PCSSEG_2,
        AuxBasisSet.AUTOAUX,
        Property.NMR,
        SolvationModel.CPCM(Solvent.CHLOROFORM),
    )

    calc.input.add_blocks(
        BlockEprnmr(nuclei=Nuclei(atom=Element.HYDROGEN, flags=(NucleiFlag(shift=True,ssall=True))))
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
