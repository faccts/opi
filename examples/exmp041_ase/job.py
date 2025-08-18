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
from ase import Atoms

if __name__ == "__main__":
    
    # Create a water molecule (H2O)
    # Positions in Ångström
    positions = [
        [0.000, 0.000, 0.000],     # O
        [0.757, 0.586, 0.000],     # H
        [-0.757, 0.586, 0.000],    # H
    ]
    symbols = ['O', 'H', 'H']

    # Create ASE Atoms object
    water = Atoms(symbols=symbols, positions=positions)

    # Optionally set info
    water.info["charge"] = -1
    water.info["multiplicity"] = 2
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_ase(water)
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
    if output.results_properties.geometries[0].single_point_data.converged:
        print("SCF CONVERGED")
    else:
        print("SCF DID NOT CONVERGE")
        sys.exit(1)

    print("FINAL SINGLE POINT ENERGY")
    print(output.get_final_energy())
