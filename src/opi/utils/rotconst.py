from opi.models.string_enum import StringEnum

__all__ = ("RotationalConstants", "RotorType",)

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
        moments: tuple[float, float, float],
        rotor_type: RotorType,
    ) -> None:
        self.A = A
        self.B = B
        self.C = C
        self.A_cm = A_cm
        self.B_cm = B_cm
        self.C_cm = C_cm
        self.moments = moments
        self.rotor_type = rotor_type

    def __str__(self) -> str:
        def fmt(x: float | None, unit: str = "") -> str:
            return f"{x:.6f} {unit}" if x is not None else "None"

        return (
            f"Rotor type : {self.rotor_type}\n\n"
            "Moments of inertia (amu·Å²):\n"
            f"  Ia = {self.moments[0]:.6f}\n"
            f"  Ib = {self.moments[1]:.6f}\n"
            f"  Ic = {self.moments[2]:.6f}\n\n"
            "Rotational constants (yeih):\n"
            f"  A = {fmt(self.A, 'MHz')}   ({fmt(self.A_cm, 'cm⁻¹')})\n"
            f"  B = {fmt(self.B, 'MHz')}   ({fmt(self.B_cm, 'cm⁻¹')})\n"
            f"  C = {fmt(self.C, 'MHz')}   ({fmt(self.C_cm, 'cm⁻¹')})"
