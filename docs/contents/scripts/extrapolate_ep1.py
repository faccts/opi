from pathlib import Path
import numpy as np
from typing import Any
from opi.core import Calculator
from opi.output.core import Output
from opi.input.structures.structure import Structure
from opi.input.simple_keywords import Scf, Wft, BasisSet


def check_and_parse_output(output: Output)-> None:
    # > Check for proper termination of ORCA
    status = output.terminated_normally()
    if not status:
        # > ORCA did not terminate normally
        raise RuntimeError(f"ORCA did not terminate normally, see output file: {output.get_outfile()}")
    else:
        # > ORCA did terminate normally so we can parse the output
        output.parse()

    # Now check for convergence of the SCF
    if not output.results_properties.geometries[0].single_point_data.converged:
        raise RuntimeError("SCF DID NOT CONVERGE")
    
def extrapolation_ep1(structure: Structure, basename : str = "job", working_dir: Path = Path("RUN"), charge = 0, mult = 1) -> dict[str, Any]:
    # > Task 1: Small basis (X=2) CCSD(T) calculation
    # > Create a Calculator object for ORCA input generation and execution
    calc = Calculator(basename=f"{basename}_X", working_dir=working_dir)

    calc.structure = structure
    calc.structure.charge = charge
    calc.structure.multiplicity = mult

    # > Add calculation keywords
    calc.input.add_simple_keywords(
        Wft.CCSD_T,
        Scf.VERYTIGHTSCF,
        BasisSet.CC_PVDZ
        )
    
    # > Write the ORCA input file
    calc.write_input()
    # > Run the ORCA calculation
    calc.run()
    # > Get the output object
    output_X = calc.get_output()
    check_and_parse_output(output_X)

    # > Task 2: Medium basis (X=3) CCSD(T) calculation
    calc = Calculator(basename=f"{basename}_Y", working_dir=working_dir)
    calc.structure = structure
    calc.structure.charge = charge
    calc.structure.multiplicity = mult
    calc.input.add_simple_keywords(
        Wft.CCSD_T,
        Scf.VERYTIGHTSCF,
        BasisSet.CC_PVTZ
    )
    calc.write_input()
    calc.run()
    output_Y = calc.get_output()
    check_and_parse_output(output_Y)

    alpha = 4.420  # based on F. Neese et al. JCTC, 7,33-43 (2011)
    beta = 2.460
    X = 2
    Y = 3
    eX = np.exp(-alpha * np.sqrt(X))
    eY = np.exp(-alpha * np.sqrt(Y))

    E0_X = output_X.results_properties.geometries[0].energy[1].refenergy[0][0]
    E0_Y = output_Y.results_properties.geometries[0].energy[1].refenergy[0][0]
    E0_CBS = (E0_X * eY - E0_Y * eX) / (eY - eX)

    E_corr_X = output_X.results_properties.geometries[0].energy[1].correnergy[0][0]
    E_corr_Y = output_Y.results_properties.geometries[0].energy[1].correnergy[0][0]
    E_corr_CBS = (X ** beta * E_corr_X - Y ** beta * E_corr_Y) / (X ** beta - Y ** beta)

    E_Total_X = output_X.results_properties.geometries[0].energy[1].totalenergy[0][0]
    E_Total_Y = output_Y.results_properties.geometries[0].energy[1].totalenergy[0][0]
    E_Total_CSB = E0_CBS + E_corr_CBS

    result = {
        "CCSD(T)/cc-pVDZ": {
            "refEnergy": float(f"{E0_X:.10f}"),
            "corrEnergy": float(f"{E_corr_X:.10f}"),
            "totalEnergy": float(f"{E_Total_X:.10f}")
        },
        "CCSD(T)/cc-pVTZ": {
            "refEnergy": float(f"{E0_Y:.10f}"),
            "corrEnergy": float(f"{E_corr_Y:.10f}"),
            "totalEnergy": float(f"{E_Total_Y:.10f}")
        },
        "CCSD(T)/CBS(cc-pVDZ/cc-pVTZ)": {
            "refEnergy": float(f"{E0_CBS:.10f}"),
            "corrEnergy": float(f"{E_corr_CBS:.10f}"),
            "totalEnergy": float(f"{E_Total_CSB:.10f}")
        }
    }

    return result

if __name__ == "__main__":
    # > Define a basename for the calculation files
    basename = "extrapolate_ep1"
    # > Create a working directory and XYZ file
    # > You can replace everything up to the next comment with your own directory or file
    working_dir = Path("RUN")
    working_dir.mkdir(exist_ok=True)

    xyz_data = """\
    3

    O         -3.56626        1.77639        0.00000
    H         -2.59626        1.77639        0.00000
    H         -3.88959        1.36040       -0.81444
    """
    xyz_file = working_dir / "struc.xyz"
    with open(xyz_file, "w") as f:
        f.write(xyz_data)

    # > Load the molecular structure from XYZ file
    structure = Structure.from_xyz(xyz_file)

    # > Run the extrapolation
    result = extrapolation_ep1(structure, basename, working_dir)

    # > Print the results
    for method, energies in result.items():
        print(f"\nMethod: {method}")
        for key, value in energies.items():
            print(f"  {key}: {value}")