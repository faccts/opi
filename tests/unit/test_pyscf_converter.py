from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from opi.output.core import Output
from opi.output.models.json.gbw.gbw_results import GbwResults

"""
Tests for the conversion of gbw data from and to PySCF.

The unit tests check the conversion against the committed JSON fixtures of real ORCA runs, e.g., by
reproducing ORCA's SCF energy with PySCF. The tests marked with `orca` additionally check the
conversion from PySCF to ORCA by reading PySCF's orbitals with ORCA.
"""

pyscf = pytest.importorskip("pyscf")


def gbw_fixtures(json_dir: Path) -> list[Path]:
    """All gbw-JSON fixtures that hold a basis set and molecular orbitals."""
    files = []
    for json_file in sorted(json_dir.glob("gbw/*.json")):
        molecule = GbwResults.from_json_file(json_file).molecule
        if molecule is not None and molecule.atoms and molecule.atoms[0].basis:
            files.append(json_file)
    return files


def scf_energy(output: Output) -> float:
    """SCF energy as written by ORCA into the property JSON."""
    assert output.results_properties is not None
    geometry = output.results_properties.geometries[-1]
    energy = next(e for e in geometry.energy if e.method == "SCF")
    return float(energy.totalenergy[0][0])


def mo_matrices(mf: Any) -> list[np.ndarray]:
    """Molecular orbitals of a mean-field object as list of matrices (one per spin)."""
    mo_coeff = np.asarray(mf.mo_coeff)
    return list(mo_coeff) if mo_coeff.ndim == 3 else [mo_coeff]


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["mp2", "roci"])
def test_to_pyscf_reproduces_hf_energy(
    output_object_factory: Callable[[str], Output], task: str
) -> None:
    """
    PySCF must reproduce ORCA's Hartree-Fock energy from ORCA's orbitals. This checks the basis
    set, the order and sign of the basis functions (including f functions), and the occupations.
    """
    output = output_object_factory(task)
    assert output.results_gbw is not None
    mf = output.results_gbw[0].to_pyscf()

    assert mf.energy_tot() == pytest.approx(scf_energy(output), abs=1e-6)


@pytest.mark.unit
@pytest.mark.output
def test_to_pyscf_orthonormal_orbitals(json_dir: Path) -> None:
    """ORCA's orbitals must be orthonormal with respect to PySCF's overlap matrix."""
    for json_file in gbw_fixtures(json_dir):
        mf = GbwResults.from_json_file(json_file).to_pyscf()
        overlap = mf.mol.intor("int1e_ovlp")

        for coeff in mo_matrices(mf):
            np.testing.assert_allclose(
                coeff.T @ overlap @ coeff, np.eye(coeff.shape[1]), atol=1e-6, err_msg=json_file.name
            )


@pytest.mark.unit
@pytest.mark.output
def test_to_pyscf_electron_count(json_dir: Path) -> None:
    """The occupations of ORCA's orbitals must match the electrons of PySCF's molecule."""
    for json_file in gbw_fixtures(json_dir):
        mf = GbwResults.from_json_file(json_file).to_pyscf()
        mo_occ = np.asarray(mf.mo_occ)

        if mo_occ.ndim == 2:
            assert tuple(mo_occ.sum(axis=1)) == pytest.approx(mf.mol.nelec), json_file.name
        else:
            assert mo_occ.sum() == pytest.approx(mf.mol.nelectron), json_file.name


@pytest.mark.unit
@pytest.mark.output
def test_ecps_parsed(json_dir: Path) -> None:
    """ECPs of the gbw-JSON must be parsed and only be applied to atoms that use them."""
    results = GbwResults.from_json_file(json_dir / "gbw/test_exmp003_opt_job.json")
    assert results.molecule is not None and results.molecule.atoms is not None
    oxygen = results.molecule.atoms[0]
    assert oxygen.ecps is not None
    assert oxygen.ecps.n_core == 2
    assert oxygen.ecps.lmax == "f"

    mol = results.to_pyscf().mol
    # > ORCA lists the ECP of oxygen also for the hydrogen atoms, which have none
    assert [mol.atom_nelec_core(i) for i in range(mol.natm)] == [2, 0, 0]


