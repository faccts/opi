from pathlib import Path

import pytest

from opi.output.models.json.gbw.gbw_results import GbwResults
from tests.pyscf_conversion.helpers import run_orca, scf_energy

"""
Tests for transferring orbitals of an X2C calculation between ORCA and PySCF.

These tests run ORCA and are not part of the CI.
"""

pyscf = pytest.importorskip("pyscf")


@pytest.mark.orca
def test_x2c(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    ORCA's X2C is reproduced by PySCF's X2C with ORCA's speed of light, in both directions. The
    Hamiltonian itself is not part of the gbw data.
    """
    monkeypatch.setattr(pyscf.lib.param, "LIGHT_SPEED", 137.0359895)
    mol = pyscf.gto.M(atom="H 0 0 0; I 0 0 1.61", verbose=0)
    output = run_orca(tmp_path, mol, "HF RHF X2C x2c-svpall NoRI")

    # > ORCA -> PySCF
    assert output.results_gbw is not None
    mf = output.results_gbw[0].to_pyscf().x2c()
    assert mf.energy_tot() == pytest.approx(scf_energy(output), abs=1e-6)

    # > PySCF -> ORCA
    mf.kernel(dm0=mf.make_rdm1())
    moread_dir = tmp_path / "moread"
    moread_dir.mkdir()
    with pytest.warns(UserWarning, match="relativistic"):
        results = GbwResults.from_pyscf(mf)
    gbw_file = results.to_gbw_file(moread_dir / "guess.gbw")
    output_moread = run_orca(moread_dir, mol, "HF RHF X2C x2c-svpall NoRI", moinp=gbw_file)
    assert output_moread.get_final_energy() == pytest.approx(mf.e_tot, abs=1e-7)
