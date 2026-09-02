#!/usr/bin/env python3
import sys
from pathlib import Path

from opi.input.structures import Structure
from opi.simple_tasks import OptResults, OptSettings, OptTask
from opi.simple_tasks.method_settings import DftSettings


def run_exmp062(structure: Structure | None = None, working_dir: Path = Path("RUN")) -> OptResults:
    # > if no structure is given read structure from inp.xyz
    if structure is None:
        structure = Structure.from_xyz("../exmp059_singlepoint_simpletask/inp.xyz")

    # > set up the task
    simple_task = OptTask(
        method="b3lyp",
        basis_set="def2-svp",
        solvation_model="cpcm",
        solvent="water",
        method_settings=DftSettings(scf_maxiter=150),
        task_settings=OptSettings(opt_threshold="tight"),
    )
    # > there are task and method-specific settings, these can be set through kwargs

    # > run the calculation with given data
    opt_result = simple_task.run("job", structure, working_dir=working_dir)

    # > check if the ORCA calculation terminated normally
    if not opt_result.status:
        print("Opt task failed")
        sys.exit(1)

    # > extract optimized structure from the `OptResults` object
    structure = opt_result.structure

    print("Optimized Structure:")
    print(structure.format_orca())

    return opt_result


if __name__ == "__main__":
    run_exmp062()
