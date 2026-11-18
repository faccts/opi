"""
Conversion of the molecular orbital data of a gbw file (`GbwResults`) from and to PySCF.

This module is internal to OPI and may change or move without notice. Use
`GbwResults.to_pyscf()` and `GbwResults.from_pyscf()` instead.

ORCA and PySCF both use contracted, real spherical Gaussian basis functions whose contraction
coefficients refer to normalized primitives, and both store effective core potentials (ECPs) as a
local part plus semi-local parts relative to it. Hence, basis set and ECP data are transferred
as they are. The two programs differ only in the order and the sign of the basis functions
within a shell:

- ORCA orders the functions of a shell by m = 0, +1, -1, +2, -2, ...
- PySCF orders them by m = -l, ..., +l, except for p shells, which are ordered x, y, z
  (m = +1, -1, 0).
- Up to l = 8, ORCA's functions with |m| = 3, 4, 7, and 8 have the opposite sign of PySCF's,
  all others have the same sign. For l = 9 and 10, all functions have the same sign.

ORCA supports shells up to l = 10 (letters s, p, d, f, g, h, i, k, l, m, n), PySCF up to l = 12.
The order and sign convention was verified for all of them against ORCA's overlap matrix.

PySCF sorts the shells of an atom by angular momentum, while ORCA keeps the order of the basis
set definition, so shells are matched by angular momentum and exponents.

PySCF is imported locally in each function, as it is an optional dependency of OPI.
"""

from __future__ import annotations

import re
import warnings
from collections.abc import Callable, Iterable
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Any

import numpy as np
import numpy.typing as npt

from opi.output.hftyp import Hftyp
from opi.output.models.json.gbw.properties.atoms import Atoms
from opi.output.models.json.gbw.properties.base import SHELL_LETTERS, Base
from opi.output.models.json.gbw.properties.ecp import Ecp, EcpShell
from opi.output.models.json.gbw.properties.mo import MO
from opi.output.models.json.gbw.properties.molecular_orbitals import MolecularOrbitals
from opi.output.models.json.gbw.properties.molecule import Molecule
from opi.utils.element import Element

if TYPE_CHECKING:
    from pyscf.gto import Mole
    from pyscf.scf.hf import SCF

    from opi.output.models.json.gbw.gbw_results import GbwResults

# > Pattern for the ghost atom prefixes that PySCF accepts in atom symbols
_GHOST_PREFIX = re.compile(r"^(GHOST-?|X-)", re.IGNORECASE)


# ============================================================
# Conventions of the basis functions
# ============================================================


@dataclass(frozen=True)
class ShellConvention:
    """
    Relation between ORCA's and PySCF's basis functions of a shell.

    Function k of a PySCF shell equals `sign[k]` times function `orca_index[k]` of the ORCA shell.
    Hence, the MO coefficients of these functions transform as
    `c_pyscf[k] = sign[k] * c_orca[orca_index[k]]`.

    Attributes
    ----------
    orca_index : tuple[int, ...]
        For each function of the PySCF shell, in PySCF's order, the index of the same function in
        the ORCA shell.
    sign : str
        For each function of the PySCF shell, in PySCF's order, "+" if ORCA's function has the
        same sign as PySCF's, and "-" if it has the opposite sign.

    Examples
    --------
    p shell: PySCF's px, py, pz are ORCA's functions 1, 2, 0 (ORCA's order is pz, px, py).

    >>> ORCA_TO_PYSCF_SHELLS[1]
    ShellConvention(orca_index=(1, 2, 0), sign='+++')

    f shell: PySCF's m = -3 function is minus ORCA's function 6 (m = -3), PySCF's m = 0 function
    is ORCA's function 0 (m = 0).

    >>> ORCA_TO_PYSCF_SHELLS[3]
    ShellConvention(orca_index=(6, 4, 2, 0, 1, 3, 5), sign='-+++++-')
    """

    orca_index: tuple[int, ...]
    sign: str


