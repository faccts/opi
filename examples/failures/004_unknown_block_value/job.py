#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockScf
from opi.input.simple_keywords import BasisSet, Method, Scf, Task
from opi.input.structures import Structure
from opi.output.core import Output


def unknown_block_value(
    structure: Structure | None = None, working_dir: Path | None = Path("RUN")
) -> Output:
    # > recreate the working dir
    shutil.rmtree(working_dir, ignore_errors=True)
    working_dir.mkdir()

    # > if no structure is given take a smiles
    if structure is None:
        structure = Structure.from_smiles("O")

    # > set up the calculator
    calc = Calculator(basename="job", working_dir=working_dir)
    calc.structure = structure
    calc.input.add_simple_keywords(
        Scf.NOAUTOSTART,
        Method.HF,
        BasisSet.DEF2_SVP,
        Task.SP,
    )

    # calc.input.add_arbitrary_string("!hf hf hf")
    # calc.input.add_arbitrary_string("%novalidblock")
    scf_block = BlockScf()
    scf_block.add_option(name="maxiter", val="invalid_value")
    calc.input.add_blocks(scf_block)

    # > write the input and run the calculation
    calc.write_input()
    calc.run()

    # > get the output and check some results
    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        print(output.error_message())
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()

    # check for convergence of the SCF
    if output.results_properties.geometries[0].single_point_data.converged:
        print("SCF CONVERGED")
    else:
        print("SCF DID NOT CONVERGE")
        sys.exit(1)

    print("FINAL SINGLE POINT ENERGY")
    print(output.get_final_energy())
    # > is equal to
    print(output.results_properties.geometries[-1].single_point_data.finalenergy)

    return output


if __name__ == "__main__":
    output = unknown_block_value()