def shells_sorted(results: GbwResults) -> bool:
    """Whether the shells of each atom are sorted by angular momentum, like PySCF sorts them."""
    assert results.molecule is not None and results.molecule.atoms is not None
    order = "spdfghiklmn"
    return all(
        [order.index(shell.shell) for shell in atom.basis or []]
        == sorted(order.index(shell.shell) for shell in atom.basis or [])
        for atom in results.molecule.atoms
    )


@pytest.mark.unit
@pytest.mark.output
def test_pyscf_round_trip(json_dir: Path) -> None:
    """
    Converting gbw data to PySCF, back, and to PySCF again must reproduce the PySCF object.
    PySCF sorts the shells of each atom by angular momentum, so the comparison is done in PySCF.
    """
    for json_file in gbw_fixtures(json_dir):
        mf = GbwResults.from_json_file(json_file).to_pyscf()
        mf_converted = GbwResults.from_pyscf(mf).to_pyscf()
        mol, mol_converted = mf.mol, mf_converted.mol

        np.testing.assert_allclose(mol_converted.atom_coords(), mol.atom_coords(), atol=1e-8)
        assert [mol_converted.atom_charge(i) for i in range(mol.natm)] == [
            mol.atom_charge(i) for i in range(mol.natm)
        ]
        assert mol_converted.nbas == mol.nbas, json_file.name
        for ish in range(mol.nbas):
            assert mol_converted.bas_angular(ish) == mol.bas_angular(ish)
            np.testing.assert_allclose(mol_converted.bas_exp(ish), mol.bas_exp(ish))
            np.testing.assert_allclose(
                mol_converted.bas_ctr_coeff(ish), mol.bas_ctr_coeff(ish), atol=1e-10
            )
        # > Same ECPs, checked by their integrals
        np.testing.assert_allclose(
            mol_converted.intor("ECPscalar"), mol.intor("ECPscalar"), atol=1e-12
        )
        assert mol_converted.nelectron == mol.nelectron

        np.testing.assert_allclose(mf_converted.mo_coeff, mf.mo_coeff, err_msg=json_file.name)
        np.testing.assert_array_equal(mf_converted.mo_occ, mf.mo_occ)
        np.testing.assert_array_equal(mf_converted.mo_energy, mf.mo_energy)


@pytest.mark.unit
@pytest.mark.output
def test_pyscf_round_trip_gbw_data(json_dir: Path) -> None:
    """
    If the shells of the gbw data are sorted by angular momentum, converting gbw data to PySCF and
    back must reproduce the gbw data exactly.
    """
    for json_file in gbw_fixtures(json_dir):
        results = GbwResults.from_json_file(json_file)
        if not shells_sorted(results):
            continue
        reconverted = GbwResults.from_pyscf(results.to_pyscf())

        original = results.to_json()["Molecule"]
        converted = reconverted.to_json()["Molecule"]
        for atom, atom_converted in zip(original["Atoms"], converted["Atoms"], strict=True):
            assert atom_converted["ElementNumber"] == atom["ElementNumber"]
            assert atom_converted["NuclearCharge"] == atom["NuclearCharge"]
            np.testing.assert_allclose(atom_converted["Coords"], atom["Coords"], atol=1e-8)
            for shell, shell_converted in zip(atom["Basis"], atom_converted["Basis"], strict=True):
                assert shell_converted["Shell"] == shell["Shell"]
                np.testing.assert_allclose(shell_converted["Exponents"], shell["Exponents"])
                np.testing.assert_allclose(
                    shell_converted["Coefficients"], shell["Coefficients"], atol=1e-10
                )
            # > ECPs are only kept for atoms that use them
            if atom["ElementNumber"] != atom["NuclearCharge"]:
                assert atom_converted["ECPs"] == atom["ECPs"]
            else:
                assert "ECPs" not in atom_converted

        orbitals = original["MolecularOrbitals"]
        orbitals_converted = converted["MolecularOrbitals"]
        assert orbitals_converted["OrbitalLabels"] == orbitals["OrbitalLabels"]
        for mo, mo_converted in zip(orbitals["MOs"], orbitals_converted["MOs"], strict=True):
            np.testing.assert_allclose(mo_converted["MOCoefficients"], mo["MOCoefficients"])
            assert mo_converted["Occupancy"] == mo["Occupancy"]
            assert mo_converted["OrbitalEnergy"] == mo["OrbitalEnergy"]