# > ORCA and PySCF both use real spherical harmonics, but order the 2l + 1 functions of a shell
# > differently and differ in the sign of some of them:
# >
# > - ORCA orders them by m = 0, +1, -1, +2, -2, ..., +l, -l (see `_orca_m_values()`).
# > - PySCF orders them by m = -l, ..., +l, except for p shells, which are ordered x, y, z
# >   (m = +1, -1, 0).
# >
# > Read from left (m = -l) to right (m = +l), the signs show the pattern: up to l = 8, ORCA's
# > functions with |m| = 3, 4, 7, and 8 have the opposite sign of PySCF's. For l = 9 and 10, all
# > functions have the same sign.
# >
# > How the table was determined and how to verify it, e.g., for a new ORCA version: run ORCA for a
# > molecule with shells of all angular momenta (`%basis AddGTO`), get ORCA's overlap matrix with
# > `Output.get_int_overlap(recreate_json=True)`, and compare it with PySCF's overlap matrix
# > (`mol.intor("int1e_ovlp")`) of the molecule from `GbwResults.to_pyscf()`. The table is
# > correct, if S_pyscf[k, k'] = sign[k] * sign[k'] * S_orca[orca_index[k], orca_index[k']] for
# > all pairs of basis functions k, k'. Note that the added shells must not make the basis set
# > nearly linearly dependent, as orca_2json then fails, and that the recreated gbw JSON only holds
# > the requested integrals, so convert the orbitals with `to_pyscf()` first. The tests in
# > tests/pyscf_conversion/test_high_angular_momentum.py check the table indirectly via ORCA's SCF
# > energy and the orthonormality of ORCA's orbitals in PySCF.
ORCA_TO_PYSCF_SHELLS: dict[int, ShellConvention] = {
    0: ShellConvention(orca_index=(0,), sign="+"),
    1: ShellConvention(orca_index=(1, 2, 0), sign="+++"),
    2: ShellConvention(orca_index=(4, 2, 0, 1, 3), sign="+++++"),
    3: ShellConvention(orca_index=(6, 4, 2, 0, 1, 3, 5), sign="-+++++-"),
    4: ShellConvention(orca_index=(8, 6, 4, 2, 0, 1, 3, 5, 7), sign="--+++++--"),
    5: ShellConvention(orca_index=(10, 8, 6, 4, 2, 0, 1, 3, 5, 7, 9), sign="+--+++++--+"),
    6: ShellConvention(
        orca_index=(12, 10, 8, 6, 4, 2, 0, 1, 3, 5, 7, 9, 11),
        sign="++--+++++--++",
    ),
    7: ShellConvention(
        orca_index=(14, 12, 10, 8, 6, 4, 2, 0, 1, 3, 5, 7, 9, 11, 13),
        sign="-++--+++++--++-",
    ),
    8: ShellConvention(
        orca_index=(16, 14, 12, 10, 8, 6, 4, 2, 0, 1, 3, 5, 7, 9, 11, 13, 15),
        sign="--++--+++++--++--",
    ),
    9: ShellConvention(
        orca_index=(18, 16, 14, 12, 10, 8, 6, 4, 2, 0, 1, 3, 5, 7, 9, 11, 13, 15, 17),
        sign="+++++++++++++++++++",
    ),
    10: ShellConvention(
        orca_index=(20, 18, 16, 14, 12, 10, 8, 6, 4, 2, 0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19),
        sign="+++++++++++++++++++++",
    ),
}
"""Relation between ORCA's and PySCF's basis functions for each angular momentum l = 0, ..., 10."""

# > Names of the p and d functions in ORCA's orbital labels; higher shells are labeled by m
_ORCA_FUNCTION_NAMES = {0: ("s",), 1: ("pz", "px", "py"), 2: ("dz2", "dxz", "dyz", "dx2y2", "dxy")}


def _orca_m_values(ang: int, /) -> list[int]:
    """
    Magnetic quantum numbers m of the functions of a shell, in ORCA's order.

    Parameters
    ----------
    ang : int
        Angular momentum l of the shell (0 for s, 1 for p, ...).

    Returns
    -------
    list[int]
        The 2l + 1 magnetic quantum numbers in ORCA's order 0, +1, -1, +2, -2, ..., +l, -l.

    Examples
    --------
    >>> _orca_m_values(2)
    [0, 1, -1, 2, -2]
    """
    return [0] + [sign * m for m in range(1, ang + 1) for sign in (1, -1)]


def _orca_function_names(ang: int, /) -> list[str]:
    """
    Names of the functions of a shell, in ORCA's order, as used in ORCA's orbital labels.

    Parameters
    ----------
    ang : int
        Angular momentum l of the shell (0 for s, 1 for p, ...), at most 10.

    Returns
    -------
    list[str]
        The 2l + 1 function names. s, p, and d functions are named like ORCA's Cartesian-like
        labels (e.g. "pz", "dxz"), higher shells by their letter and m (e.g. "f+1").

    Examples
    --------
    >>> _orca_function_names(1)
    ['pz', 'px', 'py']
    >>> _orca_function_names(3)
    ['f0', 'f+1', 'f-1', 'f+2', 'f-2', 'f+3', 'f-3']
    """
    if ang in _ORCA_FUNCTION_NAMES:
        return list(_ORCA_FUNCTION_NAMES[ang])
    letter = SHELL_LETTERS[ang]
    return [f"{letter}{m:+d}" if m else f"{letter}0" for m in _orca_m_values(ang)]


def _shell_ang(shell: str | None, /) -> int:
    """
    Angular momentum of a shell letter of the gbw data.

    Parameters
    ----------
    shell : str | None
        Shell letter as stored in the gbw data, e.g. "s" or "D" (case-insensitive).

    Returns
    -------
    int
        Angular momentum l of the shell, i.e., the index of the letter in `SHELL_LETTERS`.

    Raises
    ------
    ValueError
        If the letter is missing or not one of `SHELL_LETTERS`.

    Examples
    --------
    >>> _shell_ang("d")
    2
    >>> _shell_ang("K")
    7
    """
    if shell is None or shell.lower() not in SHELL_LETTERS:
        raise ValueError(f"Unsupported shell type in gbw data: {shell}")
    return SHELL_LETTERS.index(shell.lower())


