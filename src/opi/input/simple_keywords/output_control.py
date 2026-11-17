from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("OutputControl",)


class OutputControl(SimpleKeywordBox):
    """Enum to store all simple keywords of type OutputControl."""

    MINIPRINT = ORCAKeyword("miniprint")
    """ORCAKeyword: OutputControl."""
    SMALLPRINT = ORCAKeyword("smallprint")
    """ORCAKeyword: OutputControl."""
    NORMALPRINT = ORCAKeyword("normalprint")
    """ORCAKeyword: OutputControl."""
    LARGEPRINT = ORCAKeyword("largeprint")
    """ORCAKeyword: OutputControl."""
    SCFSOLVERTIME = ORCAKeyword("scfsolvertime")
    """ORCAKeyword: OutputControl."""
    PRINTGAP = ORCAKeyword("printgap")
    """ORCAKeyword: OutputControl."""
    PRINTMOS = ORCAKeyword("printmos")
    """ORCAKeyword: OutputControl."""
    PRINTBASIS = ORCAKeyword("printbasis")
    """ORCAKeyword: printbas."""
    GRIDPRINT = ORCAKeyword("gridprint")
    """ORCAKeyword: Print grid information."""
    WRITEONLYINITIALPROPFILE = ORCAKeyword("writeonlyinitialpropfile")
    """ORCAKeyword: Only write property file for first geometry."""
    NOMOPRINT = ORCAKeyword("nomoprint")
    """ORCAKeyword: OutputControl."""
    NOPROPFILE = ORCAKeyword("nopropfile")
    """ORCAKeyword: Write no property file."""
    NOPRINTMOS = ORCAKeyword("noprintmos")
    """ORCAKeyword: OutputControl."""
    POPDISP = ORCAKeyword("popdisp")
    """ORCAKeyword: Pairwise dispersion correction analysis."""
