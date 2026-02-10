#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockNeb
from opi.input.simple_keywords import Neb, Scf, Sqm
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp039(working_dir: Path | None = Path("RUN")) -> Output:
    example_folder = Path(__file__).parent
    shutil.rmtree(working_dir, ignore_errors=True)
    working_dir.mkdir()

    calc = Calculator(basename="job", working_dir=working_dir)
    shutil.copy(example_folder / "prod.xyz", working_dir / "prod.xyz")
    calc.structure = Structure.from_xyz(example_folder / "reac.xyz")
    calc.input.add_simple_keywords(Scf.NOAUTOSTART, Sqm.NATIVE_GFN2_XTB, Neb.NEB_TS)

    calc.input.add_blocks(BlockNeb(neb_end_xyzfile="prod.xyz"))

    calc.write_input()
    calc.run()

    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()

    N = len(output.results_gbw)
    print(f"N: {N}")
    # > Print hl gap for scan
    for index, gbw in enumerate(output.results_gbw[1:], start=1):
        print(index, output.get_hl_gap(index))

    # > Printing energies
    for index, gbw in enumerate(output.results_properties.geometries[1:], start=1):
        print(index, output.get_final_energy(index=index))

    return output


if __name__ == "__main__":
    run_exmp039()
