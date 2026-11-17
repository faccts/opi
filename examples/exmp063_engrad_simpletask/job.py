#!/usr/bin/env python3
import sys
from pathlib import Path

from opi.input.structures import Structure
from opi.simple_tasks import EngradResults, EngradTask


def run_exmp063(
    structure: Structure | None = None, working_dir: Path = Path("RUN")
) -> EngradResults:
    # > if no structure is given read structure from inp.xyz
    if structure is None:
        structure = Structure.from_xyz("inp.xyz")

    engrad_task = EngradTask(method="r2scan-3c")
    engrad_result = engrad_task.run("job", structure, working_dir=working_dir)

    if not engrad_result.status:
        print(f"Engrad task failed, see output file: {engrad_result.output.get_outfile()}")
        sys.exit(1)

    print("FINAL SINGLE POINT ENERGY")
    print(engrad_result.final_energy)
    print("SCF ENERGY")
    print(engrad_result.output.get_energies()["SCF"])

    return engrad_result


if __name__ == "__main__":
    run_exmp063()
