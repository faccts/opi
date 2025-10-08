#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockDocker
from opi.input.simple_keywords import Sqm
from opi.input.structures import Properties, Structure


def run_exmp050(
    structure: Structure | None = None, working_dir: Path | None = Path("RUN")
) -> tuple[list[Structure], list[Properties]]:
    # > recreate the working dir
    shutil.rmtree(working_dir, ignore_errors=True)
    working_dir.mkdir()

    # > Guest structure lies in example folder
    example_folder = Path(__file__).parent

    # > if no structure is given read structure from inp.xyz
    if structure is None:
        structure = Structure.from_xyz("inp.xyz")

    # > set up the calculator
    calc = Calculator(basename="job", working_dir=working_dir)
    calc.structure = structure
    calc.input.add_simple_keywords(Sqm.GFN2_XTB)

    calc.input.add_blocks(BlockDocker(guest=example_folder / "inp.xyz"))

    # > write the input and run the calculation
    calc.write_input()
    calc.run()

    # > get the output and check some results
    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()

    # > Print graph to visualize available results
    output.print_graph()

    structures = Structure.from_trj_xyz(
        working_dir / f"{calc.basename}.docker.struc1.all.optimized.xyz"
    )

    properties_list = Properties.from_trj_xyz(
        working_dir / f"{calc.basename}.docker.struc1.all.optimized.xyz", mode="docker"
    )

    # > Print structures that were read
    for structure, properties in zip(structures, properties_list):
        print(f"FINAL ENERGY: {properties.energy_total}")
        print(structure.to_xyz_block())

    return structures, properties_list


if __name__ == "__main__":
    output = run_exmp050()
