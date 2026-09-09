#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.simple_keywords import Dft, Scf, Task
from opi.input.structures import Structure
from opi.output.core import Output
from opi.output.models.json.gbw.gbw_results import GbwResults


def run_exmp003(
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
    calc.input.add_simple_keywords(Scf.NOAUTOSTART, Dft.WB97X3C, Task.OPT)
    calc.input.ncores = 4

    calc.write_input()
    calc.run()

    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        print(output.error_message())
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()

    # > Verify that SCF converged
    if not output.scf_converged():
        print(f"ORCA SCF failed to converge, see output file: {output.get_outfile()}")
        sys.exit(1)

    # > Verify that geometry optimization converged
    if not output.geometry_optimization_converged():
        print(
            f"ORCA geometry optimization failed to converge, see output file: {output.get_outfile()}"
        )
        sys.exit(1)

    ngeoms = len(output.results_properties.geometries)
    print("N GEOMETRIES")
    print(ngeoms)
    print("FINAL SINGLE POINT ENERGY")
    print(output.results_properties.geometries[-1].single_point_data.finalenergy)
    print("SCF Energy along trajectory")
    # > Geometry index starts from 1 to *ngeom*
    for igeom in range(0, ngeoms):
        print(
            f"{igeom})", output.results_properties.geometries[igeom].single_point_data.finalenergy
        )
    print("Mulliken charges along trajectory")
    # > Geometry index starts from 1 to *ngeom*
    for igeom in range(0, ngeoms):
        try:
            charges = (
                output.results_properties.geometries[igeom]
                .mulliken_population_analysis[0]
                .atomiccharges
            )
        except TypeError:
            charges = "n/a"
        print(f"{igeom})", charges)

    # > Now we print the final structure as xyz file
    optimized = output.get_structure()
    print(optimized.to_xyz_block())

    # > The final structure is also stored in the gbw file, so it can be obtained from there
    # > instead of from the property JSON.
    from_gbw = output.get_structure_from_gbw()
    print("RMSD between the structure from the property JSON and from the gbw JSON")
    print(optimized.rmsd(from_gbw))

    # > This also works with nothing but the gbw file at hand, i.e. without an `Output` object.
    # > The gbw file is converted to JSON with `orca_2json` on the fly.
    standalone = GbwResults.from_gbw_file(working_dir / "job.gbw").get_structure()
    print("STRUCTURE FROM GBW FILE")
    print(standalone.to_xyz_block())

    # > Now we print the last gradient calculated which is for
    # > the structure one step before the final structure
    print(output.get_gradient(index=-2))

    return output


if __name__ == "__main__":
    run_exmp003()
