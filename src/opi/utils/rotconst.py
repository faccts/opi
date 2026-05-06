from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from opi.models.string_enum import StringEnum
from opi.utils import constants, units

__all__ = (
    "PrincipalMoments",
    "RotationalConstants",
    "RotorType",
    "classify_rotor_type",
    "moment_to_mhz",
    "mhz_to_wavenumber",
)


# ============================================================
# Rotor type classification
# ============================================================
class RotorType(StringEnum):
    MONOATOMIC = "monoatomic"
    LINEAR = "linear"
    SPHERICAL_TOP = "spherical top"
    OBLATE_TOP = "symmetric top (oblate)"
    PROLATE_TOP = "symmetric top (prolate)"
    ASYMMETRIC_TOP = "asymmetric top"

    def __str__(self) -> str:
        return f"Rotor type : {self.value}"


# ============================================================
# Principal Moments
# ============================================================


@dataclass
class PrincipalMoments:
    """
    Principal moments of inertia (amu·Å²), sorted ascending.

    Attributes
    ----------
    Ia, Ib, Ic : float
        Principal moments in amu·Å².
    axes : np.ndarray, shape (3, 3)
        Corresponding eigenvectors (columns).
    """

    Ia: float
    Ib: float
    Ic: float
    axes: np.ndarray

    def __str__(self) -> str:
        return (
            "Moments of inertia (amu·Å²):\n"
            f"  Ia = {self.Ia:.6f}\n"
            f"  Ib = {self.Ib:.6f}\n"
            f"  Ic = {self.Ic:.6f}"
        )


# ============================================================
# Rotational constants result container
# ============================================================
class RotationalConstants:
    """
    Stores rotational constants and molecular moments of inertia.

    Attributes
    ----------
    A, B, C : float | None
        Rotational constants in MHz (None for a degenerate axis).
    A_cm, B_cm, C_cm : float | None
        Rotational constants in cm⁻¹.
    moments : tuple[float, float, float]
        Principal moments of inertia (Ia, Ib, Ic) in amu·Å².
    rotor_type : RotorType
        Molecular rotor classification.
    """

    def __init__(
        self,
        A: float | None,
        B: float | None,
        C: float | None,
        A_cm: float | None,
        B_cm: float | None,
        C_cm: float | None,
    ) -> None:
        self.A = A
        self.B = B
        self.C = C
        self.A_cm = A_cm
        self.B_cm = B_cm
        self.C_cm = C_cm

    def __str__(self) -> str:
        def fmt(x: float | None, unit: str = "") -> str:
            return f"{x:.6f} {unit}" if x is not None else "None"

        return (
            "Rotational constants:\n"
            f"  A = {fmt(self.A, 'MHz')}   ({fmt(self.A_cm, 'cm⁻¹')})\n"
            f"  B = {fmt(self.B, 'MHz')}   ({fmt(self.B_cm, 'cm⁻¹')})\n"
            f"  C = {fmt(self.C, 'MHz')}   ({fmt(self.C_cm, 'cm⁻¹')})"
        )


# ============================================================
# Helper functions (used by Structure methods)
# ============================================================


def moment_to_mhz(inertia: float) -> float | None:
    """
    Convert a principal moment of inertia (amu·Å²) to a rotational
    constant in MHz.  Returns None when the moment is effectively zero
    (degenerate / linear axis).
    """
    if inertia < 1e-6:
        return None
    I_si = inertia * units.AMU_TO_KG * (units.ANGST_TO_M**2)
    return constants.H_PLANCK / (8.0 * np.pi**2 * I_si) / 1e6


def mhz_to_wavenumber(mhz: float | None) -> float | None:
    """Convert a rotational constant from MHz to cm⁻¹."""
    if mhz is None:
        return None
    return mhz * 1e6 / constants.C


def classify_rotor_type(moments: np.ndarray, tol: float = 1e-3) -> RotorType:
    """
    Classify the molecular rotor from three principal moments of inertia
    (amu·Å², sorted ascending).

    Parameters
    ----------
    moments : array-like, shape (3,)
        Principal moments Ia ≤ Ib ≤ Ic.
    tol : float
        Absolute tolerance for treating two moments as equal.
    """
    Ia, Ib, Ic = moments
    n_zero = sum(m < 1e-6 for m in (Ia, Ib, Ic))

    if n_zero == 3:
        return RotorType.MONOATOMIC
    if n_zero == 2:
        return RotorType.LINEAR
    if abs(Ia - Ib) < tol and abs(Ib - Ic) < tol:
        return RotorType.SPHERICAL_TOP
    if abs(Ia - Ib) < tol:
        return RotorType.OBLATE_TOP
    if abs(Ib - Ic) < tol:
        return RotorType.PROLATE_TOP
    return RotorType.ASYMMETRIC_TOP
