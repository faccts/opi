from dataclasses import dataclass


@dataclass
class VcdMode:
    """
    Data available from ORCA for a single vibrational circular dichroism (VCD) mode.

    Attributes
    ----------
    mode: int
        Number of the mode, counting starts at 1.
    wavenumber: float
        Wavenumber of the mode in cm⁻¹.
    intensity: float
        Rotational strength of the mode in 1E-44*esu**2*cm**2. In contrast to an IR intensity
        this value is signed, and it changes sign between the two enantiomers.
    """

    mode: int
    wavenumber: float
    intensity: float

    @classmethod
    def from_string(cls, line: str) -> "VcdMode":
        """
        Parse a string line like:
            12   965.0         46.23
        and initializes `VcdMode` from it.

        Arguments
        ---------
        line: str
            String line from which to parse.

        Returns
        ---------
        VcdMode
            Parsed VCD mode.

        Raises
        ---------
        ValueError
            If the string cannot be properly parsed.
        """
        parts = line.replace(":", "").split()

        return cls(
            mode=int(parts[0]),
            wavenumber=float(parts[1]),
            intensity=float(parts[2]),
        )

    @classmethod
    def header(cls) -> str:
        """Returns the header from the ORCA VCD spectrum. Print this once before printing `VcdMode` for column context."""
        return " Mode   Freq    VCD-Intensity\n       (1/cm) (1E-44*esu^2*cm^2)"

    def __str__(self) -> str:
        """Reconstruct the VCD line in ORCA-like format."""
        return f"{self.mode:>5d} {self.wavenumber:>7.1f} {self.intensity:>13.2f}"
