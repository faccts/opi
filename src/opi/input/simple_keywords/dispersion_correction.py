from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("DispersionCorrection",)


class DispersionCorrection(SimpleKeywordBox):
    """Enum to store all simple keywords of type DispersionCorrection.

    Attributes
    ----------
    ABC : SimpleKeyword
        Use three body term, applicable together with D3BJ.
    D2 : SimpleKeyword
        D2 - Dispersion correction.
    D3 : SimpleKeyword
        D3 - Dispersion correction.
    D3ZERO : SimpleKeyword
        D3 - Dispersion correction with zero damping.
    D3BJ : SimpleKeyword
        D3 - Dispersion correction with Becke-Johnson damping
    D3TZ : SimpleKeyword
        Use TZ optimized damping parameters if available
    D4 : SimpleKeyword
        D4 - Dispersion correction with three body term and Becke-Johnson damping
    NL : SimpleKeyword
        Use -NL / -VV10 / -V dispersion correction
    POPDISP : SimpleKeyword
        Pairwise dispersion correction analysis
    SCNL : SimpleKeyword
        Use self-consistent NL
    """

    ABC = SimpleKeyword("abc")
    D2 = SimpleKeyword("d2")
    D3 = SimpleKeyword("d3")
    D3ZERO = SimpleKeyword("d3zero")
    D3BJ = SimpleKeyword("d3bj")
    D3TZ = SimpleKeyword("d3tz")
    D4 = SimpleKeyword("d4")
    NL = SimpleKeyword("nl")
    POPDISP = SimpleKeyword("popdisp")
    SCNL = SimpleKeyword("scnl")
