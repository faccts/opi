#!/usr/bin/env python3

import sys

import pytest

from opi.core import Calculator
from opi.input.blocks import BlockScf
from opi.input.simple_keywords import BasisSet, Method, Scf, Task
from opi.input.structures import Structure
from opi.output.core import Output


@pytest.mark.examples
@pytest.mark.orca
@pytest.mark.xfail
def test_unknown_block_key(tmp_path) -> Output:

    structure = Structure.from_smiles("O")

    # > set up the calculator
    calc = Calculator(basename="job", working_dir=tmp_path)
    calc.structure = structure
    calc.input.add_simple_keywords(
        Scf.NOAUTOSTART,
        Method.HF,
        BasisSet.DEF2_SVP,
        Task.SP,
    )

    scf_block = BlockScf()
    scf_block.add_option(name="invalid_key", val="none")
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
    pytest.main([__file__, "-v", "-s"])
