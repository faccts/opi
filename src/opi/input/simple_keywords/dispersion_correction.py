from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("DispersionCorrection",)


class DispersionCorrection(SimpleKeywordBox):
    """Enum to store all simple keywords of type DispersionCorrection."""

    ABC = ORCAKeyword("abc")
    """ORCAKeyword: Use three body term, applicable together with D3BJ.."""
    D2 = ORCAKeyword("d2")
    """ORCAKeyword: D2 - Dispersion correction.."""
    D3 = ORCAKeyword("d3")
    """ORCAKeyword: D3 - Dispersion correction.."""
    D3ZERO = ORCAKeyword("d3zero")
    """ORCAKeyword: D3 - Dispersion correction with zero damping.."""
    D3BJ = ORCAKeyword("d3bj")
    """ORCAKeyword: D3 - Dispersion correction with Becke-Johnson damping."""
    D3TZ = ORCAKeyword("d3tz")
    """ORCAKeyword: Use TZ optimized damping parameters if available."""
    D4 = ORCAKeyword("d4")
    """ORCAKeyword: D4 - Dispersion correction with three body term and Becke-Johnson damping."""
    NL = ORCAKeyword("nl")
    """ORCAKeyword: Use -NL / -VV10 / -V dispersion correction."""
    SCNL = ORCAKeyword("scnl")
    """ORCAKeyword: Use self-consistent NL."""
