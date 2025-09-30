#!/usr/bin/env python3

import sys
from pathlib import Path

from opi.core import Calculator
from opi.output.core import Output


def run_exmp045() -> Output:
    # > Get output of existing calculation and parse it
    example_folder = Path(__file__).parent
    working_dir = example_folder / "RUN"

    # > same basename as existing calculation in the 'RUN' directory
    calc = Calculator(basename="job", working_dir=working_dir)
    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files (will be created by parse from gbw and property.txt files)
    output.parse()

    # check for convergence of the SCF
    if output.results_properties.geometries[0].single_point_data.converged:
        print("SCF CONVERGED")
    else:
        print("SCF DID NOT CONVERGE")
        sys.exit(1)

    print("FINAL SINGLE POINT ENERGY")
    print(output.get_final_energy())
    print(output.get_homo())
    return output


if __name__ == "__main__":
    run_exmp045()
