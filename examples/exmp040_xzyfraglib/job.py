#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockFrag
from opi.input.simple_keywords import Scf, Sqm
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp040(working_dir: Path | None = Path("RUN")) -> Output:
    current_folder = Path(__file__).parent
    working_dir = current_folder / "RUN"
    shutil.rmtree(working_dir, ignore_errors=True)
    working_dir.mkdir()

    struc_file = current_folder / "struc.xyz"
    lib_file = current_folder / "frag_lib.xyz"

    shutil.copy(struc_file, working_dir)
    shutil.copy(lib_file, working_dir)

    calc = Calculator(basename="job", working_dir=working_dir)
    calc.structure = Structure.from_xyz(struc_file)
    calc.input.add_simple_keywords(
        Scf.NOAUTOSTART,
        Sqm.NATIVE_GFN2_XTB,
    )

    calc.input.add_blocks(BlockFrag(printlevel=3, fragproc="extlib", xzyfraglib=str(lib_file)))

    calc.write_input()
    calc.run()

    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()

    return output


if __name__ == "__main__":
    run_exmp040()
