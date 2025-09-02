from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("ShellType",)


class ShellType(SimpleKeywordBox):
    """Enum to store all simple keywords of type ShellType."""

    RHF = SimpleKeyword("rhf")
    """SimpleKeyword: Type of the wavefunction: restricted, unrestricted, multireference."""
    RKS = SimpleKeyword("rks")
    """SimpleKeyword: Type of the wavefunction: restricted, unrestricted, multireference."""
    ROHF = SimpleKeyword("rohf")
    """SimpleKeyword: Type of the wavefunction: restricted, unrestricted, multireference."""
    ROKS = SimpleKeyword("roks")
    """SimpleKeyword: Type of the wavefunction: restricted, unrestricted, multireference."""
    UHF = SimpleKeyword("uhf")
    """SimpleKeyword: Type of the wavefunction: restricted, unrestricted, multireference."""
    UKS = SimpleKeyword("uks")
    """SimpleKeyword: Type of the wavefunction: restricted, unrestricted, multireference."""
    CASSCF = SimpleKeyword("casscf")
    """SimpleKeyword: Type of the wavefunction: restricted, unrestricted, multireference."""
