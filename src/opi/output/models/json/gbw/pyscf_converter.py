"""
Conversion of the molecular orbital data of a gbw file (`GbwResults`) from and to PySCF.

ORCA and PySCF both use contracted, real spherical Gaussian basis functions whose contraction
coefficients refer to normalized primitives, and both store effective core potentials (ECPs) as a
local part plus semi-local parts relative to it. Hence, basis set and ECP data are transferred
as they are. The two programs differ only in the order and the sign of the basis functions
within a shell:

- ORCA orders the functions of a shell by m = 0, +1, -1, +2, -2, ...
- PySCF orders them by m = -l, ..., +l, except for p shells, which are ordered x, y, z
  (m = +1, -1, 0).
- ORCA's functions with |m| = 3 and |m| = 4 have the opposite sign of PySCF's, all others
  (including |m| = 5 and 6) have the same sign.

The order and sign convention was verified up to i shells (l = 6) against ORCA's overlap
matrix and energies.

PySCF sorts the shells of an atom by angular momentum, while ORCA keeps the order of the basis
set definition, so shells are matched by angular momentum and exponents.

PySCF is imported locally in each function, as it is an optional dependency of OPI.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

import numpy as np
import numpy.typing as npt

from opi.output.hftyp import Hftyp
from opi.output.models.json.gbw.properties.atoms import Atoms
from opi.output.models.json.gbw.properties.base import Base
from opi.output.models.json.gbw.properties.ecp import Ecp, EcpShell
from opi.output.models.json.gbw.properties.mo import MO
from opi.output.models.json.gbw.properties.molecular_orbitals import MolecularOrbitals
from opi.output.models.json.gbw.properties.molecule import Molecule
from opi.utils.element import Element

if TYPE_CHECKING:
    from opi.output.models.json.gbw.gbw_results import GbwResults

__all__ = ("gbw_to_pyscf", "gbw_from_pyscf")

# > Angular momentum letters as used by ORCA
SHELL_LETTERS = "spdfghi"

# > Names of the p and d functions in ORCA's orbital labels; higher shells are labeled by m
_ORCA_FUNCTION_NAMES = {0: ("s",), 1: ("pz", "px", "py"), 2: ("dz2", "dxz", "dyz", "dx2y2", "dxy")}

# > Pattern for the ghost atom prefixes that PySCF accepts in atom symbols
_GHOST_PREFIX = re.compile(r"^(GHOST-?|X-)", re.IGNORECASE)


# ============================================================
# AO ordering
# ============================================================


def _orca_m_values(ang: int, /) -> list[int]:
    """Magnetic quantum numbers of the functions of a shell in ORCA's order."""
    return [0] + [sign * m for m in range(1, ang + 1) for sign in (1, -1)]


def _pyscf_position(ang: int, m: int, /) -> int:
    """Position of the function with magnetic quantum number m in a PySCF shell."""
    if ang == 1:
        return {1: 0, -1: 1, 0: 2}[m]
    return m + ang


def shell_ao_map(ang: int, /) -> tuple[npt.NDArray[np.int_], npt.NDArray[np.float64]]:
    """
    Map the basis functions of a shell from ORCA's to PySCF's order.

    Parameters
    ----------
    ang : int
        Angular momentum of the shell.

    Returns
    -------
    tuple[npt.NDArray[np.int_], npt.NDArray[np.float64]]
        PySCF position and sign of each basis function in ORCA's order, so that
        `c_pyscf[position] = sign * c_orca`.
    """
    m_values = _orca_m_values(ang)
    positions = np.array([_pyscf_position(ang, m) for m in m_values], dtype=np.int_)
    signs = np.array([-1.0 if abs(m) in (3, 4) else 1.0 for m in m_values], dtype=np.float64)
    return positions, signs


def _orca_function_names(ang: int, /) -> list[str]:
    """Names of the functions of a shell as used in ORCA's orbital labels."""
    if ang in _ORCA_FUNCTION_NAMES:
        return list(_ORCA_FUNCTION_NAMES[ang])
    letter = SHELL_LETTERS[ang]
    return [f"{letter}{m:+d}" if m else f"{letter}0" for m in _orca_m_values(ang)]


def _shell_ang(shell: str | None, /) -> int:
    """Angular momentum of a shell letter."""
    if shell is None or shell.lower() not in SHELL_LETTERS:
        raise ValueError(f"Unsupported shell type in gbw data: {shell}")
    return SHELL_LETTERS.index(shell.lower())


# ============================================================
# ORCA -> PySCF
# ============================================================