@dataclass(frozen=True)
class AOMap:
    """
    Relation between ORCA's and PySCF's basis functions (AOs) of a molecule.

    Function `orca_ao[i]` of ORCA's basis equals `sign[i]` times function `pyscf_ao[i]` of
    PySCF's basis. Create it with `from_shells()` and transform MO coefficients with
    `orca_to_pyscf()` and `pyscf_to_orca()`.

    Attributes
    ----------
    orca_ao : npt.NDArray[np.int_]
        Indices of basis functions in ORCA's basis, with shape (n_ao,).
    pyscf_ao : npt.NDArray[np.int_]
        Indices of the same basis functions in PySCF's basis, with shape (n_ao,).
    sign : npt.NDArray[np.float64]
        Sign of ORCA's function relative to PySCF's (+1 or -1), with shape (n_ao,).
    """

    orca_ao: npt.NDArray[np.int_]
    pyscf_ao: npt.NDArray[np.int_]
    sign: npt.NDArray[np.float64]

    @classmethod
    def from_shells(cls, shells: Iterable[tuple[int, int, int]], /) -> AOMap:
        """
        Create the relation from the positions of the shells in ORCA's and PySCF's basis.

        Parameters
        ----------
        shells : Iterable[tuple[int, int, int]]
            The shells of the molecule in ORCA's order, each as its angular momentum, the index
            of its first basis function in ORCA's basis, and the index of its first basis function
            in PySCF's basis.

        Returns
        -------
        AOMap
            Relation of all basis functions of the shells.

        Raises
        ------
        ValueError
            If no shells are given, or if the shells do not cover each basis function of ORCA's
            and PySCF's basis exactly once.

        Examples
        --------
        ORCA's basis holds a p shell followed by an s shell (functions pz, px, py, s), while
        PySCF's basis holds the s shell first (functions s, px, py, pz). So the p shell starts at
        index 0 in ORCA's and at index 1 in PySCF's basis, and the s shell at index 3 in ORCA's
        and at index 0 in PySCF's basis:

        >>> ao_map = AOMap.from_shells([(1, 0, 1), (0, 3, 0)])
        >>> ao_map.orca_ao
        array([1, 2, 0, 3])
        >>> ao_map.pyscf_ao
        array([1, 2, 3, 0])
        >>> ao_map.sign
        array([1., 1., 1., 1.])

        That is, ORCA's px (1) is PySCF's px (1), ORCA's py (2) is PySCF's py (2), ORCA's pz (0)
        is PySCF's pz (3), and ORCA's s (3) is PySCF's s (0).
        """
        orca_ao: list[npt.NDArray[np.int_]] = []
        pyscf_ao: list[npt.NDArray[np.int_]] = []
        signs: list[npt.NDArray[np.float64]] = []
        for ang, orca_start, pyscf_start in shells:
            convention = ORCA_TO_PYSCF_SHELLS[ang]
            orca_ao.append(orca_start + np.array(convention.orca_index, dtype=np.int_))
            pyscf_ao.append(pyscf_start + np.arange(len(convention.orca_index), dtype=np.int_))
            signs.append(np.array([1.0 if s == "+" else -1.0 for s in convention.sign]))
        if not orca_ao:
            raise ValueError("No shells given")
        ao_map = cls(
            orca_ao=np.concatenate(orca_ao),
            pyscf_ao=np.concatenate(pyscf_ao),
            sign=np.concatenate(signs),
        )
        # > Otherwise, the transformed coefficients would hold uninitialized values
        all_aos = np.arange(ao_map.n_ao)
        if not (
            np.array_equal(np.sort(ao_map.orca_ao), all_aos)
            and np.array_equal(np.sort(ao_map.pyscf_ao), all_aos)
        ):
            raise ValueError("The shells do not cover each basis function exactly once")
        return ao_map

    @property
    def n_ao(self) -> int:
        """Number of basis functions."""
        return len(self.orca_ao)

    def orca_to_pyscf(self, coeff: npt.NDArray[np.float64], /) -> npt.NDArray[np.float64]:
        """
        Transform MO coefficients from ORCA's to PySCF's basis functions (AOs).

        Parameters
        ----------
        coeff : npt.NDArray[np.float64]
            MO coefficients with respect to ORCA's AOs, with shape (n_ao, n_mo).

        Returns
        -------
        npt.NDArray[np.float64]
            The same MOs as coefficients with respect to PySCF's AOs, with shape (n_ao, n_mo).
        """
        result = np.empty_like(coeff)
        result[self.pyscf_ao] = self.sign[:, None] * coeff[self.orca_ao]
        return result

    def pyscf_to_orca(self, coeff: npt.NDArray[np.float64], /) -> npt.NDArray[np.float64]:
        """
        Transform MO coefficients from PySCF's to ORCA's basis functions (AOs).

        The inverse of `orca_to_pyscf()`.

        Parameters
        ----------
        coeff : npt.NDArray[np.float64]
            MO coefficients with respect to PySCF's AOs, with shape (n_ao, n_mo).

        Returns
        -------
        npt.NDArray[np.float64]
            The same MOs as coefficients with respect to ORCA's AOs, with shape (n_ao, n_mo).
        """
        result = np.empty_like(coeff)
        result[self.orca_ao] = self.sign[:, None] * coeff[self.pyscf_ao]
        return result


# ============================================================
# Molecular orbitals
# ============================================================


@dataclass(frozen=True)
class Orbitals:
    """
    Molecular orbitals (MOs) of a restricted or unrestricted calculation.

    Restricted and unrestricted MOs are stored alike, with a leading spin axis of length n_spin =
    1 (restricted) or 2 (unrestricted: alpha, beta). The MO coefficients refer to either ORCA's or
    PySCF's basis functions (AOs); `transformed()` changes between them.

    The class is independent of ORCA and PySCF and is meant to stay so, e.g., to be reused for
    further formats. Do not add program-specific fields.

    Attributes
    ----------
    coeff : npt.NDArray[np.float64]
        MO coefficients with shape (n_spin, n_ao, n_mo).
    occ : npt.NDArray[np.float64]
        Occupation numbers with shape (n_spin, n_mo).
    energy : npt.NDArray[np.float64]
        Orbital energies in Hartree with shape (n_spin, n_mo).
    """

    coeff: npt.NDArray[np.float64]
    occ: npt.NDArray[np.float64]
    energy: npt.NDArray[np.float64]

    @property
    def n_spin(self) -> int:
        """Number of spin components: 1 for restricted, 2 for unrestricted MOs."""
        return int(self.coeff.shape[0])

    def transformed(
        self,
        transform: Callable[[npt.NDArray[np.float64]], npt.NDArray[np.float64]],
        /,
    ) -> Orbitals:
        """
        Transform the MO coefficients of each spin, e.g., from ORCA's to PySCF's AOs.

        Parameters
        ----------
        transform : Callable[[npt.NDArray[np.float64]], npt.NDArray[np.float64]]
            Transformation of MO coefficients with shape (n_ao, n_mo), i.e.,
            `AOMap.orca_to_pyscf` or `AOMap.pyscf_to_orca`.

        Returns
        -------
        Orbitals
            The same MOs with transformed coefficients; occupation numbers and orbital energies
            are kept.
        """
        return replace(self, coeff=np.stack([transform(coeff) for coeff in self.coeff]))


