#!/usr/bin/env python3
"""
Example: GFN-FF geometry optimisation with `Grepper` fallback.

GFN-FF is an external force field method in ORCA (calls xtb internally).
It writes a property JSON file, but the file contains no geometry entries,
so the normal JSON-based output parsing returns None for energies, gradients,
and structures. The `Grepper` fallback (enabled by default) recovers these
quantities directly from the plain-text .out file.
"""

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.simple_keywords import ForceField, Task
from opi.input.structures import Structure
from opi.output.core import Output


def run_exmp055(
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
    # > GFN-FF is an external method; ORCA writes a .out file but no property JSON
    calc.input.add_simple_keywords(ForceField.GFN_FF, Task.OPT)

    calc.write_input()
    calc.run()

    # > Get output without version check since it is not possible with external methods
    output = calc.get_output(version_check=False)
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        print(output.error_message())
        sys.exit(1)

    # > parse() loads a property JSON with no geometry entries for GFN-FF
    output.parse()

    # > get_final_energy / get_structure / get_gradient fall back to grepping the .out
    # > file automatically when no JSON data is available (fallback=True by default)
    final_energy = output.get_final_energy()
    print("FINAL SINGLE POINT ENERGY (from .out fallback)")
    print(final_energy)

    optimized = output.get_structure()
    print("OPTIMIZED STRUCTURE (from .out fallback)")
    print(optimized.to_xyz_block())

    # > In a geometry optimisation the gradient is not printed for the final geometry.
    # > Use index=-2 to retrieve the gradient from the second-to-last step.
    gradient = output.get_gradient(index=-2)
    print("GRADIENT AT SECOND-TO-LAST STEP in Eh/Bohr (from .out fallback)")
    print(gradient)

    # > The fallback supports iterating over individual optimisation steps.
    # > get_final_energy returns None once the index exceeds the number of steps.
    step = 0
    print("ENERGIES ALONG OPTIMISATION TRAJECTORY")
    while True:
        e = output.get_final_energy(index=step)
        if e is None:
            break
        s = output.get_structure(index=step)
        print(f"  step {step:3d}  E = {e:.10f}  ({len(s.atoms)} atoms)")
        step += 1

    return output


if __name__ == "__main__":
    run_exmp055()
