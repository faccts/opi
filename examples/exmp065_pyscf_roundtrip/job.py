#!/usr/bin/env python3
"""
Example: Transfer molecular orbitals between ORCA and PySCF.

ORCA -> PySCF:
    `mf = output.results_gbw[0].to_pyscf()` creates a PySCF mean-field object from the gbw data
    of an ORCA calculation. The object holds ORCA's structure, basis set, effective core
    potentials (ECPs), and molecular orbitals, but no SCF has been run with it.

PySCF -> ORCA:
    `GbwResults.from_pyscf(mf).to_gbw_file(gbw_file)` writes PySCF's orbitals into a gbw file,
    which ORCA reads as SCF guess with `MORead`.

The example runs both directions as a round trip: ORCA's Hartree-Fock orbitals of BiH3 are
converted to PySCF, which reproduces ORCA's SCF energy and runs its own SCF. PySCF's orbitals are
then converted back and read by ORCA, whose SCF converges immediately.

Note on the system: bismuth carries an ECP, and its def2-TZVP basis set is augmented by a g, an
f, and an h shell. This is not needed for the conversion. It only makes the example a demanding
test, as high angular momenta and shells that are not sorted by angular momentum are covered.

Requires the optional dependency PySCF (`pip install pyscf`).
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

# > Shells added to the def2-TZVP basis set of bismuth, in this order. They only make the example
# > a harder test of the conversion and can be left out.
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

    # > 2. ORCA -> PySCF: The structure, the basis set, the ECP, and the orbitals are taken from
    # > the gbw data. `results_gbw[0]` is the main gbw file of the calculation.
    # > The returned object is a Hartree-Fock object (`scf.RHF`, `scf.UHF`, or `scf.ROHF`) with
    # > `mo_coeff`, `mo_occ`, and `mo_energy` set. For a DFT calculation, create a Kohn-Sham object
    # > from `mf.mol` yourself and copy these attributes, as the functional is not part of the gbw
    # > data.
    mf = output.results_gbw[0].to_pyscf()
    # > No SCF is needed to evaluate the energy of ORCA's orbitals
    print("PYSCF ENERGY OF ORCA'S ORBITALS")
    print(mf.energy_tot())

    # > Use the object like any other PySCF object, e.g., run an SCF starting from ORCA's orbitals
    mf.conv_tol = 1e-10
    mf.kernel(dm0=mf.make_rdm1())
    print("PYSCF SCF ENERGY")
    print(mf.e_tot)

    # > 3. PySCF -> ORCA: The orbitals of the mean-field object are written into a gbw file.
    # > Other orbitals, e.g., localized ones, can be passed with `mo_coeff` and `mo_occ`.
    # > The second calculation runs in a subfolder. The gbw file has to be created inside that
    # > folder, as ORCA only accepts a `%moinp` file below its own working directory.
    moread_dir = working_dir / "moread"
    moread_dir.mkdir()
    gbw_file = GbwResults.from_pyscf(mf).to_gbw_file(moread_dir / "from_pyscf.gbw")
    # > ORCA reads the gbw file with `MORead` and `%moinp`, see `run_orca()`
    output_moread = run_orca(structure, moread_dir, "job_moread", moinp=gbw_file)
    print("ORCA SCF ENERGY WITH PYSCF'S ORBITALS AS GUESS")
    print(output_moread.get_final_energy())

    return output_moread


if __name__ == "__main__":
    run_exmp065()