def _orca_orbitals(mos: list[MO], hftyp: Hftyp, /) -> Orbitals:
    """
    Read the MOs of the gbw data.

    Parameters
    ----------
    mos : list[MO]
        MOs of the gbw data. For UHF, the alpha MOs come first, followed by as many beta MOs.
    hftyp : Hftyp
        HF type of the gbw data, which tells whether the MOs are unrestricted.

    Returns
    -------
    Orbitals
        The MOs, with coefficients with respect to ORCA's AOs. Missing occupation numbers and
        orbital energies are set to zero.

    Raises
    ------
    ValueError
        If the MO coefficients of at least one MO are missing.
    """
    if any(mo.mocoefficients is None for mo in mos):
        raise ValueError("MO coefficients of at least one molecular orbital are missing")
    # > Shape (n_ao, n_mo) of all spins together
    coeff = np.array([mo.mocoefficients for mo in mos], dtype=np.float64).T
    occ = np.array([mo.occupancy or 0.0 for mo in mos], dtype=np.float64)
    energy = np.array([mo.orbitalenergy or 0.0 for mo in mos], dtype=np.float64)
    if hftyp == Hftyp.UHF:
        # > The gbw data lists the alpha MOs first, then the beta MOs: [a0, ..., a(n-1), b0, ...,
        # > b(n-1)]. The columns :n_mo are the alpha MOs and n_mo: the beta MOs, which are stacked
        # > along a new spin axis.
        n_mo = len(mos) // 2
        return Orbitals(
            coeff=np.stack((coeff[:, :n_mo], coeff[:, n_mo:])),
            occ=np.stack((occ[:n_mo], occ[n_mo:])),
            energy=np.stack((energy[:n_mo], energy[n_mo:])),
        )
    return Orbitals(coeff=coeff[None], occ=occ[None], energy=energy[None])


def _orca_mos(orbitals: Orbitals, /) -> list[MO]:
    """
    Create the MOs of the gbw data.

    Parameters
    ----------
    orbitals : Orbitals
        The MOs, with coefficients with respect to ORCA's AOs.

    Returns
    -------
    list[MO]
        MOs of the gbw data. For unrestricted MOs, the alpha MOs come first, followed by the beta
        MOs. Symmetry is not assigned.
    """
    return [
        MO(
            mocoefficients=coeff[:, i].tolist(),
            occupancy=float(occ[i]),
            orbitalenergy=float(energy[i]),
            orbitalsymlabel="A",
            orbitalsymmetry=0,
        )
        for coeff, occ, energy in zip(orbitals.coeff, orbitals.occ, orbitals.energy, strict=True)
        for i in range(coeff.shape[1])
    ]


# ============================================================
# ORCA -> PySCF
# ============================================================


def gbw_to_pyscf(gbw: GbwResults, /) -> SCF:
    """
    Create a PySCF mean-field object from the molecular orbital data of a gbw file.

    The conversion proceeds in four steps:

    1. Build PySCF's molecule from the gbw data: geometry, charge, multiplicity, basis set, and
       ECPs (`_orca_to_pyscf_mole()`).
    2. Relate ORCA's basis functions (AOs) to PySCF's (`_orca_to_pyscf_ao_map()`).
    3. Read the MOs from the gbw data (`_orca_orbitals()`) and transform their coefficients to
       PySCF's AOs.
    4. Create the mean-field object holding the MOs (`_pyscf_mean_field()`).

    See `GbwResults.to_pyscf()` for details.
    """
    molecule = gbw.molecule
    if molecule is None or not molecule.atoms:
        raise ValueError("No atoms present in gbw data")
    mo_data = molecule.molecularorbitals
    if mo_data is None or not mo_data.mos:
        raise ValueError("No molecular orbitals present in gbw data")
    if molecule.hftyp is None:
        raise ValueError("HF type is missing in gbw data")
    hftyp = Hftyp(molecule.hftyp.lower())

    mol = _orca_to_pyscf_mole(molecule)
    ao_map = _orca_to_pyscf_ao_map(molecule.atoms, mol)

    orca_orbitals = _orca_orbitals(mo_data.mos, hftyp)
    if orca_orbitals.coeff.shape[1] != ao_map.n_ao:
        raise ValueError("Number of MO coefficients does not match the basis set size")
    orbitals = orca_orbitals.transformed(ao_map.orca_to_pyscf)

    return _pyscf_mean_field(mol, hftyp, orbitals)


