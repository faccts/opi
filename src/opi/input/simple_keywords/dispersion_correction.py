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
        three body term for d3bj
    D2 : SimpleKeyword
        D2
    D3 : SimpleKeyword
        D3
    D3ZERO : SimpleKeyword
        D3 Zero damping
    D3BJ : SimpleKeyword
        D3 with BJ damping
    D3TZ : SimpleKeyword
        Use TZ optimized values damping parameters if available
    D4 : SimpleKeyword
        Use D4 dispersion correction
    NL : SimpleKeyword
        use -NL / -VV10 / -V dispersion correction
    POPDISP : SimpleKeyword
        pairwise dispersion correction analysis
    SCNL : SimpleKeyword
        Use self-consistent nl
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
