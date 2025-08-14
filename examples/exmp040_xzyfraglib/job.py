#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockFrag
from opi.input.simple_keywords import Sqm
from opi.input.simple_keywords import Scf
from opi.input.structures import Structure

if __name__ == "__main__":
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    struc_file = "struc.xyz"
    lib_file = "frag_lib.xyz"

    shutil.copy(struc_file, wd)
    shutil.copy(lib_file, wd)

    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_xyz(struc_file)
    calc.input.add_simple_keywords(
        Scf.NOAUTOSTART,
        Sqm.NATIVE_GFN2_XTB,
    )

    calc.input.add_blocks(BlockFrag(printlevel=3, fragproc="extlib", xzyfraglib=lib_file))

    calc.write_input()
    calc.run()

    output = calc.get_output(create_gbw_json=True)
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()
