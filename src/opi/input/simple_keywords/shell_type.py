from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("ShellType",)


class ShellType(SimpleKeywordBox):
    """Enum to store all simple keywords of type ShellType."""

    RHF = ORCAKeyword("rhf")
    """ORCAKeyword: Type of the wavefunction: restricted, unrestricted, multireference."""
    RKS = ORCAKeyword("rks")
    """ORCAKeyword: Type of the wavefunction: restricted, unrestricted, multireference."""
    ROHF = ORCAKeyword("rohf")
    """ORCAKeyword: Type of the wavefunction: restricted, unrestricted, multireference."""
    ROKS = ORCAKeyword("roks")
    """ORCAKeyword: Type of the wavefunction: restricted, unrestricted, multireference."""
    UHF = ORCAKeyword("uhf")
    """ORCAKeyword: Type of the wavefunction: restricted, unrestricted, multireference."""
    UKS = ORCAKeyword("uks")
    """ORCAKeyword: Type of the wavefunction: restricted, unrestricted, multireference."""
    CASSCF = ORCAKeyword("casscf")
    """ORCAKeyword: Type of the wavefunction: restricted, unrestricted, multireference."""
