from pathlib import Path
import pandas as pd
from opi.core import Calculator
from opi.output.core import Output
from opi.input.structures.structure import Structure
from opi.input.simple_keywords import Wft, Scf, BasisSet, Dlpno, AuxBasisSet
from opi.input.blocks import BlockMdci


def check_and_parse_output(output: Output) -> None:
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
    basename = "extrapolate_CPS_CBS"

    # > Task 1
    # > Create a Calculator object for ORCA input generation and execution
    calc = Calculator(basename=f"{basename}_1", working_dir=working_dir)

    # > Load the molecular structure from XYZ file
    structure = Structure.from_xyz(xyz_file)
    calc.structure = structure
    calc.structure.multiplicity = 1
    calc.structure.charge = 0

    # > Add calculation keywords and blocks
    calc.input.add_simple_keywords(
        Wft.DLPNO_CCSD_T1,
        BasisSet.AUG_CC_PVTZ,
        Scf.VERYTIGHTSCF,
        Dlpno.TIGHTPNO,
        AuxBasisSet.AUG_CC_PVQZ_C
    )
    calc.input.add_blocks(
        BlockMdci(tcutpno=1e-6, printlevel=3),
    )
    calc.input.add_arbitrary_string('%BASIS auxc "autoaux" autoauxlmax true End')

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
    calc.structure.multiplicity = 1
    calc.structure.charge = 0
    calc.input.add_simple_keywords(
        Wft.DLPNO_CCSD_T1,
        BasisSet.AUG_CC_PVTZ,
        Scf.VERYTIGHTSCF,
        Dlpno.TIGHTPNO,
        AuxBasisSet.AUG_CC_PVQZ_C
    )
    calc.input.add_blocks(
        BlockMdci(tcutpno=1e-7, printlevel=3),
    )
    calc.input.add_arbitrary_string('%BASIS auxc "autoaux" autoauxlmax true End')
    calc.write_input()
    calc.run()
    output_2 = calc.get_output()
    check_and_parse_output(output_2)

    # > Task 3
    calc = Calculator(basename=f"{basename}_3", working_dir=working_dir)
    structure = Structure.from_xyz(xyz_file)
    calc.structure = structure
    calc.structure.multiplicity = 1
    calc.structure.charge = 0
    calc.input.add_simple_keywords(
        Wft.DLPNO_CCSD_T1,
        BasisSet.AUG_CC_PVQZ,
        Scf.VERYTIGHTSCF,
        Dlpno.TIGHTPNO,
        AuxBasisSet.AUG_CC_PV5Z_C
    )
    calc.input.add_blocks(
        BlockMdci(tcutpno=1e-6, printlevel=3),
    )
    calc.input.add_arbitrary_string('%BASIS auxc "autoaux" autoauxlmax true End')
    calc.write_input()
    calc.run()
    output_3 = calc.get_output()
    check_and_parse_output(output_3)

    # > Task 4
    calc = Calculator(basename=f"{basename}_4", working_dir=working_dir)
    structure = Structure.from_xyz(xyz_file)
    calc.structure = structure
    calc.structure.multiplicity = 1
    calc.structure.charge = 0
    calc.input.add_simple_keywords(
        Wft.DLPNO_CCSD_T1,
        BasisSet.AUG_CC_PVQZ,
        Scf.VERYTIGHTSCF,
        Dlpno.TIGHTPNO,
        AuxBasisSet.AUG_CC_PV5Z_C
    )
    calc.input.add_blocks(
        BlockMdci(tcutpno=1e-7, printlevel=3),
    )
    calc.input.add_arbitrary_string('%BASIS auxc "autoaux" autoauxlmax true End')
    calc.write_input()
    calc.run()
    output_4 = calc.get_output()
    check_and_parse_output(output_4)

    F_CPS = 1.5
    X = 3
    Y = 4
    F_0 = 1.301304
    F_corr = 1.711889

    E0_X = output_1.results_properties.geometries[0].energy[1].refenergy[0][0]
    E0_Y = output_3.results_properties.geometries[0].energy[1].refenergy[0][0]
    E0_CBS = E0_X + F_0 * (E0_Y - E0_X)

    E_corr_X_Loose = output_1.results_properties.geometries[0].energy[1].correnergy[0][0]
    E_corr_X_Tight = output_2.results_properties.geometries[0].energy[1].correnergy[0][0]
    E_corr_Y_Loose = output_3.results_properties.geometries[0].energy[1].correnergy[0][0]
    E_corr_Y_Tight = output_4.results_properties.geometries[0].energy[1].correnergy[0][0]
    E_corr_CBS_Loose = E_corr_X_Loose + F_corr * (E_corr_Y_Loose - E_corr_X_Loose)
    E_corr_CBS_Tight = E_corr_X_Tight + F_corr * (E_corr_Y_Tight - E_corr_X_Tight)
    E_corr_X = E_corr_X_Loose + F_CPS * (E_corr_X_Tight - E_corr_X_Loose)
    E_corr_Y = E_corr_Y_Loose + F_CPS * (E_corr_Y_Tight - E_corr_Y_Loose)
    E_corr_CBS_CPS = E_corr_CBS_Loose + F_CPS * (E_corr_CBS_Tight - E_corr_CBS_Loose)

    E_Total_X_Loose = output_1.results_properties.geometries[0].energy[1].totalenergy[0][0]
    E_Total_X_Tight = output_2.results_properties.geometries[0].energy[1].totalenergy[0][0]
    E_Total_Y_Loose = output_3.results_properties.geometries[0].energy[1].totalenergy[0][0]
    E_Total_Y_Tight = output_4.results_properties.geometries[0].energy[1].totalenergy[0][0]
    E_Total_Loose_CBS = E0_CBS + E_corr_CBS_Loose
    E_Total_Tight_CBS = E0_CBS + E_corr_CBS_Tight
    E_Total_X_CPS = E0_X + E_corr_X
    E_Total_Y_CPS = E0_Y + E_corr_Y
    E_Total_CBS_CPS = E0_CBS + E_corr_CBS_CPS

    rows = [
        ("SCF Energy", "-",
        f"{E0_X:.15f}", f"{E0_Y:.15f}", f"{E0_CBS:.15f}"),
        ("Correlation Energy", "TCutPNO = 1e-6",
        f"{E_corr_X_Loose:.8f}", f"{E_corr_Y_Loose:.8f}", f"{E_corr_CBS_Loose:.8f}"),
        ("Correlation Energy", "TCutPNO = 1e-7",
        f"{E_corr_X_Tight:.8f}", f"{E_corr_Y_Tight:.8f}", f"{E_corr_CBS_Tight:.8f}"),
        ("Correlation Energy", "CPS(6/7)",
        f"{E_corr_X:.8f}", f"{E_corr_Y:.8f}", f"{E_corr_CBS_CPS:.8f}"),
        ("Total Energy", "TCutPNO = 1e-6",
        f"{E_Total_X_Loose:.8f}", f"{E_Total_Y_Loose:.8f}", f"{E_Total_Loose_CBS:.8f}"),
        ("Total Energy", "TCutPNO = 1e-7",
        f"{E_Total_X_Tight:.8f}", f"{E_Total_Y_Tight:.8f}", f"{E_Total_Tight_CBS:.8f}"),
        ("Total Energy", "CPS(6/7)",
        f"{E_Total_X_CPS:.8f}", f"{E_Total_Y_CPS:.8f}", f"{E_Total_CBS_CPS:.8f}"),
    ]

    df = pd.DataFrame(rows, columns=[
        "Energy Types", "TCut Levels", "aug-cc-pVDZ", "aug-cc-pVTZ", "CBS(3/4)"
    ])
    df.set_index(["Energy Types", "TCut Levels"], inplace=True)
    print(df)