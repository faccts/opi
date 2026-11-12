#!/usr/bin/env python3
"""
Example: Round trip of a heavy-element wavefunction between ORCA and PySCF.

A Hartree-Fock calculation on BiH3 is run with ORCA. Bismuth carries an effective core potential
(ECP) and the def2-TZVP basis set, augmented by a g, an f, and an h shell via `%basis AddGTO`.
The added shells come after the f shells of def2-TZVP, so the shells of bismuth are not sorted by
angular momentum. This makes the example a demanding test of the conversion.

1. `Output.get_pyscf_scf()` converts ORCA's orbitals into a PySCF mean-field object, which
   reproduces ORCA's SCF energy.
2. PySCF runs its own SCF starting from ORCA's orbitals.
3. `GbwResults.from_pyscf()` converts PySCF's orbitals back into gbw data, which is written into a
   gbw file and read by ORCA as SCF guess (`MORead`). As the orbitals are converged, ORCA's SCF
   converges immediately.

Requires the optional dependency PySCF (`pip install orca-pi[pyscf]`).
"""

import shutil
import sys
from pathlib import Path

from opi.core import Calculator
from opi.input.blocks import BasisShell, BlockBasis, NewBasis
from opi.input.simple_keywords import Approximation, BasisSet, Method, Scf, Task
from opi.input.structures import Structure
from opi.output.core import Output
from opi.output.models.json.gbw.gbw_results import GbwResults
from opi.utils.element import Element

# > Shells added to the def2-TZVP basis set of bismuth, in this order
ADDED_SHELLS = [
    BasisShell(angmom="g", primitives=[(0.4203, 1.0)]),
    BasisShell(angmom="f", primitives=[(1.26256, 1.0)]),
    BasisShell(angmom="h", primitives=[(0.5, 1.0)]),
]


def run_orca(structure: Structure, working_dir: Path, basename: str, moinp: Path | None) -> Output:
    """Run a Hartree-Fock single point with ORCA, optionally with an SCF guess from `moinp`."""
    calc = Calculator(basename=basename, working_dir=working_dir)
    calc.structure = structure
    calc.input.add_simple_keywords(
        Scf.NOAUTOSTART,
        Method.HF,
        BasisSet.DEF2_TZVP,
        Approximation.NORI,
        Scf.VERYTIGHTSCF,
        Task.SP,
    )
    calc.input.add_blocks(BlockBasis(addgto=NewBasis(element=Element.BISMUTH, shells=ADDED_SHELLS)))
    if moinp is not None:
        calc.input.add_simple_keywords(Scf.MOREAD)
        calc.input.moinp = moinp
    calc.input.ncores = 4

    calc.write_input()
    calc.run()

    output = calc.get_output()
    if not output.terminated_normally():
        print(f"ORCA calculation failed, see output file: {output.get_outfile()}")
        print(output.error_message())
        sys.exit(1)
    # << END OF IF

    # > Parse JSON files
    output.parse()
    return output


def run_exmp065(
    structure: Structure | None = None, working_dir: Path | None = Path("RUN")
) -> Output:
    # > recreate the working dir
    shutil.rmtree(working_dir, ignore_errors=True)
    working_dir.mkdir()

    # > if no structure is given read structure from inp.xyz
    if structure is None:
        structure = Structure.from_xyz("inp.xyz")

    # > 1. ORCA calculation
    output = run_orca(structure, working_dir, "job", moinp=None)
    print("ORCA SCF ENERGY")
    print(output.get_final_energy())

    # > 2. ORCA -> PySCF: The basis set, the ECP, and the orbitals are taken from the gbw file
    mf = output.get_pyscf_scf()
    print("PYSCF ENERGY OF ORCA'S ORBITALS")
    print(mf.energy_tot())

    # > Run PySCF's SCF starting from ORCA's orbitals
    mf.conv_tol = 1e-10
    mf.kernel(dm0=mf.make_rdm1())
    print("PYSCF SCF ENERGY")
    print(mf.e_tot)

    # > 3. PySCF -> ORCA: The second calculation runs in a subfolder. The gbw file has to be
    # > created inside that folder, as ORCA only accepts a `%moinp` file below its own working
    # > directory.
    moread_dir = working_dir / "moread"
    moread_dir.mkdir()
    gbw_file = GbwResults.from_pyscf(mf).to_gbw_file(moread_dir / "from_pyscf.gbw")
    output_moread = run_orca(structure, moread_dir, "job_moread", moinp=gbw_file)
    print("ORCA SCF ENERGY WITH PYSCF'S ORBITALS AS GUESS")
    print(output_moread.get_final_energy())

    return output_moread


if __name__ == "__main__":
    run_exmp065()
