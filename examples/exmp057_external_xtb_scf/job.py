#!/usr/bin/env python3
"""
Example: External xTB calculation with SCF convergence check.

Runs GFN2-xTB using the external xTB calculation method and checks that
`output.scf_converged()` properly detects convergence in the .out file.
"""

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.simple_keywords import Scf, Sqm, Task
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp057(
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
    calc.input.add_simple_keywords(Scf.NOAUTOSTART, Sqm.GFN2_XTB, Task.SP)

    calc.write_input()
    calc.run()

    # > Get output without version check since it is an external method
    output = calc.get_output(version_check=False)
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        print(output.error_message())
        sys.exit(1)

    # > parse output properties
    output.parse()

    # > check for convergence of the external xTB SCF
    if output.scf_converged():
        print("EXTERNAL XTB SCF CONVERGED")
    else:
        print("EXTERNAL XTB SCF DID NOT CONVERGE")
        sys.exit(1)

    return output


if __name__ == "__main__":
    run_exmp057()
