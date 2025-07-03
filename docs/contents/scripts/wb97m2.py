from pathlib import Path
from opi.core import Calculator
from opi.output.core import Output
from opi.input.structures.structure import Structure
from opi.input.simple_keywords import BasisSet, AuxBasisSet, DispersionCorrection, Dft, Grid, Scf
from opi.input.blocks import BlockBasis, BlockMp2, BlockScf


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
    basename = "wB97M2"

    # > Task 1
    # > Create a Calculator object for ORCA input generation and execution
    calc = Calculator(basename=f"{basename}_scf", working_dir=working_dir)
    
    # > Load the molecular structure from XYZ file
    structure = Structure.from_xyz(xyz_file)
    calc.structure = structure
    calc.structure.charge = 0
    calc.structure.multiplicity = 1

    # > Add calculation keywords and blocks
    calc.input.add_simple_keywords(
        Dft.WB97M_V,
        DispersionCorrection.SCNL,
        Grid.DEFGRID2,
    )
    calc.input.add_blocks(
        BlockBasis(basis=BasisSet.DEF2_TZVP, auxj=AuxBasisSet.DEF2_J)
    )

    # > Write the ORCA input file
    calc.write_input()
    # > Run the ORCA calculation
    calc.run()
    # > Get the output object
    output_scf = calc.get_output()
    check_and_parse_output(output_scf)

    # > Task 2
    calc = Calculator(basename=f"{basename}_mp2", working_dir=working_dir)
    calc.structure = structure
    calc.structure.charge = 0
    calc.structure.multiplicity = 1
    calc.input.add_simple_keywords(
        Dft.WB97M_2,
        DispersionCorrection.SCNL,
        Grid.DEFGRID2,
        Scf.NOITER,
        Scf.CALCGUESSENERGY,
        Scf.MOREAD
    )
    calc.input.add_blocks(
        BlockBasis(basis=BasisSet.DEF2_TZVP, auxc=AuxBasisSet.DEF2_TZVP_C, auxj=AuxBasisSet.DEF2_J),
        BlockScf(ignoreconv=1),
        BlockMp2(ri=True)
    )
    calc.input.add_arbitrary_string('%moinp "wB97M2_scf.gbw"')
    # calc.input.moinp = working_dir / "wB97M2_scf.gbw"
    calc.write_input()
    calc.run()
    output_mp2 = calc.get_output()
    check_and_parse_output(output_mp2)

    E_Total_wB97MV = output_scf.results_properties.geometries[0].energy[0].totalenergy[0][0]
    E_Total_wB97M2 = output_mp2.results_properties.geometries[0].energy[1].totalenergy[0][0]

    print({
        "ωB97M-V/def2-TZVP": {
            "totalEnergy": float(f"{E_Total_wB97MV:.10f}")
        }
    })

    print({
        "ωB97M(2)/def2-TZVP": {
            "totalEnergy": float(f"{E_Total_wB97M2:.10f}")
        }
    })