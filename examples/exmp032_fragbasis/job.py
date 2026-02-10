#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockBasis, FragAuxJ, FragBasis, FragEcp
from opi.input.simple_keywords import AuxBasisSet, BasisSet, Dft, Ecp, OutputControl, Scf
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp032(
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
        OutputControl.PRINTBASIS, Dft.BP86, Scf.NOITER, BasisSet.DEF2_SVP, AuxBasisSet.DEF2_J
    )

    calc.input.add_blocks(
        BlockBasis(
            fragbasis=FragBasis(frag={1: BasisSet.DEF2_TZVP, 2: BasisSet.DEF2_QZVP}),
            fragauxj=FragAuxJ(frag={2: AuxBasisSet.AUTOAUX, 3: AuxBasisSet.DEF2_JK}),
            fragecp=FragEcp(frag={3: Ecp.SK_MCDHF_RSC}),
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

    return output


if __name__ == "__main__":
    run_exmp032()
