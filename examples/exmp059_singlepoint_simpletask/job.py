#!/usr/bin/env python3
import sys
from pathlib import Path

from opi.input.simple_keywords import AtomicCharge
from opi.input.structures import Structure
from opi.simple_tasks import SinglePointResults, SinglePointTask


def run_exmp059(
    structure: Structure | None = None, working_dir: Path = Path("RUN")
) -> SinglePointResults:
    # > if no structure is given read structure from inp.xyz
    if structure is None:
        structure = Structure.from_xyz("inp.xyz")

    # > set up the task
    simple_task = SinglePointTask(
        method="b3lyp", basis_set="def2-svp", solvation_model="cpcm", solvent="water"
    )
    # > there are task and method-specific settings, these can be set through kwargs

    # > It is possible to modify the input object associated with the task object for more specific settings
    simple_task.input.add_simple_keywords(AtomicCharge.HIRSHFELD)

    # > run the calculation with given data
    singlepoint_result = simple_task.run("job", structure, working_dir=working_dir)

    # > check if the ORCA calculation terminated normally
    if not singlepoint_result.status:
        print("SinglePoint task failed")
        sys.exit(1)

    # > extract primary property from the `TaskResults` object. For a single point calculation, it is the final energy.
    final_energy = singlepoint_result.final_energy

    print(f"Final single point energy: {final_energy: 10f} Eh")

    return singlepoint_result


if __name__ == "__main__":
    run_exmp059()
