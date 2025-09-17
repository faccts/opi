#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockMethod
from opi.input.simple_keywords import BasisSet
from opi.input.simple_keywords import (
    DispersionCorrection,
)
from opi.input.simple_keywords import Method
from opi.input.simple_keywords import Scf
from opi.input.simple_keywords import SolvationModel
from opi.input.simple_keywords import Solvent
from opi.input.simple_keywords import Task
from opi.input.structures import Structure

if __name__ == "__main__":
    """Run HF/def2-SVP single-point energies on a trajectory file"""
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    # > Read structures from inp.xyz
    structures = Structure.from_trj("inp.xyz")
    print(f"Number of structures in inp.xyz: {len(structures)}")
    # > Read structures from other.xyz (empty lines in between)
    structures_other = Structure.from_trj("other.xyz")
    print(f"Number of structures in other.xyz: {len(structures_other)}")

    for index, structure in enumerate(structures):
        calc = Calculator(basename="job", working_dir=wd)
        calc.structure = structure
        calc.input.add_simple_keywords(
            Scf.NOAUTOSTART,
            Method.HF,
            BasisSet.DEF2_SVP,
            Task.SP
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

        # check for convergence of the SCF
        if not output.scf_converged():
            print("SCF DID NOT CONVERGE")
            sys.exit(1)

        print(index, output.get_final_energy())
