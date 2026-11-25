#!/usr/bin/env python3

import shutil
import sys
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
from opi.output.core import Output
from opi.utils.element import Element


def run_exmp012(
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
        Wft.RIMP2,
        BasisSet.PCSSEG_2,
        AuxBasisSet.AUTOAUX,
        Property.NMR,
        SolvationModel.CPCM(Solvent.CHLOROFORM),
    )

    calc.input.add_blocks(
        BlockEprnmr(
            nuclei=Nuclei(atom=Element.HYDROGEN, flags=(NucleiFlag(shift=True, ssall=True)))
        )
    )

    calc.write_input()
    calc.run()

    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        print(output.error_message())
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()

    # > Print the isotropic shieldings. ORCA reports one entry per method and density type,
    # > here SCF as well as unrelaxed and relaxed MP2.
    shieldings = output.get_chemical_shift()
    if shieldings is not None:
        for shift in shieldings:
            print(f"Isotropic shieldings ({shift.method}, {shift.level}):")
            for nuc, elem, siso in zip(shift.nuc, shift.elems, shift.siso):
                symbol = Element.from_atomic_number(elem).value
                print(f"  {symbol}{nuc}: {siso:8.3f} ppm")
    # << END OF IF

    # > Print the isotropic spin-spin coupling constants
    couplings = output.get_spin_spin_coupling()
    if couplings is not None:
        for coupling in couplings:
            print(f"Spin-spin couplings ({coupling.method}, {coupling.level}):")
            # > `pairsinfo` holds (index 1, atomic number 1, index 2, atomic number 2)
            for pair, value in zip(coupling.pairsinfo, coupling.pairstotalssciso):
                print(f"  J({pair[0]},{pair[2]}): {value[0]:8.3f} Hz")
    # << END OF IF

    return output


if __name__ == "__main__":
    run_exmp012()
