#!/usr/bin/env python3
"""
Example: GFN2-xTB transition-state optimisation followed by a frequency calculation.

Starting from a near-TS geometry, OPTTS locates the first-order saddle point and FREQ
then computes the Hessian. A true transition state has exactly one imaginary (negative)
frequency, which is retrieved via ``get_imaginary_frequencies()``.
"""

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.simple_keywords import (
    Opt,
    Scf,
    Sqm,
    Task,
)
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp056(
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
    calc.input.add_simple_keywords(Scf.NOAUTOSTART, Sqm.NATIVE_GFN2_XTB, Opt.OPTTS, Task.NUMFREQ)

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

    print("ALL VIBRATIONAL FREQUENCIES [cm-1]")
    frequencies = output.get_frequencies()
    for mode, freq in frequencies.items():
        print(f"  Mode {mode:3d}: {freq:12.4f}")

    print("IMAGINARY FREQUENCIES [cm-1]")
    imaginary = output.get_imaginary_frequencies()
    if imaginary:
        for mode, freq in imaginary.items():
            print(f"  Mode {mode:3d}: {freq:12.4f}")
    else:
        print("  None")

    print(f"Number of imaginary frequencies: {len(imaginary)}")
    print("Is PES transition state")
    print(output.is_pes_transition_state())
    print("FINAL SINGLE POINT ENERGY")
    print(output.get_final_energy())

    return output


if __name__ == "__main__":
    run_exmp056()
