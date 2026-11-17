#!/usr/bin/env python3
"""
Example: Write a gbw file from parsed output data and reuse it as an SCF guess.

A Hartree-Fock calculation is run and its gbw-JSON file is parsed into `GbwResults`.
`GbwResults.to_gbw_file()` converts that data back into a gbw file by running
`orca_2json <json-file> -gbw`. The written file holds the geometry, the basis set and the
molecular orbitals, so it can be used as an SCF guess (`MORead`) of a second calculation.

Note that ORCA only creates a rudimentary gbw file, which contains less information than the
gbw file written by the calculation itself.
"""

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.simple_keywords import BasisSet, Method, Scf, Task
from opi.input.structures import Structure
from opi.output.core import Output
from opi.output.models.json.gbw.gbw_results import GbwResults


def run_exmp058(
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
    calc.input.add_simple_keywords(Scf.NOAUTOSTART, Method.HF, BasisSet.DEF2_SVP, Task.SP)

    calc.write_input()
    calc.run()

    output = calc.get_output()
    if not output.terminated_normally() and output.scf_converged():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        print(output.error_message())
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()

    print("FINAL SINGLE POINT ENERGY")
    print(output.get_final_energy())

    # > The gbw-JSON file of the calculation, parsed into `GbwResults`
    results_gbw = output.results_gbw[0]
    print("NUMBER OF MOLECULAR ORBITALS")
    print(len(results_gbw.molecule.molecularorbitals.mos))

    # > Write a gbw file from the parsed data. The file has to be created inside the working
    # > directory, as ORCA only accepts a `%moinp` file below its own working directory.
    gbw_file = results_gbw.to_gbw_file(working_dir / "from_results.gbw")
    print("GBW FILE WRITTEN FROM THE PARSED DATA")
    print(f"{gbw_file.name} ({gbw_file.stat().st_size} bytes)")

    # > Use the written gbw file as SCF guess of a second calculation
    calc_moread = Calculator(basename="job_moread", working_dir=working_dir)
    # > Get the structure form the gbw file
    calc_moread.structure = GbwResults.from_gbw_file(gbw_file).get_structure()
    calc_moread.input.add_simple_keywords(
        Scf.NOAUTOSTART, Scf.MOREAD, Method.HF, BasisSet.DEF2_SVP, Task.SP
    )
    calc_moread.input.moinp = gbw_file

    calc_moread.write_input()
    calc_moread.run()

    output_moread = calc_moread.get_output()
    if not output_moread.terminated_normally() and output.scf_converged():
        print(f"ORCA calculation failed, see output file: {output_moread.get_outfile()}")
        print(output_moread.error_message())
        sys.exit(1)
    # << END OF IF

    output_moread.parse()

    print("FINAL SINGLE POINT ENERGY WITH THE WRITTEN GBW FILE AS GUESS")
    print(output_moread.get_final_energy())

    return output_moread


if __name__ == "__main__":
    run_exmp058()
