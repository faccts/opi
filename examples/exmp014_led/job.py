#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.simple_keywords import Approximation, AuxBasisSet, BasisSet, Dlpno, Scf, Wft
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp014(
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
        Wft.DLPNO_CCSD_T,
        BasisSet.CC_PVDZ,
        AuxBasisSet.CC_PVDZ_C,
        AuxBasisSet.CC_PVTZ_JK,
        Dlpno.TIGHTPNO,
        Scf.TIGHTSCF,
        Approximation.RIJK,
        Dlpno.LED,
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

    # > Obtain the structure and write a new input file with the same fragment IDs
    new_structure = output.get_structure()
    new_calc = Calculator(basename="new_job", working_dir=working_dir)
    new_calc.structure = new_structure
    new_calc.input.add_simple_keywords(
        Wft.DLPNO_CCSD_T,
        BasisSet.CC_PVDZ,
        AuxBasisSet.CC_PVDZ_C,
        AuxBasisSet.CC_PVTZ_JK,
        Dlpno.TIGHTPNO,
        Scf.TIGHTSCF,
        Approximation.RIJK,
        Dlpno.LED,
    )

    new_calc.write_input()
    return output


if __name__ == "__main__":
    run_exmp014()
