from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Esd",)


class Esd(SimpleKeywordBox):
    """Enum to store all simple keywords of type Esd."""

    ESD = SimpleKeyword("esd")
    """SimpleKeyword: Check for excited state dynamics calculation."""
    ESD_ABS = SimpleKeyword("esd(abs)")
    """SimpleKeyword: Check for excited state dynamics calculation."""
    ESD_CPF = SimpleKeyword("esd(cpf)")
    """SimpleKeyword: Check for excited state dynamics calculation."""
    ESD_CPP = SimpleKeyword("esd(cpp)")
    """SimpleKeyword: Check for excited state dynamics calculation."""
    ESD_ECD = SimpleKeyword("esd(ecd)")
    """SimpleKeyword: Check for excited state dynamics calculation."""
    ESD_FLUOR = SimpleKeyword("esd(fluor)")
    """SimpleKeyword: Check for excited state dynamics calculation."""
    ESD_IC = SimpleKeyword("esd(ic)")
    """SimpleKeyword: Check for excited state dynamics calculation."""
    ESD_ISC = SimpleKeyword("esd(isc)")
    """SimpleKeyword: Check for excited state dynamics calculation."""
    ESD_MCD = SimpleKeyword("esd(mcd)")
    """SimpleKeyword: Check for excited state dynamics calculation."""
    ESD_PHOSP = SimpleKeyword("esd(phosp)")
    """SimpleKeyword: Check for excited state dynamics calculation."""
    ESD_RR = SimpleKeyword("esd(rr)")
    """SimpleKeyword: Check for excited state dynamics calculation."""
    ESD_RRAMAN = SimpleKeyword("esd(rraman)")
    """SimpleKeyword: Check for excited state dynamics calculation."""
