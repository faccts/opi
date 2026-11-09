from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Esd",)


class Esd(SimpleKeywordBox):
    """Enum to store all simple keywords of type Esd."""

    ESD = ORCAKeyword("esd")
    """ORCAKeyword: Check for excited state dynamics calculation."""
    ESD_ABS = ORCAKeyword("esd(abs)")
    """ORCAKeyword: Check for excited state dynamics calculation."""
    ESD_CPF = ORCAKeyword("esd(cpf)")
    """ORCAKeyword: Check for excited state dynamics calculation."""
    ESD_CPP = ORCAKeyword("esd(cpp)")
    """ORCAKeyword: Check for excited state dynamics calculation."""
    ESD_ECD = ORCAKeyword("esd(ecd)")
    """ORCAKeyword: Check for excited state dynamics calculation."""
    ESD_FLUOR = ORCAKeyword("esd(fluor)")
    """ORCAKeyword: Check for excited state dynamics calculation."""
    ESD_IC = ORCAKeyword("esd(ic)")
    """ORCAKeyword: Check for excited state dynamics calculation."""
    ESD_ISC = ORCAKeyword("esd(isc)")
    """ORCAKeyword: Check for excited state dynamics calculation."""
    ESD_MCD = ORCAKeyword("esd(mcd)")
    """ORCAKeyword: Check for excited state dynamics calculation."""
    ESD_PHOSP = ORCAKeyword("esd(phosp)")
    """ORCAKeyword: Check for excited state dynamics calculation."""
    ESD_RR = ORCAKeyword("esd(rr)")
    """ORCAKeyword: Check for excited state dynamics calculation."""
    ESD_RRAMAN = ORCAKeyword("esd(rraman)")
    """ORCAKeyword: Check for excited state dynamics calculation."""
