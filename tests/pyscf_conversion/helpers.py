"""
Helpers for the tests that check the conversion between ORCA and PySCF with real ORCA runs.
"""

from collections.abc import Sequence
from pathlib import Path
from typing import Any

from opi.core import Calculator
from opi.input.blocks import BlockABC, BlockScf
from opi.input.simple_keywords import ORCAKeyword, Scf
from opi.input.structures import Structure
from opi.output.core import Output

WATER = "O 0 0 0; H 0 0.757 0.587; H 0 -0.757 0.587"


def run_orca(
    tmp_path: Path,
    mol: Any,
    keywords: str,
    *,
    moinp: Path | None = None,
    blocks: Sequence[BlockABC] = (),
) -> Output:
    """Run a single point with ORCA for a PySCF molecule."""
    xyz = "\n".join(
        f"{mol.atom_pure_symbol(i)} {x:.10f} {y:.10f} {z:.10f}"
        for i, (x, y, z) in enumerate(mol.atom_coords(unit="Angstrom"))
    )
    (tmp_path / "inp.xyz").write_text(f"{mol.natm}\n\n{xyz}\n")
    structure = Structure.from_xyz(tmp_path / "inp.xyz")
    structure.charge = mol.charge
    structure.multiplicity = mol.spin + 1

    calc = Calculator(basename="job", working_dir=tmp_path)
    calc.structure = structure
    # > Simple keywords are written before the blocks. Otherwise, a basis set keyword would
    # > replace shells added in a `%basis` block.
    calc.input.add_simple_keywords(Scf.NOAUTOSTART, Scf.VERYTIGHTSCF)
    calc.input.add_simple_keywords(
        *(ORCAKeyword(word) for word in f"{keywords} NoFrozenCore".split())
    )
    calc.input.add_blocks(*blocks)
    if moinp is not None:
        calc.input.add_simple_keywords(Scf.MOREAD)
        # > A wrong guess would not converge within two iterations
        calc.input.add_blocks(BlockScf(maxiter=2))
        calc.input.moinp = moinp
    calc.write_and_run()

    output = calc.get_output()
    output.parse()
    assert output.terminated_normally()
    assert output.scf_converged()
    return output


def scf_energy(output: Output) -> float:
    """SCF energy as written by ORCA into the property JSON."""
    assert output.results_properties is not None
    geometry = output.results_properties.geometries[-1]
    energy = next(e for e in geometry.energy if e.method == "SCF")
    return float(energy.totalenergy[0][0])
