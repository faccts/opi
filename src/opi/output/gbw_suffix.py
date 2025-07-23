from typing import Self

from opi.models.string_enum import StringEnum


class GbwSuffix(StringEnum):
    """Enumeration to keep track of the different suffixes of gbw files"""

    GBW = ".gbw"
    """Default gbw file suffix."""
    LOC = ".loc"
    """Suffix for localized molecular orbitals."""
    QRO = ".qro"
    """Suffix for quasi-restricted orbitals (QROs)."""
    UNO = ".uno"
    """Suffix for unrestricted natural orbitals (UHFs)."""
    UNSO = ".unso"
    """Suffix for unrestricted natural spin-orbitals (UNSOs)."""
    UCO = ".uco"
    """Suffix for unrestricted corresponding orbitals (UCOs)."""
    NBO = ".nbo"
    """Suffix for natural bond orbitals (NBOs)."""

    @classmethod
    def _missing_(cls, suffix: object, /) -> Self:
        """
        Raises
        ------
        TypeError: If input value cannot be cast to string.
        ValueError: If input value is not part of the Enum.
        """
        # > Add leading dot if missing
        if isinstance(suffix, str) and not suffix.startswith("."):
            suffix = "." + suffix
        # > Can raise TypeError and ValueError
        return super()._missing_(suffix)
