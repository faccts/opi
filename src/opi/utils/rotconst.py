from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from opi.models.string_enum import StringEnum
from opi.utils import constants, units

__all__ = (
    "PrincipalMoments",
    "RotationalConstants",
    "RotorType",
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

    def rotor_type(self, tol: float = 1e-3) -> RotorType:
        Ia, Ib, Ic = self.Ia, self.Ib, self.Ic
        n_zero = sum(m < tol for m in (Ia, Ib, Ic))

        if n_zero == 3:
            return RotorType.MONOATOMIC
        if n_zero == 1 and abs(Ib - Ic) < tol:
            return RotorType.LINEAR
        if abs(Ia - Ib) < tol and abs(Ib - Ic) < tol:
            return RotorType.SPHERICAL_TOP
        if abs(Ib - Ic) < tol:  # Ia < Ib == Ic → prolate
            return RotorType.PROLATE_TOP
        if abs(Ia - Ib) < tol:  # Ia == Ib < Ic → oblate
            return RotorType.OBLATE_TOP
        return RotorType.ASYMMETRIC_TOP

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
    Stores rotational constants in MHz.

    Attributes
    ----------
    A, B, C : float | None
        Rotational constants in MHz (`None` for a degenerate axis).
    """

    def __init__(
        self,
        A: float | None,
        B: float | None,
        C: float | None,
    ) -> None:
        self.A = A
        self.B = B
        self.C = C

    def get_in_wavenumbers(self) -> tuple[float | None, float | None, float | None]:
        """
        Return rotational constants A, B, C converted to cm⁻¹.

        Returns
        -------
        tuple[float | None, float | None, float | None]
            A, B, C in cm⁻¹. `None` for any degenerate axis.
        """
        return (
            mhz_to_wavenumber(self.A),
            mhz_to_wavenumber(self.B),
            mhz_to_wavenumber(self.C),
        )

    def __str__(self) -> str:
        def fmt(x: float | None, unit: str = "") -> str:
            return f"{x:.6f} {unit}" if x is not None else "None"

        A_cm, B_cm, C_cm = self.get_in_wavenumbers()
        return (
            "Rotational constants:\n"
            f"  A = {fmt(self.A, 'MHz')}   ({fmt(A_cm, 'cm⁻¹')})\n"
            f"  B = {fmt(self.B, 'MHz')}   ({fmt(B_cm, 'cm⁻¹')})\n"
            f"  C = {fmt(self.C, 'MHz')}   ({fmt(C_cm, 'cm⁻¹')})"
        )


# ============================================================
# Helper functions (used by Structure methods)
# ============================================================


def moment_to_mhz(inertia: float | None) -> float | None:
    """
    Convert a principal moment of inertia (amu·Å²) to a rotational
    constant in MHz. Returns `None` when the moment is `None` or
    effectively zero (degenerate / linear axis).
    """
    if inertia is None or inertia < 1e-6:
        return None
    I_si = inertia * units.AMU_TO_KG * (units.ANGST_TO_M**2)
    return constants.H_PLANCK / (8.0 * np.pi**2 * I_si) / 1e6


def mhz_to_wavenumber(mhz: float | None) -> float | None:
    """
    Convert a rotational constant from MHz to cm⁻¹.
    Returns `None` if `mhz` is `None`.
    """
    if mhz is None:
        return None
    return mhz * 1e6 / constants.C
