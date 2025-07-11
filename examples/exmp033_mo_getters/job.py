#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.simple_keywords import BasisSet
from opi.input.simple_keywords import Method
from opi.input.simple_keywords import Scf
from opi.input.simple_keywords import Task
from opi.input.simple_keywords import Dft
from opi.input.structures import Structure

if __name__ == "__main__":
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_xyz("inp.xyz")
    calc.structure.charge = 1
    calc.structure.multiplicity = 2
    calc.input.add_simple_keywords(
        Scf.NOAUTOSTART,
        Dft.PBE0,
        BasisSet.DEF2_SVP,
        Task.SP,
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

    print(output.get_hftype())
    print(output.get_nelectrons())
    mos = output.get_mos()
    print(f"HOMO energy: {output.get_homo().orbitalenergy:.8f} Eh")
    print(f"LUMO energy: {output.get_lumo().orbitalenergy:.8f} Eh")
    print(f"HOMO-LUMO gap: {output.get_hl_gap():.2f} eV")