@pytest.mark.unit
@pytest.mark.output
def test_to_pyscf_unsorted_shells(output_object_factory: Callable[[str], Output]) -> None:
    """
    Bismuth with def2-TZVP, augmented by a g, an f, and an h shell, has an ECP, g and h
    functions, and shells that are not sorted by angular momentum (..., f, f, g, f, h), which
    PySCF sorts. PySCF must still reproduce ORCA's energy. This also checks the signs of the
    functions with |m| = 4 (flipped) and |m| = 5 (not flipped).
    """
    output = output_object_factory("pyscf_roundtrip")
    assert output.results_gbw is not None
    results = output.results_gbw[0]
    # > Ensure the fixture keeps covering unsorted shells
    assert not shells_sorted(results)

    mf = results.to_pyscf()

    assert mf.mol.atom_nelec_core(0) == 60
    assert max(mf.mol.bas_angular(i) for i in range(mf.mol.nbas)) == 5
    assert mf.energy_tot() == pytest.approx(scf_energy(output), abs=1e-6)


@pytest.mark.unit
@pytest.mark.output
def test_from_pyscf_rejects_cartesian_basis() -> None:
    """ORCA only supports spherical basis functions."""
    mol = pyscf.gto.M(atom="He 0 0 0", basis="cc-pvdz", cart=True, verbose=0)
    mf = pyscf.scf.RHF(mol)
    mf.mo_coeff = np.eye(mol.nao)
    mf.mo_occ = np.zeros(mol.nao)

    with pytest.raises(ValueError, match="Cartesian"):
        GbwResults.from_pyscf(mf)


@pytest.mark.unit
@pytest.mark.output
def test_to_pyscf_unsorted_primitives(output_object_factory: Callable[[str], Output]) -> None:
    """
    PySCF sorts the primitives of a shell by exponent. Shells whose primitives are stored in
    another order must still be found and yield ORCA's energy.
    """
    output = output_object_factory("mp2")
    assert output.results_gbw is not None
    results = output.results_gbw[0].model_copy(deep=True)
    assert results.molecule is not None and results.molecule.atoms is not None
    reversed_shells = 0
    for atom in results.molecule.atoms:
        for shell in atom.basis or []:
            assert shell.exponents is not None and shell.coefficients is not None
            if len(shell.exponents) > 1:
                shell.exponents.reverse()
                shell.coefficients.reverse()
                reversed_shells += 1
    assert reversed_shells > 0

    mf = results.to_pyscf()

    assert mf.energy_tot() == pytest.approx(scf_energy(output), abs=1e-6)


def water_rhf() -> Any:
    """Mean-field object of water holding (unconverged) orbitals, without running an SCF."""
    mol = pyscf.gto.M(atom="O 0 0 0; H 0 0.757 0.587; H 0 -0.757 0.587", basis="sto-3g", verbose=0)
    mf = pyscf.scf.RHF(mol)
    mf.mo_coeff = np.eye(mol.nao)
    mf.mo_occ = np.array([2.0] * 5 + [0.0] * 2)
    mf.mo_energy = np.arange(mol.nao, dtype=float)
    return mf


