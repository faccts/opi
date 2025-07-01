from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("ShellType",)


class ShellType(SimpleKeywordBox):
    """Enum to store all simple keywords of type ShellType.

    Attributes
    ----------
    RHF : SimpleKeyword
        Type of the wavefunction: restricted, unrestricted, multireference
    RKS : SimpleKeyword
        Type of the wavefunction: restricted, unrestricted, multireference
    ROHF : SimpleKeyword
        Type of the wavefunction: restricted, unrestricted, multireference
    ROKS : SimpleKeyword
        Type of the wavefunction: restricted, unrestricted, multireference
    UHF : SimpleKeyword
        Type of the wavefunction: restricted, unrestricted, multireference
    UKS : SimpleKeyword
        Type of the wavefunction: restricted, unrestricted, multireference
    CASSCF : SimpleKeyword
        Type of the wavefunction: restricted, unrestricted, multireference
    """

    RHF = SimpleKeyword("rhf")
    RKS = SimpleKeyword("rks")
    ROHF = SimpleKeyword("rohf")
    ROKS = SimpleKeyword("roks")
    UHF = SimpleKeyword("uhf")
    UKS = SimpleKeyword("uks")
    CASSCF = SimpleKeyword("casscf")
