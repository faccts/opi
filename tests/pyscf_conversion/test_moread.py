from pathlib import Path

import pytest

from opi.output.models.json.gbw.gbw_results import GbwResults
from tests.pyscf_conversion.helpers import WATER, run_orca

"""
Tests for reading PySCF's orbitals in ORCA: PySCF -> gbw file -> ORCA `MORead`.

These tests run ORCA and are not part of the CI.
"""

pyscf = pytest.importorskip("pyscf", reason="PySCF not installed")
pytestmark = pytest.mark.pyscf


@pytest.mark.orca
@pytest.mark.parametrize(
    ("atom", "basis", "spin", "method"),
    [
        # > ECP and general contractions
        ("H 0 0 0; I 0 0 1.61", "def2-svp", 0, "RHF"),
        (WATER, "cc-pvdz", 0, "RHF"),
        # > g functions
        (WATER, "def2-qzvp", 0, "RHF"),
        # > h functions, whose |m| = 5 functions do not change sign, unlike |m| = 3, 4
        (WATER, "cc-pv5z", 0, "RHF"),
        ("O 0 0 0; H 0 0 0.97", "def2-tzvp", 1, "UHF"),
        ("O 0 0 0; H 0 0 0.97", "def2-svp", 1, "ROHF"),
    ],
)
def test_from_pyscf_orca_moread(
    tmp_path: Path, atom: str, basis: str, spin: int, method: str
) -> None:
    """ORCA must accept converged orbitals of PySCF as converged guess."""
    mol = pyscf.gto.M(atom=atom, basis=basis, ecp=basis, spin=spin, verbose=0)
    mf = getattr(pyscf.scf, method)(mol).run(conv_tol=1e-11)
    gbw_file = GbwResults.from_pyscf(mf).to_gbw_file(tmp_path / "guess.gbw")

    output = run_orca(tmp_path, mol, f"HF {method} {basis}", moinp=gbw_file)

    assert output.get_final_energy() == pytest.approx(mf.e_tot, abs=1e-7)


@pytest.mark.orca
@pytest.mark.parametrize(("pyscf_method", "orca_method"), [("RHF", "UHF"), ("UHF", "RHF")])
def test_from_pyscf_orca_moread_other_hf_type(
    tmp_path: Path, pyscf_method: str, orca_method: str
) -> None:
    """ORCA must accept restricted orbitals as guess of an unrestricted calculation and vice versa."""
    mol = pyscf.gto.M(atom=WATER, basis="def2-svp", verbose=0)
    mf = getattr(pyscf.scf, pyscf_method)(mol).run(conv_tol=1e-11)
    gbw_file = GbwResults.from_pyscf(mf).to_gbw_file(tmp_path / "guess.gbw")

    output = run_orca(tmp_path, mol, f"HF {orca_method} def2-svp NoRI", moinp=gbw_file)

    assert output.get_final_energy() == pytest.approx(mf.e_tot, abs=1e-7)
