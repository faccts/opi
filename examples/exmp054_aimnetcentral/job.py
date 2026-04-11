#!/usr/bin/env python3

from pathlib import Path

from opi.core import Calculator
from opi.external_methods import AimnetCentralConfig, create_aimnetcentral_extopt
from opi.input.simple_keywords import Task
from opi.input.structures import Structure


def main() -> None:
    working_dir = Path("RUN")
    working_dir.mkdir(exist_ok=True)

    calc = Calculator(basename="job", working_dir=working_dir, version_check=False)
    calc.structure = Structure.from_xyz("inp.xyz")

    extopt_kw, aimnet_block = create_aimnetcentral_extopt(
        AimnetCentralConfig(
            model="aimnet2_2025",
            device="cuda",
            compile_model=True,
            coulomb_method="dsf",
            coulomb_cutoff=15.0,
            dftd3_cutoff=15.0,
        )
    )

    calc.input.add_simple_keywords(extopt_kw, Task.OPT)
    calc.input.add_blocks(aimnet_block)
    calc.write_input()


if __name__ == "__main__":
    main()
