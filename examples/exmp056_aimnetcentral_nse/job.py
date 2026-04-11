#!/usr/bin/env python3
"""Example: AIMNetCentral with NSE (Neural Spin Equilibration) for open-shell systems.

This example demonstrates how to use AIMNet2-NSE model with ORCA ExtOpt interface
for calculating properties of open-shell (radical) systems.

The NSE model supports spin-polarized charges with num_charge_channels=2,
requiring both charge and multiplicity (or spin) to be passed correctly.
"""

from pathlib import Path

# This example shows how to write ORCA input files for AIMNetCentral NSE calculations
# To run actual AIMNetCentral calculations, use the command-line interface:
# python -m opi.external_methods.aimnetcentral.run_aimnetcentral_extopt --model aimnet2nse --mult 2.0

def main() -> None:
    """Write ORCA input files for NSE calculation on a radical system (methyl radical)."""
    working_dir = Path("RUN")
    working_dir.mkdir(exist_ok=True)

    # Create a simple XYZ file for methyl radical (CH3•)
    # Open-shell system with 7 valence electrons (odd count)
    # Charge = 0, Multiplicity = 2 (doublet, S = 1/2)
    xyz_content = """4

C  0.000000  0.000000  0.000000
H  0.000000  0.000000  1.090000
H  1.026739  0.000000 -0.363333
H -0.513370 -0.889181 -0.363333
"""
    xyz_path = working_dir / "inp.xyz"
    xyz_path.write_text(xyz_content)

    # Create ORCA input file
    orca_input = """! extopt pbe def2-svp def2-svpjk

%scf
  maxiter 200
end

%method
  ProgExt "python3"
  Ext_Params "run_aimnetcentral_extopt.py --model aimnet2nse --mult 2.0"
end

* xyz 0 2
C  0.000000  0.000000  0.000000
H  0.000000  0.000000  1.090000
H  1.026739  0.000000 -0.363333
H -0.513370 -0.889181 -0.363333
*
"""
    orca_path = working_dir / "job.inp"
    orca_path.write_text(orca_input)

    print(f"Input files written to {working_dir}")
    print(f"Created: {xyz_path}")
    print(f"Created: {orca_path}")
    print()
    print("To run the calculation:")
    print("  cd RUN && orca job.inp")
    print()
    print("For NSE models (aimnet2nse):")
    print("  - Set 'Mult 2' in ORCA input (or via Ext_Params)")
    print("  - Both charge and multiplicity must be specified correctly")
    print("  - Outputs spin_charges in addition to charges")


if __name__ == "__main__":
    main()