@pytest.mark.unit
@pytest.mark.output
def test_from_pyscf_custom_orbitals() -> None:
    """Orbitals given explicitly must not be labeled with the data of the mean-field object."""
    mf = water_rhf()
    virtuals = mf.mo_coeff[:, 5:]

    # > The occupation numbers of the mean-field object do not belong to the given orbitals
    with pytest.raises(ValueError, match="mo_occ"):
        GbwResults.from_pyscf(mf, mo_coeff=virtuals)

    results = GbwResults.from_pyscf(mf, mo_coeff=virtuals, mo_occ=[0.0, 0.0])
    assert results.molecule is not None and results.molecule.molecularorbitals is not None
    mos = results.molecule.molecularorbitals.mos
    assert mos is not None
    assert [mo.occupancy for mo in mos] == [0.0, 0.0]
    # > Neither do its orbital energies
    assert [mo.orbitalenergy for mo in mos] == [0.0, 0.0]

    results = GbwResults.from_pyscf(mf, mo_coeff=virtuals, mo_occ=[0.0, 0.0], mo_energy=[1.5, 2.5])
    assert results.molecule is not None and results.molecule.molecularorbitals is not None
    mos = results.molecule.molecularorbitals.mos
    assert mos is not None
    assert [mo.orbitalenergy for mo in mos] == [1.5, 2.5]


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    ("kwargs", "match"),
    [
        # > Wrong number of occupation numbers or orbital energies
        ({"mo_occ": [2.0, 2.0]}, "mo_occ"),
        ({"mo_energy": [0.0, 1.0]}, "mo_energy"),
        # > Wrong number of basis functions
        ({"mo_coeff": np.eye(3), "mo_occ": [2.0, 2.0, 2.0]}, "basis functions"),
        # > Neither restricted nor unrestricted orbitals
        ({"mo_coeff": np.zeros((3, 7, 7)), "mo_occ": np.zeros((3, 7))}, "shape"),
        ({"mo_coeff": np.eye(7) * 1j, "mo_occ": np.zeros(7)}, "Complex"),
    ],
)
def test_from_pyscf_rejects_inconsistent_orbitals(kwargs: dict[str, Any], match: str) -> None:
    """Orbital data of inconsistent shape or type must be rejected with a clear error."""
    with pytest.raises(ValueError, match=match):
        GbwResults.from_pyscf(water_rhf(), **kwargs)


@pytest.mark.unit
@pytest.mark.output
def test_from_pyscf_requires_orbitals() -> None:
    """A mean-field object that was never run holds no orbitals."""
    mf = water_rhf()
    mf.mo_coeff = None

    with pytest.raises(ValueError, match="no orbitals"):
        GbwResults.from_pyscf(mf)


@pytest.mark.unit
@pytest.mark.output
def test_from_pyscf_unrestricted_object_with_restricted_orbitals() -> None:
    """Restricted orbitals, e.g., natural orbitals, may be taken from an unrestricted object."""
    mol = water_rhf().mol
    mf = pyscf.scf.UHF(mol)
    mf.mo_coeff = np.stack((np.eye(mol.nao), np.eye(mol.nao)))
    mf.mo_occ = np.stack(([1.0] * 5 + [0.0] * 2, [1.0] * 5 + [0.0] * 2))

    results = GbwResults.from_pyscf(mf, mo_coeff=np.eye(mol.nao), mo_occ=[2.0] * 5 + [0.0] * 2)

    assert results.molecule is not None and results.molecule.molecularorbitals is not None
    assert results.molecule.hftyp == "RHF"
    assert len(results.molecule.molecularorbitals.mos or []) == mol.nao


@pytest.mark.unit
@pytest.mark.output
def test_from_pyscf_open_shell_restricted_orbitals() -> None:
    """Restricted orbitals of an open-shell molecule must be stored as ROHF type orbitals."""
    mol = pyscf.gto.M(atom="O 0 0 0; H 0 0 0.97", basis="sto-3g", spin=1, verbose=0)
    mf = pyscf.scf.UHF(mol)
    natural_occupations = [2.0, 2.0, 2.0, 2.0, 1.0, 0.0]

    results = GbwResults.from_pyscf(mf, mo_coeff=np.eye(mol.nao), mo_occ=natural_occupations)

    assert results.molecule is not None
    assert results.molecule.multiplicity == 2
    assert results.molecule.hftyp == "ROHF"


