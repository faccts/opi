#!/usr/bin/env python3
import sys
from pathlib import Path

from opi.input.structures import Structure
from opi.output.ir_mode import IrMode
from opi.simple_tasks import FreqResults, FreqTask


def run_exmp061(structure: Structure | None = None, working_dir: Path = Path("RUN")) -> FreqResults:
    # > if no structure is given read structure from inp.xyz
    if structure is None:
        structure = Structure.from_xyz("inp.xyz")

    freq_task = FreqTask(method="tpss", basis_set="def2-svp")
    freq_result = freq_task.run("job", structure, working_dir=working_dir)

    if not freq_result.status:
        print(f"Freq task failed, see output file: {freq_result.output.get_outfile()}")
        sys.exit(1)

    output = freq_result.output

    ir_dict = output.get_ir()
    print(IrMode.header())
    for ir_mode in ir_dict.values():
        print(ir_mode)

    ngeoms = len(output.results_properties.geometries)
    print("N GEOMETRIES")
    print(ngeoms)
    print("FINAL SINGLE POINT ENERGY")
    print(output.get_final_energy())
    print("Temperature [K]")
    print(output.results_properties.geometries[0].thermochemistry_energies[0].temperature)
    print("Final Gibbs free energy")
    print(output.get_free_energy())
    print("Zero-point energy")
    print(output.get_zpe())
    print("Final enthalpy H")
    print(output.get_enthalpy())
    print("Final entropy S")
    print(output.get_entropy())
    print("G-E(el)")
    print(freq_result.free_energy_delta)

    return freq_result


if __name__ == "__main__":
    run_exmp061()
