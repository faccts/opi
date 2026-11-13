from pathlib import Path

import numpy as np
import pytest

from tests.pyscf_conversion.helpers import WATER, run_orca, scf_energy

"""
Tests for converting ORCA's orbitals to PySCF for different wavefunction types and ECPs.

These tests run ORCA and are not part of the CI.
"""

pyscf = pytest.importorskip("pyscf", reason="PySCF not installed")
pytestmark = pytest.mark.pyscf


@pytest.mark.orca
def test_to_pyscf_ecp_energy(tmp_path: Path) -> None:
    """PySCF must reproduce ORCA's Hartree-Fock energy of a molecule with an ECP."""
    mol = pyscf.gto.M(atom="H 0 0 0; I 0 0 1.61", verbose=0)
    output = run_orca(tmp_path, mol, "HF RHF def2-svp")

    assert output.results_gbw is not None
    mf = output.results_gbw[0].to_pyscf()

    assert mf.mol.atom_nelec_core(1) == 28
    assert mf.energy_tot() == pytest.approx(scf_energy(output), abs=1e-6)


@pytest.mark.orca
@pytest.mark.parametrize(
    ("atom", "spin", "method"),
    [(WATER, 0, "RHF"), (WATER, 0, "UHF"), ("O 0 0 0; H 0 0 0.97", 1, "UHF")],
)
def test_to_pyscf_hf_types(tmp_path: Path, atom: str, spin: int, method: str) -> None:
    """PySCF must reproduce ORCA's Hartree-Fock energy for restricted and unrestricted orbitals."""
    mol = pyscf.gto.M(atom=atom, spin=spin, verbose=0)
    output = run_orca(tmp_path, mol, f"HF {method} def2-svp NoRI")

    assert output.results_gbw is not None
    mf = output.results_gbw[0].to_pyscf()

    assert type(mf).__name__ == method
    assert mf.energy_tot() == pytest.approx(scf_energy(output), abs=1e-6)


@pytest.mark.orca
def test_to_pyscf_rohf_fractional_occupations(tmp_path: Path) -> None:
    """
    ORCA's ROHF averages the occupation of the degenerate pi orbitals of OH (1.5 each). PySCF's
    ROHF cannot represent this, so integer occupations are used and a warning is issued.
    """
    mol = pyscf.gto.M(atom="O 0 0 0; H 0 0 0.97", spin=1, verbose=0)
    output = run_orca(tmp_path, mol, "HF ROHF def2-svp NoRI")
    assert output.results_gbw is not None
    results = output.results_gbw[0]
    assert results.molecule is not None and results.molecule.molecularorbitals is not None
    orca_occupations = [mo.occupancy for mo in results.molecule.molecularorbitals.mos or []]
    # > Ensure the test keeps covering fractional occupations
    assert 1.5 in orca_occupations

    with pytest.warns(UserWarning, match="fractional occupation numbers"):
        mf = results.to_pyscf()

    assert set(mf.mo_occ) <= {0.0, 1.0, 2.0}
    assert mf.mo_occ.sum() == mf.mol.nelectron
    overlap = mf.mol.intor("int1e_ovlp")
    np.testing.assert_allclose(
        mf.mo_coeff.T @ overlap @ mf.mo_coeff, np.eye(mf.mo_coeff.shape[1]), atol=1e-6
    )
