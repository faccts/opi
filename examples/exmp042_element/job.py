#!/usr/bin/env python3

import shutil
from pathlib import Path

from opi.core import Calculator
from opi.input.structures import Structure
from opi.output.core import Output
from opi.utils.element import Element


def run_exmp042(
    structure: Structure | None = None, working_dir: Path | None = Path("RUN")
) -> Output:
    # > recreate the working dir
    shutil.rmtree(working_dir, ignore_errors=True)
    working_dir.mkdir()

    # > if no structure is given read structure from inp.xyz
    if structure is None:
        structure = Structure.from_xyz("inp.xyz")

    # > Disable version check to be ORCA independent
    calc = Calculator(basename="job", working_dir=working_dir, version_check=False)
    calc.structure = structure

    # > Print cardinal numbers of input file
    for atom in calc.structure.atoms:
        print(atom.element.atomic_number)

    # > Print some other cardinal numbers
    he_element = Element("he")
    print(he_element.atomic_number)

    return calc.get_output()


if __name__ == "__main__":
    run_exmp042()
