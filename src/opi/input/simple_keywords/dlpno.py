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
        HF + Dispersion energy
    LED : SimpleKeyword
        Energy decomposition for DLPNO-CC methods.
    LOOSEPNO : SimpleKeyword
        Select loose PNO settings.
    NORMALPNO : SimpleKeyword
        Select normal PNO settings.
    TIGHTPNO : SimpleKeyword
        Select Tight PNO settings.
    ADLD : SimpleKeyword
        Atomic decomposition of the London Dispersion energy.
    PNOEXTRAPOLATION : SimpleKeyword
        Automatic extrapolation of PNO space.
    """

    HFLD = SimpleKeyword("hfld")
    LED = SimpleKeyword("led")
    LOOSEPNO = SimpleKeyword("loosepno")
    NORMALPNO = SimpleKeyword("normalpno")
    TIGHTPNO = SimpleKeyword("tightpno")
    ADLD = SimpleKeyword("adld")
    PNOEXTRAPOLATION = SimpleKeyword("pnoextrapolation")
