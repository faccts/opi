from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Dlpno",)


class Dlpno(SimpleKeywordBox):
    """Enum to store all simple keywords of type Dlpno.

    Attributes
    ----------
    HFLD : SimpleKeyword
        HF + Dispersion energy decomposition  as cheaper alternative to DLPNO-CCSD(T) LED
    LED : SimpleKeyword
        Energy decomposition for DLPNO-CCSD(T)
    LOOSEPNO : SimpleKeyword
        loose PNO settings
    NORMALPNO : SimpleKeyword
        normal PNO settings
    TIGHTPNO : SimpleKeyword
        Tight PNO settings
    ADLD : SimpleKeyword
        Dlpno
    PNOEXTRAPOLATION : SimpleKeyword
        automatic extrapolation of PNO space
    """

    HFLD = SimpleKeyword("hfld")
    LED = SimpleKeyword("led")
    LOOSEPNO = SimpleKeyword("loosepno")
    NORMALPNO = SimpleKeyword("normalpno")
    TIGHTPNO = SimpleKeyword("tightpno")
    ADLD = SimpleKeyword("adld")
    PNOEXTRAPOLATION = SimpleKeyword("pnoextrapolation")