def _orca_to_pyscf_mole(molecule: Molecule, /) -> Mole:
    """
    Build PySCF's molecule from the gbw data.

    Each atom gets a unique label (e.g., "O1", "H2", and "ghost-H3" for a ghost atom), so that the
    basis set and ECP of each atom are transferred exactly, even if atoms of the same element
    differ in them. The basis set is passed to PySCF in ORCA's shell order, but PySCF sorts the
    shells of each atom by angular momentum (see `_orca_to_pyscf_shell_order()`).

    Parameters
    ----------
    molecule : Molecule
        Molecule of the gbw data with at least one atom.

    Returns
    -------
    pyscf.gto.Mole
        PySCF's molecule with spherical basis functions. It reports with PySCF's default verbosity.

    Raises
    ------
    ValueError
        If an atom lacks its element, coordinates, or basis set, if a shell is incomplete or of an
        unsupported angular momentum, or if PySCF cannot build the molecule, e.g., because charge
        and multiplicity do not match the number of electrons.
    """
    from pyscf import gto
    from pyscf.lib import logger

    unit = "Bohr" if (molecule.coordinateunits or "").lower().startswith("bohr") else "Angstrom"

    atoms: list[tuple[str, list[float]]] = []
    basis: dict[str, list[Any]] = {}
    ecps: dict[str, list[Any]] = {}
    for idx, atom in enumerate(molecule.atoms or []):
        if atom.elementnumber is None or atom.coords is None or not atom.basis:
            raise ValueError(f"Atom {idx} in gbw data lacks element, coordinates, or basis set")
        element = Element.from_atomic_number(atom.elementnumber)
        # > A unique label per atom keeps the basis set and ECP of each atom exact
        label = f"{element.value}{idx + 1}"
        if atom.nuclearcharge == 0.0:
            label = f"ghost-{label}"
        atoms.append((label, atom.coords))

        shells: list[Any] = []
        for shell in atom.basis:
            if shell.exponents is None or shell.coefficients is None:
                raise ValueError(f"Basis shell of atom {idx} in gbw data is incomplete")
            ang = _shell_ang(shell.shell)
            shells.append([ang, *zip(shell.exponents, shell.coefficients, strict=True)])
        basis[label] = shells

        if atom.ecps is not None and _orca_ecp_in_use(atom):
            ecps[label] = _orca_to_pyscf_ecp(atom.ecps)

    try:
        mol = gto.M(
            atom=atoms,
            basis=basis,
            ecp=ecps,
            unit=unit,
            charge=molecule.charge or 0,
            spin=(molecule.multiplicity or 1) - 1,
            cart=False,
            verbose=logger.QUIET,
        )
    except Exception as err:
        # > PySCF raises various exceptions, e.g., if charge and multiplicity do not match the
        # > number of electrons
        raise ValueError(f"PySCF cannot build the molecule of the gbw data: {err}") from err
    # > The molecule is built quietly, but PySCF shall report on anything the user does with the
    # > returned object, e.g., an SCF that does not converge
    mol.verbose = logger.NOTE
    return mol


def _orca_ecp_in_use(atom: Atoms, /) -> bool:
    """
    Whether the ECP listed for an atom in the gbw data is in use.

    ORCA may list ECP data also for atoms without an ECP, so the number of core electrons of the
    ECP is checked against the difference of atomic number and nuclear charge.

    Parameters
    ----------
    atom : Atoms
        Atom of the gbw data.

    Returns
    -------
    bool
        True if the atom has an ECP that replaces core electrons, False otherwise.
    """
    ecp = atom.ecps
    if ecp is None or not ecp.n_core or atom.elementnumber is None or atom.nuclearcharge is None:
        return False
    return round(atom.elementnumber - atom.nuclearcharge) == ecp.n_core


def _orca_to_pyscf_ecp(ecp: Ecp, /) -> list[Any]:
    """
    Convert an ECP from the gbw data into PySCF's format.

    Both programs store an ECP as a local part plus semi-local parts relative to it, with
    primitives c * r^(n-2) * exp(-a * r^2). The gbw data marks the local part as the channel of
    the highest angular momentum (`Ecp.lmax`), PySCF with l = -1.

    Parameters
    ----------
    ecp : Ecp
        ECP of an atom of the gbw data.

    Returns
    -------
    list[Any]
        ECP in PySCF's format: [n_core, [[l, [primitives of n = 0, primitives of n = 1, ...]],
        ...]] with the primitives as [a, c] pairs.

    Raises
    ------
    ValueError
        If a channel lacks exponents, coefficients, or powers, or has an unsupported angular
        momentum.
    """
    lmax = _shell_ang(ecp.lmax)
    channels: list[Any] = []
    for channel in ecp.potential or []:
        if channel.ecp is None or len(channel.ecp) != 3:
            raise ValueError("Invalid ECP data in gbw data")
        exponents, coefficients, powers = channel.ecp
        by_power: list[list[list[float]]] = [[] for _ in range(int(max(powers, default=0)) + 1)]
        for exponent, coefficient, power in zip(exponents, coefficients, powers, strict=True):
            by_power[int(power)].append([exponent, coefficient])
        ang = _shell_ang(channel.shell)
        # > PySCF labels the local part with l = -1
        channels.append([-1 if ang == lmax else ang, by_power])
    return [ecp.n_core, channels]


def _orca_to_pyscf_ao_map(atoms: list[Atoms], mol: Mole, /) -> AOMap:
    """
    Relate ORCA's basis functions (AOs) of the gbw data to PySCF's AOs of its molecule.

    ORCA's shells follow each other in ORCA's basis. In PySCF's basis, each ORCA shell starts at
    the first AO of its matching PySCF shell (see `_orca_to_pyscf_shell_order()`).

    Parameters
    ----------
    atoms : list[Atoms]
        Atoms of the gbw data, whose basis sets were checked by `_orca_to_pyscf_mole()`.
    mol : pyscf.gto.Mole
        PySCF's molecule built from these atoms by `_orca_to_pyscf_mole()`.

    Returns
    -------
    AOMap
        Relation between ORCA's and PySCF's AOs.

    Raises
    ------
    ValueError
        If a shell of the gbw data is not found in PySCF's molecule, or if the basis sets differ
        in size.
    """
    ao_loc = mol.ao_loc_nr()
    shell_positions: list[tuple[int, int, int]] = []
    orca_start = 0
    for idx, atom in enumerate(atoms):
        orca_shells = [
            (_shell_ang(shell.shell), shell.exponents or []) for shell in atom.basis or []
        ]
        pyscf_shells = _orca_to_pyscf_shell_order(mol, idx, orca_shells)
        for (ang, _), ish in zip(orca_shells, pyscf_shells, strict=True):
            shell_positions.append((ang, orca_start, int(ao_loc[ish])))
            orca_start += 2 * ang + 1
    ao_map = AOMap.from_shells(shell_positions)
    if mol.nao != ao_map.n_ao:
        raise ValueError(
            f"Basis set of PySCF ({mol.nao}) and gbw data ({ao_map.n_ao}) differ in size"
        )
    return ao_map


