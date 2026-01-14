from dataclasses import dataclass
from typing import Tuple


@dataclass
class IrMode:
    """
    Data available from ORCA for a single infrared (IR) mode.

    Attributes
    ----------
    mode: int
        Number of the mode, counting starts at 1.
    wavenumber: float
        Wavenumber of the mode in cm⁻¹.
    eps: float
        Partial molar absorptivity (epsilon) of the mode in L/(mol*cm).
    intensity: float
        IR intensity of the mode in km/mol.
    dipole: Tuple[float, float, float]
        Dipole derivatives TX TY TZ in atomic units.
    """

    mode: int
    wavenumber: float
    eps: float
    intensity: float
    dipole: Tuple[float, float, float]

    @classmethod
    def from_string(cls, line: str) -> "IrMode":
        """
        Parse a string line like:
        6:   1535.92   0.012167   61.49  0.002472  ( 0.028738 -0.018467 -0.036127)
        and initializes `IrMode` from it.

        Arguments
        ---------
        line: str
            String line from which to parse.

        Returns
        ---------
        IrMode
            Parsed IR mode.

        Raises
        ---------
        ValueError
            If the string cannot be properly parsed.
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
        """Returns the header from the ORCA IR spectrum. Print this once before printing `IrMode` for column context."""
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
