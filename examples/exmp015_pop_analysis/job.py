#!/usr/bin/env python3

import sys
import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockElprop
from opi.input.simple_keywords import (
    AtomicCharge,
    AuxBasisSet,
    BasisSet,
    Dft,
    SolvationModel,
    Solvent,
)
from opi.input.structures import Structure

if __name__ == "__main__":
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_xyz("inp.xyz")
    calc.input.add_simple_keywords(
        Dft.DSD_PBEP86,
        BasisSet.DEF2_SVP,
        AuxBasisSet.DEF2_SVP_C,
        AuxBasisSet.DEF2_J,
        AtomicCharge.CHELPG,
        AtomicCharge.HIRSHFELD,
        AtomicCharge.MULLIKEN,
        AtomicCharge.LOEWDIN,
        AtomicCharge.MAYER,
        AtomicCharge.MBIS,
        AtomicCharge.REDUCEDPOP,
        SolvationModel.CPCM(Solvent.WATER),
    )

    calc.input.add_blocks(BlockElprop(dipole=True, quadrupole=True, polar="analytic"))

    calc.write_input()
    calc.run()

    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()

    print("Mulliken: ", output.get_mulliken())
    print("Loewdin: ", output.get_loewdin())
    print("CHELPG: ", output.get_chelpg())
    print("Hirshfeld: ", output.get_hirshfeld())
    print("Mayer: ", output.get_mayer())
    print("MBIS: ", output.get_mbis())

    dip = output.get_dipole()
    print(f"Total dipole moment (x,y,z): {dip[0].dipoletotal[0][0]:.8f}, {dip[0].dipoletotal[1][0]:.8f}, "
          f"{dip[0].dipoletotal[2][0]:.8f}")
    quad = output.get_quadrupole()
    print(f"Total quadrupole moment (xx,yy,zz): {quad[0].quadtotal[0][0]:.8f}, {quad[0].quadtotal[1][0]:.8f}, {quad[0].quadtotal[2][0]:.8f}")
    print(f"Total quadrupole moment (xy,xz,yz): {quad[0].quadtotal[3][0]:.8f}, {quad[0].quadtotal[4][0]:.8f}, {quad[0].quadtotal[5][0]:.8f}")

    print(output.get_polarizability())