def _orca_to_pyscf_shell_order(
    mol: Mole, atom_idx: int, shells: list[tuple[int, list[float]]], /
) -> list[int]:
    """
    Find the PySCF shell of each ORCA shell of an atom.

    PySCF sorts the shells of an atom by angular momentum, while ORCA keeps the order of the
    basis set definition (e.g., the polarization functions of def2-QZVPP come after higher
    shells). Hence, the shells are matched by angular momentum and exponents. Shells that agree
    in both (e.g., general contractions) keep their relative order in PySCF.

    Parameters
    ----------
    mol : pyscf.gto.Mole
        PySCF's molecule.
    atom_idx : int
        Index of the atom.
    shells : list[tuple[int, list[float]]]
        Angular momentum and exponents of the ORCA shells of the atom, in ORCA's order.

    Returns
    -------
    list[int]
        Index of the PySCF shell for each ORCA shell.

    Raises
    ------
    ValueError
        If an ORCA shell has no matching PySCF shell.
    """
    # > PySCF sorts the primitives of a shell by exponent, so sorted exponents are compared
    available = [int(ish) for ish in mol.atom_shell_ids(atom_idx)]
    pyscf_shells = {
        ish: (int(mol.bas_angular(ish)), np.sort(mol.bas_exp(ish))) for ish in available
    }
    matched: list[int] = []
    for ang, exponents in shells:
        sorted_exponents = np.sort(exponents)
        for ish in available:
            pyscf_ang, pyscf_exponents = pyscf_shells[ish]
            if (
                pyscf_ang == ang
                and len(pyscf_exponents) == len(sorted_exponents)
                and np.allclose(pyscf_exponents, sorted_exponents, rtol=1e-12, atol=0.0)
            ):
                matched.append(ish)
                available.remove(ish)
                break
        else:
            raise ValueError(f"Shell of atom {atom_idx} not found in PySCF molecule")
    return matched


def _pyscf_mean_field(mol: Mole, hftyp: Hftyp, orbitals: Orbitals, /) -> SCF:
    """
    Create PySCF's mean-field object holding the MOs.

    The object is created with PySCF's factory functions, which choose the class by the HF type
    and PySCF's molecule (always without symmetry here):

    - UHF: `scf.UHF` returns `uhf.UHF` (`uhf.HF1e` for one electron).
    - ROHF: `scf.ROHF` returns `rohf.ROHF` (`rohf.HF1e` for one electron). Fractional occupation
      numbers are replaced by integer ones (see `_integer_rohf_occupations()`).
    - RHF and CASSCF: `scf.RHF` returns `rhf.RHF` for a singlet, but `rohf.ROHF` for higher
      multiplicities. The occupation numbers are kept, i.e., CASSCF natural orbitals keep their
      fractional occupation numbers.

    Parameters
    ----------
    mol : pyscf.gto.Mole
        PySCF's molecule.
    hftyp : Hftyp
        HF type of the gbw data.
    orbitals : Orbitals
        The MOs, with coefficients with respect to PySCF's AOs. They are unrestricted for UHF.

    Returns
    -------
    pyscf.scf.hf.SCF
        PySCF's mean-field object with `mo_coeff`, `mo_occ`, and `mo_energy` set. No SCF has been
        run with it.

    Warns
    -----
    UserWarning
        If fractional ROHF occupation numbers are replaced by integer ones.
    """
    from pyscf import scf

    if hftyp == Hftyp.UHF:
        mf = scf.UHF(mol)
        mf.mo_coeff = orbitals.coeff
        mf.mo_occ = orbitals.occ
        mf.mo_energy = orbitals.energy
        return mf

    occ = orbitals.occ[0]
    if hftyp == Hftyp.ROHF:
        mf = scf.ROHF(mol)
        occ = _integer_rohf_occupations(occ, mol.nelec)
    else:
        mf = scf.RHF(mol)
    mf.mo_coeff = orbitals.coeff[0]
    mf.mo_occ = occ
    mf.mo_energy = orbitals.energy[0]
    return mf


def _integer_rohf_occupations(
    occ: npt.NDArray[np.float64], nelec: tuple[int, int], /
) -> npt.NDArray[np.float64]:
    """
    Return ROHF occupation numbers that PySCF can handle.

    For an open shell of degenerate orbitals (e.g., the pi orbitals of OH), ORCA's ROHF averages
    over the configurations and stores fractional occupation numbers. PySCF's ROHF only
    represents a single determinant, with occupation numbers of 0, 1, and 2. Fractional
    occupations are therefore replaced by integer ones, filling the orbitals in ORCA's order.

    Parameters
    ----------
    occ : npt.NDArray[np.float64]
        ROHF occupation numbers from the gbw data with shape (n_mo,), in ORCA's orbital order.
    nelec : tuple[int, int]
        Numbers of alpha and beta electrons.

    Returns
    -------
    npt.NDArray[np.float64]
        `occ` if all occupation numbers are integers, otherwise integer occupation numbers.

    Warns
    -----
    UserWarning
        If the occupation numbers had to be replaced.
    """
    if np.allclose(occ, np.round(occ)):
        return occ
    n_alpha, n_beta = nelec
    integer_occ = np.zeros_like(occ)
    integer_occ[:n_beta] = 2.0
    integer_occ[n_beta:n_alpha] = 1.0
    # > Points to the line of `GbwResults.to_pyscf()` that calls `gbw_to_pyscf()`
    warnings.warn(
        "ORCA's ROHF averaged the occupation of degenerate open-shell orbitals, which a "
        "single-determinant PySCF object cannot represent. The fractional occupation numbers "
        "were replaced by integer ones, so the energy of the PySCF object differs from ORCA's.",
        stacklevel=4,
    )
    return integer_occ