@pytest.mark.unit
@pytest.mark.output
def test_from_pyscf_rejects_periodic_calculation() -> None:
    """Orbitals at two k-points must not be mistaken for unrestricted orbitals."""
    from pyscf.pbc import gto as pbc_gto
    from pyscf.pbc import scf as pbc_scf

    cell = pbc_gto.M(atom="He 0 0 0", a=np.eye(3) * 4.0, basis="sto-3g", verbose=0)
    mf = pbc_scf.KRHF(cell, kpts=cell.make_kpts([2, 1, 1]))
    mf.mo_coeff = np.ones((2, 1, 1))
    mf.mo_occ = np.full((2, 1), 2.0)

    with pytest.raises(ValueError, match="Periodic"):
        GbwResults.from_pyscf(mf)


@pytest.mark.unit
@pytest.mark.output
def test_from_pyscf_warns_about_relativistic_hamiltonian() -> None:
    """The relativistic Hamiltonian of PySCF is not part of the gbw data."""
    reference = water_rhf()
    mf = reference.x2c()
    mf.mo_coeff, mf.mo_occ = reference.mo_coeff, reference.mo_occ

    with pytest.warns(UserWarning, match="relativistic"):
        GbwResults.from_pyscf(mf)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    ("modify", "match"),
    [
        # > An atom without basis functions
        (lambda molecule: setattr(molecule.atoms[0], "basis", []), "lacks element"),
        # > Water cannot be a doublet, which PySCF reports with its own exception
        (lambda molecule: setattr(molecule, "multiplicity", 2), "PySCF cannot build"),
    ],
)
def test_to_pyscf_rejects_invalid_gbw_data(
    json_dir: Path, modify: Callable[[Any], None], match: str
) -> None:
    """Invalid gbw data must be reported as `ValueError`, also if PySCF detects it."""
    results = GbwResults.from_json_file(json_dir / "gbw/test_exmp006_mp2_job.json")
    modify(results.molecule)

    with pytest.raises(ValueError, match=match):
        results.to_pyscf()


@pytest.mark.unit
@pytest.mark.output
def test_to_pyscf_is_not_silenced(json_dir: Path) -> None:
    """The returned object must report warnings of PySCF, e.g., about an unconverged SCF."""
    mf = GbwResults.from_json_file(json_dir / "gbw/test_exmp006_mp2_job.json").to_pyscf()

    assert mf.verbose > 0
    assert mf.mol.verbose > 0


@pytest.mark.unit
@pytest.mark.output
def test_from_pyscf_rejects_generalized_orbitals() -> None:
    """Generalized (spinor-like) orbitals cannot be stored as RHF, UHF, or ROHF orbitals."""
    mol = water_rhf().mol
    mf = pyscf.scf.GHF(mol)
    mf.mo_coeff = np.eye(2 * mol.nao)
    mf.mo_occ = np.array([1.0] * 10 + [0.0] * 4)

    with pytest.raises(ValueError, match="Generalized"):
        GbwResults.from_pyscf(mf)


@pytest.mark.unit
@pytest.mark.output
def test_from_pyscf_rejects_spin_orbit_ecp() -> None:
    """ECPs with spin-orbit terms cannot be stored in gbw data."""
    mol = pyscf.gto.M(atom="I 0 0 0; H 0 0 1.61", basis="def2-svp", ecp={"I": "crenbl"}, verbose=0)
    mf = pyscf.scf.RHF(mol)
    mf.mo_coeff = np.eye(mol.nao)
    mf.mo_occ = np.zeros(mol.nao)

    with pytest.raises(ValueError, match="spin-orbit"):
        GbwResults.from_pyscf(mf)


@pytest.mark.unit
@pytest.mark.output
def test_missing_pyscf(json_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A helpful error must be raised if PySCF is not installed."""
    monkeypatch.setattr("opi.utils.optional.find_spec", lambda name: None)
    results = GbwResults.from_json_file(json_dir / "gbw/test_exmp006_mp2_job.json")

    with pytest.raises(ImportError, match="PySCF is not installed"):
        results.to_pyscf()
