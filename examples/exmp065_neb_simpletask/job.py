#!/usr/bin/env python3
import sys
from pathlib import Path

from opi.input.structures import Structure
from opi.simple_tasks import NebResults, NebSettings, NebTask
from opi.utils.units import AU_TO_KCAL


def run_exmp065(
    reactant: Structure | None = None,
    product: Structure | None = None,
    working_dir: Path = Path("RUN"),
) -> NebResults:
    example_folder = Path(__file__).parent

    # > if no structures are given read them from reac.xyz and prod.xyz
    if reactant is None:
        reactant = Structure.from_xyz(example_folder / "reac.xyz")
    if product is None:
        product = Structure.from_xyz(example_folder / "prod.xyz")

    # > set up the task: climbing-image NEB with 8 images between the endpoints,
    # > which are optimized first
    neb_task = NebTask("gfn2-xtb", task_settings=NebSettings(nimages=8, preopt_ends=True))

    # > the product is given per run, since it belongs to the reaction and not to the task
    neb_result = neb_task.run("job", reactant, product=product, working_dir=working_dir)

    # > check if the ORCA calculation terminated normally and the NEB converged
    if not neb_result.status:
        print("NEB task failed")
        sys.exit(1)

    # > the minimal energy pathway as list of structures and list of energies
    structures, energies = neb_result.primary_property

    print("Minimal energy pathway relative to the reactant:")
    for image, energy in enumerate(energies):
        print(f"IMAGE {image:2d}: {(energy - energies[0]) * AU_TO_KCAL:8.2f} kcal/mol")

    # > the highest image approximates the transition state
    barrier = (neb_result.highest_energy - energies[0]) * AU_TO_KCAL
    print(f"Highest image: {neb_result.highest_image_index} ({barrier:.2f} kcal/mol)")
    print(neb_result.highest_structure.to_xyz_block())

    return neb_result


if __name__ == "__main__":
    run_exmp065()
