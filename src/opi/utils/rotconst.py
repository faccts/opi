import os
import warnings
from dataclasses import dataclass
from typing import List, Tuple, Union

import numpy as np

# ============================================================
# Physical constants
# ============================================================
_AMU_TO_KG = 1.66053906660e-27
_ANGSTROM_TO_M = 1.0e-10
_H_PLANCK = 6.62607015e-34
_C_CM = 2.99792458e10


# ============================================================
# Atomic masses
# ============================================================
ATOMIC_MASSES = {
    "X": 0.0,
    "PointCharge": 0.0,
    "H": 1.008,
    "He": 4.003,
    "Li": 6.941,
    "Be": 9.012,
    "B": 10.810,
    "C": 12.011,
    "N": 14.007,
    "O": 15.999,
    "F": 18.998,
    "Ne": 20.179,
    "Na": 22.990,
    "Mg": 24.305,
    "Al": 26.982,
    "Si": 28.086,
    "P": 30.974,
    "S": 32.060,
    "Cl": 35.453,
    "Ar": 39.948,
    "K": 39.100,
    "Ca": 40.080,
    "Sc": 44.960,
    "Ti": 47.900,
    "V": 50.940,
    "Cr": 52.000,
    "Mn": 54.940,
    "Fe": 55.850,
    "Co": 58.930,
    "Ni": 58.700,
    "Cu": 63.550,
    "Zn": 65.380,
    "Ga": 69.720,
    "Ge": 72.590,
    "As": 74.920,
    "Se": 78.960,
    "Br": 79.900,
    "Kr": 83.800,
    "Rb": 85.479,
    "Sr": 87.620,
    "Y": 88.910,
    "Zr": 91.220,
    "Nb": 92.910,
    "Mo": 95.940,
    "Tc": 97.000,
    "Ru": 101.070,
    "Rh": 102.910,
    "Pd": 106.400,
    "Ag": 107.870,
    "Cd": 112.410,
    "In": 114.820,
    "Sn": 118.690,
    "Sb": 121.750,
    "Te": 127.600,
    "I": 126.900,
    "Xe": 131.300,
    "Cs": 132.9054,
    "Ba": 137.3300,
    "La": 138.9055,
    "Ce": 140.1200,
    "Pr": 140.9077,
    "Nd": 144.2400,
    "Pm": 145.0000,
    "Sm": 150.4000,
    "Eu": 151.9600,
    "Gd": 157.2500,
    "Tb": 158.9254,
    "Dy": 162.5000,
    "Ho": 164.9304,
    "Er": 167.2600,
    "Tm": 168.9342,
    "Yb": 173.0400,
    "Lu": 174.9670,
    "Hf": 178.4900,
    "Ta": 180.9479,
    "W": 183.8500,
    "Re": 186.2070,
    "Os": 190.2000,
    "Ir": 192.2200,
    "Pt": 195.0900,
    "Au": 196.9665,
    "Hg": 200.5900,
    "Tl": 204.3700,
    "Pb": 207.2000,
    "Bi": 208.9804,
    "Po": 209.0000,
    "At": 210.0000,
    "Rn": 222.0000,
    "Fr": 223.0000,
    "Ra": 226.0254,
    "Ac": 227.0278,
    "Th": 232.0381,
    "Pa": 231.0359,
    "U": 238.0290,
    "Np": 237.0482,
    "Pu": 244.0000,
    "Am": 243.0000,
    "Cm": 247.0000,
    "Bk": 247.0000,
    "Cf": 251.0000,
    "Es": 252.0000,
    "Fm": 257.0000,
    "Md": 258.0000,
    "No": 259.0000,
    "Lr": 262.0000,
    "Rf": 267.0000,
    "Db": 268.0000,
    "Sg": 269.0000,
    "Bh": 270.0000,
    "Hs": 269.0000,
    "Mt": 278.0000,
    "Ds": 281.0000,
    "Rg": 281.0000,
    "Cn": 285.0000,
    "Nh": 283.0000,
    "Fl": 289.0000,
    "Mc": 288.0000,
    "Lv": 293.0000,
    "Ts": 294.0000,
    "Og": 294.0000,
}


# ============================================================
# Dataclass
# ============================================================
@dataclass
class RotationalConstants:
    A: float | None
    B: float | None
    C: float | None
    A_cm: float | None
    B_cm: float | None
    C_cm: float | None
    moments: tuple[float, float, float]
    rotor_type: str

    def __str__(self) -> str:
        def fmt(x: float | None, unit: str = "") -> str:
            return f"{x:.6f} {unit}" if x is not None else "None"

        return (
            # "Rotational Spectrum\n"
            # "--------------------\n"
            f"Rotor type : {self.rotor_type}\n\n"
            "Moments of inertia (amu·Å²):\n"
            f"  Ia = {self.moments[0]:.6f}\n"
            f"  Ib = {self.moments[1]:.6f}\n"
            f"  Ic = {self.moments[2]:.6f}\n\n"
            "Rotational constants:\n"
            f"  A = {fmt(self.A, 'MHz')}   ({fmt(self.A_cm, 'cm⁻¹')})\n"
            f"  B = {fmt(self.B, 'MHz')}   ({fmt(self.B_cm, 'cm⁻¹')})\n"
            f"  C = {fmt(self.C, 'MHz')}   ({fmt(self.C_cm, 'cm⁻¹')})"
        )


# ============================================================
# Utilities
# ============================================================
def _normalize_symbol(s: str) -> str:
    if s in ("X", "PointCharge"):
        return s
    return s.capitalize()


