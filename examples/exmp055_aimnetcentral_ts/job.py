#!/usr/bin/env python3

"""
Example exmp055: Transition State Optimization with AIMNetCentral

This example demonstrates how to perform a transition state (TS) optimization
using ORCA's external methods interface with AIMNetCentral as the calculator.

For TS optimization, ORCA uses:
- `! extopt optts` keyword combination
- The external method wrapper computes gradients (forces) for the TS optimizer
- TS requires at least one imaginary frequency in the final Hessian

Notes
-----
- The wrapper computes gradients which ORCA's TS optimizer uses internally
- Make sure your initial guess has the correct symmetry/constraints for the TS
- After optimization, verify the TS has exactly one imaginary frequency
"""

from pathlib import Path

from opi.core import Calculator
from opi.external_methods import AimnetCentralConfig, create_aimnetcentral_extopt
from opi.input.blocks import BlockGeom
from opi.input.simple_keywords import Task, Opt
from opi.input.structures import Structure


def main() -> None:
    working_dir = Path("RUN_TS")
    working_dir.mkdir(exist_ok=True)

    # > Create calculator
    calc = Calculator(basename="ts_opt", working_dir=working_dir, version_check=False)
    
    # > Read structure from inp.xyz (should be an initial guess near the TS)
    calc.structure = Structure.from_xyz("inp.xyz")
    
    # > For TS optimization, we need to specify opt_type="optts"
    extopt_kw, aimnet_block = create_aimnetcentral_extopt(
        AimnetCentralConfig(
            model="aimnet2_2025",
            device="cuda",
            opt_type="optts",  # Important: set to "optts" for transition state
        ),
        opt_type="optts",  # Also set via create_aimnetcentral_extopt parameter
    )

    # > For TS optimization, use Task.OPT with Opt.OPTTS keyword
    # > ORCA will use %geom ts_search ef for Eigenvector Follow
    calc.input.add_simple_keywords(extopt_kw, Opt.OPTTS)
    
    # > Optional: Add %geom block for TS-specific settings
    # > These can help the TS optimizer converge
    calc.input.add_blocks(
        BlockGeom(
            ts_search="ef",  # Eigenvector Follow for TS search
            maxiter=100,
            trust=0.1,  # Smaller trust radius for TS
            step="rfo",  # Rational Function Optimization
        )
    )
    
    # > Set number of cores
    calc.input.ncores = 4

    # > Write input and run
    calc.write_input()
    print(f"ORCA input written to {working_dir / 'ts_opt.inp'}")
    
    # > To run the actual calculation, uncomment the following:
    # > calc.run()
    
    print("\nExample input for TS optimization:")
    print("=" * 60)
    print(f"! extopt optts")
    print(f"%method")
    print(f"  ProgExt {aimnet_block.ProgExt}")
    print(f"  Ext_Params {aimnet_block.Ext_Params}")
    print(f"end")
    print(f"%geom")
    print(f"  ts_search ef")
    print(f"  maxiter 100")
    print(f"  trust 0.1")
    print(f"  step rfo")
    print(f"end")
    print("=" * 60)
    print("\nAfter running, verify TS by checking for exactly one imaginary frequency.")
    print("Run: orca_job.out for frequency analysis or use ORCA's freq module.")


if __name__ == "__main__":
    main()
