#!/usr/bin/env python3
#!/usr/bin/env python3
import sys
from pathlib import Path

from opi.input.structures import Properties, Structure
from opi.simple_tasks import GoatSettings, GoatTask


def run_exmp060(
    structure: Structure | None = None, working_dir: Path = Path("RUN")
) -> tuple[list[Structure], list[Properties]]:

    # > if no structure is given read structure from inp.xyz
    if structure is None:
        structure = Structure.from_xyz("inp.xyz")

    goat_settings = GoatSettings(goat_maxiter=128, goat_explore=True)
    goat_task = GoatTask("gfn2-xtb", task_settings=goat_settings)

    goat_result = goat_task.run("job", structure, working_dir=working_dir, ncores=4)

    # > check if the ORCA calculation terminated normally
    if not goat_result.status:
        print("GOAT task failed")
        sys.exit(1)

    structures, properties_list = goat_result.primary_property

    # > Print structures that were read
    for structure, properties in zip(structures, properties_list):
        print(f"FINAL ENERGY: {properties.energy_total}")
        print(structure.to_xyz_block())

    return structures, properties_list


if __name__ == "__main__":
    run_exmp060()
