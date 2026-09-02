from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Dlpno",)


class PNOThresh(SimpleKeywordBox):
    LOOSEPNO = SimpleKeyword("loosepno")
    """SimpleKeyword: Select loose PNO settings.."""
    NORMALPNO = SimpleKeyword("normalpno")
    """SimpleKeyword: Select normal PNO settings.."""
    TIGHTPNO = SimpleKeyword("tightpno")
    """SimpleKeyword: Select Tight PNO settings.."""


class Dlpno(PNOThresh):
    """Enum to store all simple keywords of type Dlpno."""

    HFLD = SimpleKeyword("hfld")
    """SimpleKeyword: HF + Dispersion energy."""
    LED = SimpleKeyword("led")
    """SimpleKeyword: Energy decomposition for DLPNO-CC methods.."""
    ADLD = SimpleKeyword("adld")
    """SimpleKeyword: Atomic decomposition of the London Dispersion energy.."""
    ADEX = SimpleKeyword("adex")
    """SimpleKeyword: Atomic decomposition of the Exchange."""
    PNOEXTRAPOLATION = SimpleKeyword("pnoextrapolation")
    """SimpleKeyword: Automatic extrapolation of PNO space.."""
