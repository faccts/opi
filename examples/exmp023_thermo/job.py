#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import (
    BlockFreq,
)
from opi.input.simple_keywords import (
    BasisSet,
    Dft,
    Scf,
    Task,
)
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp023(
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
    calc.input.add_simple_keywords(Scf.NOAUTOSTART, BasisSet.DEF2_TZVP, Dft.TPSS, Task.FREQ)
    calc.input.add_blocks(
        BlockFreq(temp=500, numfreq=True, quasirrho=False, pressure=1.5, partial_hess=[0, 1])
    )
    calc.input.ncores = 4

    calc.write_input()
    calc.run()

    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()

    ngeoms = len(output.results_properties.geometries)
    print("N GEOMETRIES")
    print(ngeoms)
    print("FINAL SINGLE POINT ENERGY")
    print(output.results_properties.geometries[0].dft_energy.finalen)
    print("Temperature [K]")
    print(output.results_properties.geometries[0].thermochemistry_energies[0].temperature)
    print("Final Gibbs free energy")
    print(output.results_properties.geometries[0].thermochemistry_energies[0].freeenergyg)

    return output


if __name__ == "__main__":
    run_exmp023()
