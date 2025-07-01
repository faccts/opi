from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Esd",)


class Esd(SimpleKeywordBox):
    """Enum to store all simple keywords of type Esd.

    Attributes
    ----------
    ESD : SimpleKeyword
        Check for excited state dynamics calculation
    ESD_ABS : SimpleKeyword
        Check for excited state dynamics calculation
    ESD_CPF : SimpleKeyword
        Check for excited state dynamics calculation
    ESD_CPP : SimpleKeyword
        Check for excited state dynamics calculation
    ESD_ECD : SimpleKeyword
        Check for excited state dynamics calculation
    ESD_FLUOR : SimpleKeyword
        Check for excited state dynamics calculation
    ESD_IC : SimpleKeyword
        Check for excited state dynamics calculation
    ESD_ISC : SimpleKeyword
        Check for excited state dynamics calculation
    ESD_MCD : SimpleKeyword
        Check for excited state dynamics calculation
    ESD_PHOSP : SimpleKeyword
        Check for excited state dynamics calculation
    ESD_RR : SimpleKeyword
        Check for excited state dynamics calculation
    ESD_RRAMAN : SimpleKeyword
        Check for excited state dynamics calculation
    """

    ESD = SimpleKeyword("esd")
    ESD_ABS = SimpleKeyword("esd(abs)")
    ESD_CPF = SimpleKeyword("esd(cpf)")
    ESD_CPP = SimpleKeyword("esd(cpp)")
    ESD_ECD = SimpleKeyword("esd(ecd)")
    ESD_FLUOR = SimpleKeyword("esd(fluor)")
    ESD_IC = SimpleKeyword("esd(ic)")
    ESD_ISC = SimpleKeyword("esd(isc)")
    ESD_MCD = SimpleKeyword("esd(mcd)")
    ESD_PHOSP = SimpleKeyword("esd(phosp)")
    ESD_RR = SimpleKeyword("esd(rr)")
    ESD_RRAMAN = SimpleKeyword("esd(rraman)")