def _read_xyz(data: Union[str, Tuple[List[str], np.ndarray]]) -> Tuple[List[str], np.ndarray]:
    """
    Read geometry from:
    - XYZ file path
    - XYZ block string
    - (symbols, coords) tuple

    Returns
    -------
    symbols : list[str]
    coords : (N, 3) ndarray
    """

    # -------------------------
    # Case 1: string input
    # -------------------------
    if isinstance(data, str):
        # Case 1a: file path
        if os.path.isfile(data):
            with open(data, "r") as f:
                lines = f.readlines()
        else:
            # Case 1b: XYZ block string
            lines = data.strip().splitlines()

        if len(lines) < 3:
            raise ValueError("Invalid XYZ format: too few lines")

        try:
            n_atoms = int(lines[0].strip())
        except ValueError:
            raise ValueError("First line must contain number of atoms")

        symbols = []
        coords = []

        for i, line in enumerate(lines[2 : 2 + n_atoms], start=3):
            parts = line.split()

            if len(parts) < 4:
                raise ValueError(f"Line {i} malformed: '{line}'")

            # --- clean symbol ---
            raw_sym = parts[0].strip()

            # Remove numeric labels (e.g. C1 → C)
            sym = "".join(filter(str.isalpha, raw_sym))

            # Capitalization (cap insensitive)
            sym = sym.capitalize()

            try:
                xyz = [float(x) for x in parts[1:4]]
            except ValueError:
                raise ValueError(f"Invalid coordinates at line {i}: '{line}'")

            symbols.append(sym)
            coords.append(xyz)

        return symbols, np.array(coords, dtype=np.float64)

    else:
        raise TypeError("Input must be: file path or XYZ string")


# ============================================================
# Main function
# ============================================================
def rotational_constants(
    symbols: list[str] | None = None,
    coords: np.ndarray | None = None,
    xyz: str | None = None,
    masses: np.ndarray | None = None,
    weights: dict[str, float] | None = None,
    atom_weights: dict[int, float] | None = None,
) -> RotationalConstants | None:
    """
    Flexible rotational constant calculator.

    Input options
    -------------
    - symbols + coords
    - xyz (file path, string, or lines)

    Mass priority
    -------------
    masses > atom_weights > weights > default

    Unknown atoms
    -------------
    Assigned mass = 0 with warning (unless overridden).
    """

    # --- Input parsing ---
    if xyz is not None:
        symbols, coords = _read_xyz(xyz)

    if symbols is None or coords is None:
        raise ValueError("Provide either (symbols, coords) or xyz input.")

    coords = np.asarray(coords, dtype=np.float64)

    # --- Normalize symbols ---
    symbols = [_normalize_symbol(s) for s in symbols]

    # --- Prepare weights ---
    weights = {_normalize_symbol(k): v for k, v in (weights or {}).items()}
    atom_weights = atom_weights or {}

    # --- Assign masses ---
    if masses is not None:
        masses = np.asarray(masses, dtype=np.float64)

    else:
        masses_list = []
        for i, s in enumerate(symbols):
            if i in atom_weights:
                m = atom_weights[i]

            elif s in weights:
                m = weights[s]

            elif s in ATOMIC_MASSES:
                m = ATOMIC_MASSES[s]

            else:
                warnings.warn(f"Unknown element '{s}' → mass set to 0.0")
                m = 0.0

            masses_list.append(m)

        masses = np.array(masses_list, dtype=np.float64)

    # --- Filter zero-mass atoms ---
    mask = masses > 0.0
    if not np.any(mask):
        return None

    masses = masses[mask]
    coords = coords[mask]

    total_mass = masses.sum()

    # --- Center of mass ---
    com = (masses[:, None] * coords).sum(axis=0) / total_mass
    coords -= com

    # --- Inertia tensor ---
    inertia = np.zeros((3, 3), dtype=np.float64)
    assert coords is not None
    for m, r in zip(masses, coords):
        inertia += m * (np.dot(r, r) * np.eye(3) - np.outer(r, r))

    # --- Diagonalize ---
    moments_raw, _ = np.linalg.eigh(inertia)
    moments_raw = np.maximum(moments_raw, 0.0)
    Ia, Ib, Ic = moments_raw

    # --- Convert to rotational constants ---
    def _moment_to_mhz(inertia: float) -> float | None:
        if inertia < 1e-6:
            return None
        I_si = inertia * _AMU_TO_KG * (_ANGSTROM_TO_M**2)
        return _H_PLANCK / (8.0 * np.pi**2 * I_si) / 1e6

    def _mhz_to_cm(mhz: float | None) -> float | None:
        return None if mhz is None else mhz * 1e6 / _C_CM

    A = _moment_to_mhz(Ia)
    B = _moment_to_mhz(Ib)
    C = _moment_to_mhz(Ic)

    # --- Rotor classification ---
    tol = 1e-3
    n_zero = sum(m < 1e-6 for m in (Ia, Ib, Ic))

    if n_zero == 3:
        rotor = "monoatomic"
    elif n_zero == 2:
        rotor = "linear"
    elif abs(Ia - Ib) < tol and abs(Ib - Ic) < tol:
        rotor = "spherical top"
    elif abs(Ia - Ib) < tol:
        rotor = "symmetric top (oblate)"
    elif abs(Ib - Ic) < tol:
        rotor = "symmetric top (prolate)"
    else:
        rotor = "asymmetric top"

    return RotationalConstants(
        A=A,
        B=B,
        C=C,
        A_cm=_mhz_to_cm(A),
        B_cm=_mhz_to_cm(B),
        C_cm=_mhz_to_cm(C),
        moments=(Ia, Ib, Ic),
        rotor_type=rotor,
    )