# ============================================================
# PySCF -> ORCA
# ============================================================


def _ecp_from_pyscf(n_core: int, channels: list[Any], /) -> Ecp:
    """Convert an ECP from PySCF's format into the gbw data model."""
    semi_local = {int(ang): data for ang, data in channels if int(ang) >= 0}
    local = next((data for ang, data in channels if int(ang) < 0), None)
    lmax = max(semi_local, default=-1) + 1

    def to_channel(ang: int, data: list[Any] | None) -> EcpShell:
        exponents: list[float] = []
        coefficients: list[float] = []
        powers: list[float] = []
        for power, primitives in enumerate(data or []):
            for primitive in primitives:
                if len(primitive) != 2:
                    raise ValueError(
                        "ECPs with spin-orbit terms are not supported, ORCA's gbw data only "
                        "holds scalar ECPs"
                    )
                exponent, coefficient = primitive
                exponents.append(float(exponent))
                coefficients.append(float(coefficient))
                powers.append(float(power))
        if not exponents:
            # > ORCA expects at least one primitive per channel
            exponents, coefficients, powers = [1.0], [0.0], [2.0]
        return EcpShell(shell=SHELL_LETTERS[ang], ecp=[exponents, coefficients, powers])

    potential = [to_channel(ang, semi_local.get(ang)) for ang in range(lmax)]
    potential.append(to_channel(lmax, local))
    return Ecp(n_core=n_core, lmax=SHELL_LETTERS[lmax], potential=potential)


def _pyscf_orbitals(
    mf: SCF,
    n_ao: int,
    mo_coeff: npt.ArrayLike | None,
    mo_occ: npt.ArrayLike | None,
    mo_energy: npt.ArrayLike | None,
    /,
) -> Orbitals:
    """
    Collect and validate the MOs, occupation numbers, and orbital energies to convert.

    Parameters
    ----------
    mf : pyscf.scf.hf.SCF
        PySCF mean-field object, used for everything that is not given explicitly.
    n_ao : int
        Number of basis functions.
    mo_coeff : array_like | None
        Molecular orbitals to use instead of `mf.mo_coeff`.
    mo_occ : array_like | None
        Occupation numbers to use instead of `mf.mo_occ`.
    mo_energy : array_like | None
        Orbital energies to use instead of `mf.mo_energy`.

    Returns
    -------
    Orbitals
        The MOs, with coefficients with respect to PySCF's AOs. They are unrestricted, if the MO
        coefficients have the shape (2, n_ao, n_mo). The orbital energies are zero, if there are
        none for the MOs.

    Raises
    ------
    ValueError
        If orbitals or occupation numbers are missing, complex, or of inconsistent shape.
    """
    custom_orbitals = mo_coeff is not None
    if not custom_orbitals:
        mo_coeff = mf.mo_coeff
        if mo_coeff is None:
            raise ValueError(
                "The mean-field object holds no orbitals: run the SCF first or pass `mo_coeff`"
            )
    if mo_occ is None:
        # > The occupation numbers of the mean-field object belong to its own orbitals
        if custom_orbitals:
            raise ValueError("`mo_occ` is required, if `mo_coeff` is given")
        mo_occ = mf.mo_occ
        if mo_occ is None:
            raise ValueError("The mean-field object holds no occupation numbers: pass `mo_occ`")
    # > Likewise, the orbital energies of the mean-field object only belong to its own orbitals
    if mo_energy is None and not custom_orbitals:
        mo_energy = getattr(mf, "mo_energy", None)

    if any(np.iscomplexobj(data) for data in (mo_coeff, mo_occ, mo_energy) if data is not None):
        raise ValueError("Complex orbitals are not supported")
    try:
        coeff = np.asarray(mo_coeff, dtype=np.float64)
        occ = np.asarray(mo_occ, dtype=np.float64)
        energies = None if mo_energy is None else np.asarray(mo_energy, dtype=np.float64)
    except (TypeError, ValueError) as err:
        raise ValueError("Orbital data cannot be converted into arrays of numbers") from err

    if coeff.ndim not in (2, 3) or (coeff.ndim == 3 and coeff.shape[0] != 2):
        raise ValueError(
            "`mo_coeff` must have the shape (n_ao, n_mo), or (2, n_ao, n_mo) for unrestricted "
            f"orbitals, but has the shape {coeff.shape}"
        )
    if coeff.shape[-2] != n_ao:
        raise ValueError(
            f"`mo_coeff` has {coeff.shape[-2]} rows, but the molecule has {n_ao} basis functions"
        )
    # > One occupation number and energy per orbital, with a leading spin axis if unrestricted
    expected_shape = coeff.shape[:-2] + coeff.shape[-1:]
    if occ.shape != expected_shape:
        raise ValueError(
            f"`mo_occ` has the shape {occ.shape}, but `mo_coeff` requires {expected_shape}"
        )
    if energies is not None and energies.shape != expected_shape:
        raise ValueError(
            f"`mo_energy` has the shape {energies.shape}, but `mo_coeff` requires {expected_shape}"
        )
    if energies is None:
        energies = np.zeros_like(occ)
    if coeff.ndim == 2:
        # > Restricted MOs get a spin axis of length 1
        return Orbitals(coeff=coeff[None], occ=occ[None], energy=energies[None])
    return Orbitals(coeff=coeff, occ=occ, energy=energies)


