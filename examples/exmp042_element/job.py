#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.utils.element import Element
from opi.input.structures import Structure

if __name__ == "__main__":
    wd = Path("RUN")
    shutil.rmtree(wd, ignore_errors=True)
    wd.mkdir()

    calc = Calculator(basename="job", working_dir=wd)
    calc.structure = Structure.from_xyz("inp.xyz")

    # > Print cardinal numbers of input file
    for atom in calc.structure.atoms:
        print(atom.element.atomic_number)

    # > Print some other cardinal numbers
    he_element = Element("he")
    print(he_element.atomic_number)





