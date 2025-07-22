from opi.models.string_enum import StringEnum


class GbwSuffixes(StringEnum):
    """Enumeration to keep track of the different suffixes of gbw files"""

    gbw = ".gbw"
    """Default gbw file suffix."""
    loc = ".loc"
    """Suffix for localized molecular orbitals."""
    qro = ".qro"
    """Suffix for quasi-restricted orbitals (QROs)."""
    uno = ".uno"
    """Suffix for unrestricted natural orbitals (UHFs)."""
    unso = ".unso"
    """Suffix for unrestricted natural spin-orbitals (UNSOs)."""
    uco = ".uco"
    """Suffix for unrestricted corresponding orbitals (UCOs)."""
    nbo = ".nbo"
    """Suffix for natural bond orbitals (NBOs)."""

    @classmethod
    def from_string(cls, suffix: str) -> "GbwSuffixes":
        if not suffix.startswith("."):
            suffix = f"{suffix}"
        try:
            return cls(suffix)
        except ValueError:
            allowed = ", ".join(m.value for m in cls)
            raise ValueError(f"Invalid gbw suffix: {suffix!r}. Allowed suffixes: {allowed}")
