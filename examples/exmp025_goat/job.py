#!/usr/bin/env python3

import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockGoat
from opi.input.simple_keywords import Goat, Sqm
from opi.input.structures import Properties, Structure


def run_exmp025(
    structure: Structure | None = None, working_dir: Path | None = Path("RUN")
) -> tuple[list[Structure], list[Properties]]:
    # > recreate the working dir
    shutil.rmtree(working_dir, ignore_errors=True)
    working_dir.mkdir()

    # > if no structure is given read structure from inp.xyz
    if structure is None:
        structure = Structure.from_xyz("inp.xyz")

    calc = Calculator(basename="job", working_dir=working_dir)
    calc.structure = structure
    calc.input.add_simple_keywords(Sqm.GFN2_XTB, Goat.GOAT)
    calc.input.add_blocks(BlockGoat(maxiter=128, explore=True))
    calc.input.ncores = 4

    calc.write_input()
    calc.run()

    structures = Structure.from_trj_xyz(working_dir / f"{calc.basename}.finalensemble.xyz")

    properties_list = Properties.from_trj_xyz(
        working_dir / f"{calc.basename}.finalensemble.xyz", mode="goat"
    )

    # > Print structures that were read
    for structure, properties in zip(structures, properties_list):
        print(f"FINAL ENERGY: {properties.energy_total}")
        print(structure.to_xyz_block())

    return structures, properties_list


if __name__ == "__main__":
    run_exmp025()
