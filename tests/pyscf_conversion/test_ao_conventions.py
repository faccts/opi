from pathlib import Path

import numpy as np
import pytest

from opi.input.blocks import BasisShell, BlockBasis, NewBasis
from opi.output.models.json.gbw._pyscf_converter import _orca_to_pyscf_ao_map
from opi.utils.element import Element
from tests.pyscf_conversion.helpers import run_orca

"""
Test of the table that relates ORCA's and PySCF's basis functions against ORCA's overlap matrix.

This test runs ORCA and is not part of the CI.
"""

pyscf = pytest.importorskip("pyscf", reason="PySCF not installed")
pytestmark = pytest.mark.pyscf


@pytest.mark.orca
@pytest.mark.slow
def test_ao_conventions_reproduce_orca_overlap(tmp_path: Path) -> None:
    """
    ORCA's overlap matrix, transformed to PySCF's basis functions, must equal PySCF's overlap
    matrix. def2-SVP provides the s, p, and d shells, the added shells cover f up to l = 10.
    """
    # > Low-symmetry geometry, so that every function of the added shells overlaps with others
    mol = pyscf.gto.M(atom="O 0 0 0; H 0.61 0.52 0.55; H -0.43 -0.77 0.31", verbose=0)
    # > The exponent differs from def2-SVP's, as nearly linearly dependent shells make
    # > orca_2json fail
    shells = [BasisShell(angmom=letter, primitives=[(1.2, 1.0)]) for letter in "fghiklmn"]
    basis_block = BlockBasis(addgto=NewBasis(element=Element.OXYGEN, shells=shells))
    output = run_orca(tmp_path, mol, "HF RHF def2-svp NoRI", blocks=[basis_block])

    # > The recreated gbw JSON only holds the requested integrals, so the gbw data is read first
    assert output.results_gbw is not None
    gbw = output.results_gbw[0]
    assert gbw.molecule is not None and gbw.molecule.atoms is not None
    mol_converted = gbw.to_pyscf().mol
    ao_map = _orca_to_pyscf_ao_map(gbw.molecule.atoms, mol_converted)
    overlap_orca = output.get_int_overlap(recreate_json=True)
    assert overlap_orca is not None

    # > Transform the rows and the columns of ORCA's overlap matrix
    overlap_converted = ao_map.orca_to_pyscf(ao_map.orca_to_pyscf(overlap_orca).T).T
    np.testing.assert_allclose(
        overlap_converted, mol_converted.intor("int1e_ovlp"), rtol=0.0, atol=1e-7
    )
