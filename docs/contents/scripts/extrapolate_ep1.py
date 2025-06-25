from pathlib import Path
import numpy as np
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
    if output.results_properties.geometries[0].single_point_data.converged:
        print("ORCA terminated normally and the SCF converged")
    else:
        raise RuntimeError("SCF DID NOT CONVERGE")
    
if __name__ == "__main__":
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

    # > Define a basename for the calculation files
    basename = "extrapolate_ep1"

    # > Task 1
    # > Create a Calculator object for ORCA input generation and execution
    calc = Calculator(basename=f"{basename}_1", working_dir=working_dir)

    # > Load the molecular structure from XYZ file
    structure = Structure.from_xyz(xyz_file)
    calc.structure = structure
    calc.structure.charge = 0
    calc.structure.multiplicity = 1

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
    output_1 = calc.get_output()
    check_and_parse_output(output_1)

    # > Task 2
    calc = Calculator(basename=f"{basename}_2", working_dir=working_dir)
    structure = Structure.from_xyz(xyz_file)
    calc.structure = structure
    calc.structure.charge = 0
    calc.structure.multiplicity = 1
    calc.input.add_simple_keywords(
        Wft.CCSD_T,
        Scf.VERYTIGHTSCF,
        BasisSet.CC_PVTZ
    )
    calc.write_input()
    calc.run()
    output_2 = calc.get_output()
    check_and_parse_output(output_2)

    alpha = 4.420  # based on F. Neese et al. JCTC, 7,33-43 (2011)
    beta = 2.460
    X = 2
    Y = 3
    eX = np.exp(-alpha * np.sqrt(X))
    eY = np.exp(-alpha * np.sqrt(Y))

    E0_X = output_1.results_properties.geometries[0].energy[1].refenergy[0][0]
    E0_Y = output_2.results_properties.geometries[0].energy[1].refenergy[0][0]
    E0_CBS = (E0_X * eY - E0_Y * eX) / (eY - eX)

    E_corr_X = output_1.results_properties.geometries[0].energy[1].correnergy[0][0]
    E_corr_Y = output_2.results_properties.geometries[0].energy[1].correnergy[0][0]
    E_corr_CBS = (X ** beta * E_corr_X - Y ** beta * E_corr_Y) / (X ** beta - Y ** beta)

    E_Total_X = output_1.results_properties.geometries[0].energy[1].totalenergy[0][0]
    E_Total_Y = output_2.results_properties.geometries[0].energy[1].totalenergy[0][0]
    E_Total_CSB = E0_CBS + E_corr_CBS

    print({
        "MDCI_Energies": {
            "refEnergy": float(f"{E0_X:.10f}"),
            "corrEnergy": float(f"{E_corr_X:.10f}"),
            "totalEnergy": float(f"{E_Total_X:.10f}")
        }
    })

    print({
        "MDCI_Energies": {
            "refEnergy": float(f"{E0_Y:.10f}"),
            "corrEnergy": float(f"{E_corr_Y:.10f}"),
            "totalEnergy": float(f"{E_Total_Y:.10f}")
        }
    })

    print({
        "CBS_Energies": {
            "refEnergy": float(f"{E0_CBS:.10f}"),
            "corrEnergy": float(f"{E_corr_CBS:.10f}"),
            "totalEnergy": float(f"{E_Total_CSB:.10f}")
        }
    })