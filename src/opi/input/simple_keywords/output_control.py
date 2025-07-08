from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("OutputControl",)


class OutputControl(SimpleKeywordBox):
    """Enum to store all simple keywords of type OutputControl."""

    MINIPRINT = SimpleKeyword("miniprint")
    """SimpleKeyword: OutputControl."""
    SMALLPRINT = SimpleKeyword("smallprint")
    """SimpleKeyword: OutputControl."""
    NORMALPRINT = SimpleKeyword("normalprint")
    """SimpleKeyword: OutputControl."""
    LARGEPRINT = SimpleKeyword("largeprint")
    """SimpleKeyword: OutputControl."""
    SCFSOLVERTIME = SimpleKeyword("scfsolvertime")
    """SimpleKeyword: OutputControl."""
    PRINTGAP = SimpleKeyword("printgap")
    """SimpleKeyword: OutputControl."""
    PRINTMOS = SimpleKeyword("printmos")
    """SimpleKeyword: OutputControl."""
    PRINTBASIS = SimpleKeyword("printbasis")
    """SimpleKeyword: printbas."""
    GRIDPRINT = SimpleKeyword("gridprint")
    """SimpleKeyword: Print grid information."""
    WRITEONLYINITIALPROPFILE = SimpleKeyword("writeonlyinitialpropfile")
    """SimpleKeyword: Only write property file for first geometry."""
    NOMOPRINT = SimpleKeyword("nomoprint")
    """SimpleKeyword: OutputControl."""
    NOPROPFILE = SimpleKeyword("nopropfile")
    """SimpleKeyword: Write no property file."""
    NOPRINTMOS = SimpleKeyword("noprintmos")
    """SimpleKeyword: OutputControl."""
