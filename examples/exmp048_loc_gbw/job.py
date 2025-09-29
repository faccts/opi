#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

import numpy as np

from opi.core import Calculator
from opi.input.simple_keywords import BasisSet, Dft, Scf, Task
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp048(
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
    calc.charge = 0
    calc.multiplicity = 1
    calc.input.add_simple_keywords(
        Scf.NOAUTOSTART,
        Dft.TPSS,
        BasisSet.DEF2_SVP,
        Task.SP,
    )

    # > Add arbitrary string for localization
    calc.input.add_arbitrary_string("%loc\nLocMet PM\nend\n")

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
    if output.scf_converged():
        print("SCF CONVERGED")
    else:
        print("SCF DID NOT CONVERGE")
        sys.exit(1)

    # > save the MOs
    mos = output.get_mos()["mo"]

    # > Get the integrals
    cmo = np.array([mo.mocoefficients for mo in mos])
    s = output.get_int_overlap(recreate_json=True)
    h = output.get_int_hcore(recreate_json=True)
    f = output.get_int_f(recreate_json=True)
    fao = h + f

    smo = cmo @ s @ cmo.T

    fmo = cmo @ fao @ cmo.T

    # > Create gbw json file with LMOs and parse it
    output.create_gbw_json(force=True, suffix=".loc")
    output.parse()

    # > save the LMOs
    lmos = output.get_mos()["mo"]

    # > Transform Fock matrix in LMO basis
    clmo = np.array([mo.mocoefficients for mo in lmos])
    flmo = clmo @ fao @ clmo.T

    # > save overlap in MO basis to file
    np.savetxt(working_dir / "smo.txt", smo, fmt="%.4f")
    # > save Fock matrix in AO basis to file
    np.savetxt(working_dir / "fao.txt", fao, fmt="%.4f")
    # > save Fock matrix in MO basis to file
    np.savetxt(working_dir / "fmo.txt", fmo, fmt="%.4f")
    # > save Fock matrix in LMO basis to file
    np.savetxt(working_dir / "flmo.txt", flmo, fmt="%.4f")


if __name__ == "__main__":
    run_exmp048()
