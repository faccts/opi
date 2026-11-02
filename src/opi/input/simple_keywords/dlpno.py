from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Dlpno",)


class PNOThresh(SimpleKeywordBox):
    LOOSEPNO = ORCAKeyword("loosepno")
    """ORCAKeyword: Select loose PNO settings.."""
    NORMALPNO = ORCAKeyword("normalpno")
    """ORCAKeyword: Select normal PNO settings.."""
    TIGHTPNO = ORCAKeyword("tightpno")
    """ORCAKeyword: Select Tight PNO settings.."""


class Dlpno(PNOThresh):
    """Enum to store all simple keywords of type Dlpno."""

    HFLD = ORCAKeyword("hfld")
    """ORCAKeyword: HF + Dispersion energy."""
    LED = ORCAKeyword("led")
    """ORCAKeyword: Energy decomposition for DLPNO-CC methods.."""
    ADLD = ORCAKeyword("adld")
    """ORCAKeyword: Atomic decomposition of the London Dispersion energy.."""
    ADEX = ORCAKeyword("adex")
    """ORCAKeyword: Atomic decomposition of the Exchange."""
    PNOEXTRAPOLATION = ORCAKeyword("pnoextrapolation")
    """ORCAKeyword: Automatic extrapolation of PNO space.."""