def _has_ecp(atom: Atoms, /) -> bool:
    """
    Whether the ECP listed for an atom is in use. ORCA may list ECP data also for atoms without
    an ECP, so the number of core electrons is checked against the nuclear charge.
    """
    ecp = atom.ecps
    if ecp is None or not ecp.n_core or atom.elementnumber is None or atom.nuclearcharge is None:
        return False
    return round(atom.elementnumber - atom.nuclearcharge) == ecp.n_core


def _ecp_to_pyscf(ecp: Ecp, /) -> list[Any]:
    """Convert an ECP into PySCF's format: [n_core, [[l, [primitives per r power]], ...]]."""
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


def _match_pyscf_shells(
    mol: Any, atom_idx: int, shells: list[tuple[int, list[float]]], /
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
        PySCF molecule.
    atom_idx : int
        Index of the atom.
    shells : list[tuple[int, list[float]]]
        Angular momentum and exponents of the ORCA shells of the atom, in ORCA's order.

    Returns
    -------
    list[int]
        Index of the PySCF shell for each ORCA shell.
    """
    available = [int(ish) for ish in mol.atom_shell_ids(atom_idx)]
    matched: list[int] = []
    for ang, exponents in shells:
        # > PySCF sorts the primitives of a shell by exponent, so sorted exponents are compared
        sorted_exponents = np.sort(exponents)
        for ish in available:
            pyscf_exponents = mol.bas_exp(ish)
            if (
                int(mol.bas_angular(ish)) == ang
                and len(pyscf_exponents) == len(sorted_exponents)
                and np.allclose(np.sort(pyscf_exponents), sorted_exponents, rtol=1e-12, atol=0.0)
            ):
                matched.append(ish)
                available.remove(ish)
                break
        else:
            raise ValueError(f"Shell of atom {atom_idx} not found in PySCF molecule")
    return matched


def gbw_to_pyscf(gbw: GbwResults, /) -> Any:
    """
    Create a PySCF mean-field object from the molecular orbital data of a gbw file.

    See `GbwResults.to_pyscf()` for details.
    """
    from pyscf import gto, scf

    molecule = gbw.molecule
    if molecule is None or not molecule.atoms:
        raise ValueError("No atoms present in gbw data")
    mo_data = molecule.molecularorbitals
    if mo_data is None or not mo_data.mos:
        raise ValueError("No molecular orbitals present in gbw data")
    if molecule.hftyp is None:
        raise ValueError("HF type is missing in gbw data")
    hftyp = Hftyp(molecule.hftyp.lower())

    unit = "Bohr" if (molecule.coordinateunits or "").lower().startswith("bohr") else "Angstrom"

    atoms: list[tuple[str, list[float]]] = []
    basis: dict[str, list[Any]] = {}
    ecps: dict[str, list[Any]] = {}
    orca_shells: list[list[tuple[int, list[float]]]] = []
    for idx, atom in enumerate(molecule.atoms):
        if atom.elementnumber is None or atom.coords is None or atom.basis is None:
            raise ValueError(f"Atom {idx} in gbw data lacks element, coordinates, or basis set")
        element = Element.from_atomic_number(atom.elementnumber)
        # > A unique label per atom keeps the basis set and ECP of each atom exact
        label = f"{element.value}{idx + 1}"
        if atom.nuclearcharge == 0.0:
            label = f"ghost-{label}"
        atoms.append((label, atom.coords))

        shells: list[Any] = []
        atom_shells: list[tuple[int, list[float]]] = []
        for shell in atom.basis:
            if shell.exponents is None or shell.coefficients is None:
                raise ValueError(f"Basis shell of atom {idx} in gbw data is incomplete")
            ang = _shell_ang(shell.shell)
            shells.append([ang, *zip(shell.exponents, shell.coefficients, strict=True)])
            atom_shells.append((ang, shell.exponents))
        basis[label] = shells
        orca_shells.append(atom_shells)

        if atom.ecps is not None and _has_ecp(atom):
            ecps[label] = _ecp_to_pyscf(atom.ecps)

    mol = gto.M(
        atom=atoms,
        basis=basis,
        ecp=ecps,
        unit=unit,
        charge=molecule.charge or 0,
        spin=(molecule.multiplicity or 1) - 1,
        cart=False,
        verbose=0,
    )
    # > PySCF position and sign of each basis function in ORCA's order
    ao_loc = mol.ao_loc_nr()
    ao_positions: list[npt.NDArray[np.int_]] = []
    ao_signs: list[npt.NDArray[np.float64]] = []
    for idx, atom_shells in enumerate(orca_shells):
        for (ang, _), ish in zip(
            atom_shells, _match_pyscf_shells(mol, idx, atom_shells), strict=True
        ):
            positions, signs = shell_ao_map(ang)
            ao_positions.append(positions + ao_loc[ish])
            ao_signs.append(signs)
    positions = np.concatenate(ao_positions)
    signs = np.concatenate(ao_signs)
    n_ao = len(positions)
    if mol.nao != n_ao:
        raise ValueError(f"Basis set of PySCF ({mol.nao}) and gbw data ({n_ao}) differ in size")

    mos = mo_data.mos
    if any(mo.mocoefficients is None for mo in mos):
        raise ValueError("MO coefficients of at least one molecular orbital are missing")
    coeff_orca = np.array([mo.mocoefficients for mo in mos], dtype=np.float64).T
    if coeff_orca.shape[0] != n_ao:
        raise ValueError("Number of MO coefficients does not match the basis set size")
    coeff = np.empty_like(coeff_orca)
    coeff[positions] = signs[:, None] * coeff_orca
    occ = np.array([mo.occupancy or 0.0 for mo in mos], dtype=np.float64)
    energies = np.array([mo.orbitalenergy or 0.0 for mo in mos], dtype=np.float64)

    if hftyp == Hftyp.UHF:
        n_mo = len(mos) // 2
        mf = scf.UHF(mol)
        mf.mo_coeff = np.stack((coeff[:, :n_mo], coeff[:, n_mo:]))
        mf.mo_occ = np.stack((occ[:n_mo], occ[n_mo:]))
        mf.mo_energy = np.stack((energies[:n_mo], energies[n_mo:]))
    else:
        mf = scf.ROHF(mol) if hftyp == Hftyp.ROHF else scf.RHF(mol)
        mf.mo_coeff = coeff
        mf.mo_occ = occ
        mf.mo_energy = energies
    return mf


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


def _mo_list(
    coeff: npt.NDArray[np.float64],
    occ: npt.NDArray[np.float64],
    energies: npt.NDArray[np.float64] | None,
    /,
) -> list[MO]:
    """Create the gbw data models of molecular orbitals (coefficients in ORCA's AO order)."""
    return [
        MO(
            mocoefficients=[float(c) for c in coeff[:, i]],
            occupancy=float(occ[i]),
            orbitalenergy=float(energies[i]) if energies is not None else 0.0,
            orbitalsymlabel="A",
            orbitalsymmetry=0,
        )
        for i in range(coeff.shape[1])
    ]


def _orbital_data(
    mf: Any, n_ao: int, mo_coeff: Any, mo_occ: Any, mo_energy: Any, /
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64], npt.NDArray[np.float64] | None]:
    """
    Collect and validate the orbitals, occupation numbers, and orbital energies to convert.

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
    tuple[npt.NDArray[np.float64], npt.NDArray[np.float64], npt.NDArray[np.float64] | None]
        Orbitals with shape (n_ao, n_mo), or (2, n_ao, n_mo) for unrestricted orbitals, and
        occupation numbers and orbital energies with shape (n_mo,), or (2, n_mo). The orbital
        energies are None, if there are none for the orbitals.

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
    return coeff, occ, energies


def gbw_from_pyscf(
    mf: Any,
    /,
    *,
    mo_coeff: Any = None,
    mo_occ: Any = None,
    mo_energy: Any = None,
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

    mo_coeff, mo_occ, energies = _orbital_data(mf, mol.nao, mo_coeff, mo_occ, mo_energy)

    if mo_coeff.ndim == 3:
        hftyp = Hftyp.UHF
    elif isinstance(mf, scf.rohf.ROHF):
        hftyp = Hftyp.ROHF
    else:
        hftyp = Hftyp.RHF

    # > Basis set: one ORCA shell per contraction, keeping PySCF's shell order within each atom
    ao_loc = mol.ao_loc_nr()
    ao_index: list[npt.NDArray[np.int_]] = []
    ao_sign: list[npt.NDArray[np.float64]] = []
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
                positions, signs = shell_ao_map(ang)
                ao_index.append(positions + ao_loc[ish] + ictr * (2 * ang + 1))
                ao_sign.append(signs)
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

    index = np.concatenate(ao_index)
    sign = np.concatenate(ao_sign)
    if len(index) != mol.nao:
        raise ValueError("Basis set conversion failed: number of basis functions differs")

    def to_orca(coeff: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        result: npt.NDArray[np.float64] = sign[:, None] * coeff[index]
        return result

    if hftyp == Hftyp.UHF:
        # > ORCA lists the orbital labels once per spin
        labels = labels * 2
        mos = _mo_list(
            to_orca(mo_coeff[0]), mo_occ[0], None if energies is None else energies[0]
        ) + _mo_list(to_orca(mo_coeff[1]), mo_occ[1], None if energies is None else energies[1])
    else:
        mos = _mo_list(to_orca(mo_coeff), mo_occ, energies)

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