def gbw_from_pyscf(
    mf: SCF,
    /,
    *,
    mo_coeff: npt.ArrayLike | None = None,
    mo_occ: npt.ArrayLike | None = None,
    mo_energy: npt.ArrayLike | None = None,
) -> GbwResults:
    """
    Create gbw data from a PySCF mean-field object.

    See `GbwResults.from_pyscf()` for details.
    """
    from pyscf import scf

    from opi.output.models.json.gbw.gbw_results import GbwResults

    mol = mf.mol
    if mol.cart:
        raise ValueError("Cartesian basis functions are not supported, ORCA uses spherical ones")

    if isinstance(mf, scf.ghf.GHF | scf.dhf.DHF):
        raise ValueError(
            "Generalized and four-component orbitals are not supported, "
            "only RHF, UHF, and ROHF type orbitals"
        )

    # > Orbitals at k-points have the same array rank as unrestricted orbitals
    if hasattr(mf, "cell") or hasattr(mf, "kpts"):
        raise ValueError("Periodic calculations are not supported")
    if getattr(mf, "with_x2c", None) is not None:
        warnings.warn(
            "The mean-field object uses a relativistic (X2C) Hamiltonian, which is not part of "
            "the gbw data. Request a corresponding Hamiltonian in ORCA.",
            stacklevel=2,
        )

    pyscf_orbitals = _pyscf_orbitals(mf, mol.nao, mo_coeff, mo_occ, mo_energy)

    # > The HF type has to be consistent with the multiplicity, which is taken from the molecule:
    # > restricted orbitals of an open-shell molecule are ROHF type orbitals
    if pyscf_orbitals.n_spin == 2:
        hftyp = Hftyp.UHF
    elif isinstance(mf, scf.rohf.ROHF) or mol.spin != 0:
        hftyp = Hftyp.ROHF
    else:
        hftyp = Hftyp.RHF

    # > Basis set: one ORCA shell per contraction, keeping PySCF's shell order within each atom
    ao_loc = mol.ao_loc_nr()
    # > Angular momentum and position of the first basis function in ORCA's and PySCF's basis of
    # > each ORCA shell
    shell_positions: list[tuple[int, int, int]] = []
    orca_start = 0
    labels: list[str] = []
    atoms: list[Atoms] = []
    coords = mol.atom_coords(unit="Angstrom")
    for idx in range(mol.natm):
        symbol = _GHOST_PREFIX.sub("", mol.atom_pure_symbol(idx))
        element = Element(symbol)
        atomic_number = element.atomic_number
        is_ghost = mol.atom_charge(idx) == 0
        n_core = int(mol.atom_nelec_core(idx))

        shells: list[Base] = []
        shell_count: dict[int, int] = {}
        for ish in mol.atom_shell_ids(idx):
            ang = int(mol.bas_angular(ish))
            exponents = [float(e) for e in mol.bas_exp(ish)]
            coefficients = mol.bas_ctr_coeff(ish)
            for ictr in range(mol.bas_nctr(ish)):
                shells.append(
                    Base(
                        shell=SHELL_LETTERS[ang],
                        exponents=exponents,
                        coefficients=[float(c) for c in coefficients[:, ictr]],
                    )
                )
                # > ORCA's shells follow each other in ORCA's basis. In PySCF's basis, the
                # > contractions of a PySCF shell follow each other.
                pyscf_start = int(ao_loc[ish]) + ictr * (2 * ang + 1)
                shell_positions.append((ang, orca_start, pyscf_start))
                orca_start += 2 * ang + 1
                shell_count[ang] = shell_count.get(ang, 0) + 1
                labels.extend(
                    f"{idx}{element.value:<2}  {shell_count[ang]}{name}"
                    for name in _orca_function_names(ang)
                )

        ecp = None
        if n_core:
            ecp_data = mol._ecp.get(mol.atom_symbol(idx)) or mol._ecp.get(symbol)
            if ecp_data is None:
                raise ValueError(f"ECP of atom {idx} not found in PySCF molecule")
            ecp = _ecp_from_pyscf(n_core, ecp_data[1])

        atoms.append(
            Atoms(
                basis=shells,
                coords=[float(x) for x in coords[idx]],
                ecps=ecp,
                elementlabel=element.value,
                elementnumber=atomic_number,
                idx=idx,
                nuclearcharge=0.0 if is_ghost else float(atomic_number - n_core),
            )
        )

    ao_map = AOMap.from_shells(shell_positions)
    if ao_map.n_ao != mol.nao:
        raise ValueError("Basis set conversion failed: number of basis functions differs")

    orbitals = pyscf_orbitals.transformed(ao_map.pyscf_to_orca)
    mos = _orca_mos(orbitals)
    # > ORCA lists the orbital labels once per spin
    labels = labels * orbitals.n_spin

    molecule = Molecule(
        atoms=atoms,
        molecularorbitals=MolecularOrbitals(energyunit="Eh", mos=mos, orbitallabels=labels),
        coordinateunits="Angs",
        multiplicity=int(mol.spin) + 1,
        charge=int(mol.charge),
        hftyp=hftyp.value.upper(),
        origin=(0.0, 0.0, 0.0),
    )
    # > The ORCA header has no default value and is set via its alias
    return GbwResults.model_validate({"orca header": None, "molecule": molecule})
