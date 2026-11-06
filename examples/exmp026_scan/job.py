#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BlockGeom, Scan
from opi.input.simple_keywords import BasisSet, Method, Scf, Task
from opi.input.structures import Structure
from opi.output.core import Output


def check_termination(output: Output) -> None:
    """Exit if the ORCA calculation did not terminate normally."""
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        print(output.error_message())
        sys.exit(1)


def run_exmp026(
    structure: Structure | None = None, working_dir: Path | None = Path("RUN")
) -> Output:
    # > recreate the working dir
    shutil.rmtree(working_dir, ignore_errors=True)
    working_dir.mkdir()

    # > if no structure is given read structure from inp.xyz
    if structure is None:
        structure = Structure.from_xyz("inp.xyz")

    calc_bond = Calculator(basename="job", working_dir=working_dir)
    calc_bond.structure = structure
    calc_bond.input.add_simple_keywords(
        Scf.NOAUTOSTART,
        Method.HF,
        BasisSet.MINIX,
        Task.OPT,
    )

    # > A scan can be defined with a `Scan` object ...
    calc_bond.input.add_blocks(
        BlockGeom(scan=Scan(mode="B", atom1=0, atom2=1, startvalue=1.1, endvalue=2.1, steps=5))
    )
    calc_bond.write_input()
    calc_bond.run()
    output_bond = calc_bond.get_output()
    check_termination(output_bond)
    output_bond.parse()

    # > Print hl gap for scan
    for index, gbw in enumerate(output_bond.results_gbw[1:], start=1):
        print(index, output_bond.get_hl_gap(index))

    # > Plot mos for scan
    for index, gbw in enumerate(output_bond.results_gbw[1:], start=1):
        homo_id = output_bond.get_homo().index
        cube_output = output_bond.plot_mo(homo_id, gbw_index=index)
        print(index, cube_output)

    # > Plot density for scan
    for index, gbw in enumerate(output_bond.results_gbw[1:], start=1):
        cube_output = output_bond.plot_density(gbw_index=index)
        print(index, cube_output)

    # > Access energies for scan
    for index, gbw in enumerate(output_bond.results_properties.geometries[1:], start=1):
        print(index, output_bond.get_final_energy(index=index))

    # > Scan an angle with a relaxed surface scan
    calc_angle = Calculator(basename="scan_angle", working_dir=working_dir)
    calc_angle.structure = structure
    calc_angle.input.add_simple_keywords(
        Scf.NOAUTOSTART,
        Method.HF,
        BasisSet.DEF2_SVP,
        Task.OPT,
    )

    # > ... or with a string in ORCA syntax
    calc_angle.input.add_blocks(BlockGeom(scan="A  1 0 2 = 110, 170, 6"))
    calc_angle.write_input()
    calc_angle.run()
    check_termination(calc_angle.get_output())

    # > Scan a dihedral over an explicit list of values given as string
    calc_dihedral = Calculator(basename="scan_dihedral", working_dir=working_dir)
    calc_dihedral.structure = structure
    calc_dihedral.input.add_simple_keywords(
        Scf.NOAUTOSTART,
        Method.HF,
        BasisSet.DEF2_SVP,
        Task.OPT,
    )

    calc_dihedral.input.add_blocks(BlockGeom(scan="D 6 1 0 2 [60 90 120]"))
    calc_dihedral.write_input()
    calc_dihedral.run()
    check_termination(calc_dihedral.get_output())

    # > Scan a bond over an explicit list of values given as `Scan` object
    calc_valuelist = Calculator(basename="scan_valuelist", working_dir=working_dir)
    calc_valuelist.structure = structure
    calc_valuelist.input.add_simple_keywords(
        Scf.NOAUTOSTART,
        Method.HF,
        BasisSet.MINIX,
        Task.OPT,
    )

    calc_valuelist.input.add_blocks(
        BlockGeom(scan=Scan(mode="B", atom1=0, atom2=1, valuelist=[1.1, 1.5, 2.1]))
    )
    calc_valuelist.write_input()
    calc_valuelist.run()
    check_termination(calc_valuelist.get_output())

    return output_bond
