from pathlib import Path

import numpy as np
import pytest

from opi.input.blocks import BasisShell, BlockBasis, NewBasis
from opi.output.models.json.gbw.gbw_results import GbwResults
from opi.utils.element import Element
from tests.pyscf_conversion.helpers import run_orca, scf_energy

"""
Tests for the order and sign of basis functions up to l = 10, the maximum of ORCA.

These tests run ORCA and are not part of the CI.
"""

pyscf = pytest.importorskip("pyscf")


@pytest.mark.orca
@pytest.mark.parametrize(
    ("letters", "import_to_orca"),
    [
        # > ORCA flips the sign of the functions with |m| = 3, 4, 7, 8 up to l = 8
        ("hikl", True),
        # > ... and of none for l = 9, 10. orca_2json of ORCA 6.1.1 cannot write gbw files with
        # > such shells, so only the export is checked.
        ("mn", False),
    ],
)
def test_high_angular_momentum(tmp_path: Path, letters: str, import_to_orca: bool) -> None:
    """
    ORCA supports shells up to l = 10. Their functions must be converted with the correct order and
    sign: a wrong sign makes ORCA's orbitals non-orthonormal in PySCF.
    """
    # > Low-symmetry geometry, so that every function of the added shells overlaps with others
    mol = pyscf.gto.M(atom="O 0 0 0; H 0.61 0.52 0.55; H -0.43 -0.77 0.31", verbose=0)
    shells = [BasisShell(angmom=letter, primitives=[(1.2, 1.0)]) for letter in letters]
    basis_block = BlockBasis(addgto=NewBasis(element=Element.OXYGEN, shells=shells))
    output = run_orca(tmp_path, mol, "HF RHF def2-svp NoRI", blocks=[basis_block])

    assert output.results_gbw is not None
    mf = output.results_gbw[0].to_pyscf()
    max_l = max(mf.mol.bas_angular(i) for i in range(mf.mol.nbas))
    assert max_l == "spdfghiklmn".index(letters[-1])
    overlap = mf.mol.intor("int1e_ovlp")
    np.testing.assert_allclose(
        mf.mo_coeff.T @ overlap @ mf.mo_coeff, np.eye(mf.mo_coeff.shape[1]), atol=1e-6
    )
    assert mf.energy_tot() == pytest.approx(scf_energy(output), abs=1e-6)

    if import_to_orca:
        # > PySCF's own SCF orbitals as guess for ORCA
        mf.kernel(dm0=mf.make_rdm1())
        moread_dir = tmp_path / "moread"
        moread_dir.mkdir()
        gbw_file = GbwResults.from_pyscf(mf).to_gbw_file(moread_dir / "guess.gbw")
        output_moread = run_orca(
            moread_dir, mol, "HF RHF def2-svp NoRI", moinp=gbw_file, blocks=[basis_block]
        )
        assert output_moread.get_final_energy() == pytest.approx(mf.e_tot, abs=1e-7)
