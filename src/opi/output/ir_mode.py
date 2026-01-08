from dataclasses import dataclass
from typing import Tuple


@dataclass
class IrMode:
    """IR mode data."""

    mode: int
    wavenumber: float  # cm^-1
    eps: float  # L/(mol*cm)
    intensity: float  # km/mol
    dipole: Tuple[float, float, float]  # TX TY TZ

    @classmethod
    def from_string(cls, line: str) -> "IrMode":
        """
        Parse a line like:
        6:   1535.92   0.012167   61.49  0.002472  ( 0.028738 -0.018467 -0.036127)
        """
        # split once
        left, right = line.split("(", maxsplit=1)
        vec_str = right.split(")", maxsplit=1)[0]

        # parse vector
        tx, ty, tz = map(float, vec_str.split())

        # parse scalars
        parts = left.replace(":", "").split()
        mode = int(parts[0])
        wavenumber = float(parts[1])
        eps = float(parts[2])
        intensity = float(parts[3])

        return cls(
            mode=mode,
            wavenumber=wavenumber,
            eps=eps,
            intensity=intensity,
            dipole=(tx, ty, tz),
        )

    @property
    def dipole_squared(self) -> float:
        """Calculate T**2 by taking the dot-product of the dipoles."""
        return (
            self.dipole[0] * self.dipole[0]
            + self.dipole[1] * self.dipole[1]
            + self.dipole[2] * self.dipole[2]
        )

    @classmethod
    def header(cls) -> str:
        return (
            " Mode   freq       eps        Int     T**2         TX        TY        TZ\n"
            "       cm**-1   L/(mol*cm)  km/mol    a.u."
        )

    def __str__(self) -> str:
        """Reconstruct the IR line in ORCA-like format."""
        return (
            f"{self.mode:>3d}: "
            f"{self.wavenumber:9.2f} "
            f"{self.eps:10.6f} "
            f"{self.intensity:8.2f} "
            f"{self.dipole_squared:.6f}  "
            f"({self.dipole[0]: .6f} "
            f"{self.dipole[1]: .6f} "
            f"{self.dipole[2]: .6f})"
        )
