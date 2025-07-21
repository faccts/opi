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
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_xyz("inp.xyz",charge=1,multiplicity=2)
    calc.input.add_simple_keywords(
        Scf.NOAUTOSTART,
        Method.HF,
        BasisSet.DEF2_SVP,
        Task.SP,
        SolvationModel.CPCM(Solvent.WATER),
        DispersionCorrection.D3,
    )

    calc.input.add_blocks(BlockMethod(d3s6=0.64, d3a1=0.3065, d3s8=0.9147, d3a2=5.0570))

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

    # Use orca_plot to plot mo 5,the density and the spin_density
    mo_5 = output.plot_mo(5)
    density = output.plot_density()
    spin_density = output.plot_spin_density()

    # Print paths to the cube files
    print(mo_5)
    print(density)
    print(spin_density)

    # > save mo in script dir
    with open(mo_5.path.name,"w") as file:
        file.write(mo_5.cube)
    # > save mo in script dir line by line
    with open(f"{mo_5.path.name}.from_iterator", "w") as file:
        for line in mo_5:
            file.write(line)

