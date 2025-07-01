from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("OutputControl",)


class OutputControl(SimpleKeywordBox):
    """Enum to store all simple keywords of type OutputControl.

    Attributes
    ----------
    MINIPRINT : SimpleKeyword
        OutputControl
    SMALLPRINT : SimpleKeyword
        OutputControl
    NORMALPRINT : SimpleKeyword
        OutputControl
    LARGEPRINT : SimpleKeyword
        OutputControl
    SCFSOLVERTIME : SimpleKeyword
        OutputControl
    PRINTGAP : SimpleKeyword
        OutputControl
    PRINTMOS : SimpleKeyword
        OutputControl
    PRINTBASIS : SimpleKeyword
        printbas
    GRIDPRINT : SimpleKeyword
        Print grid information
    WRITEONLYINITIALPROPFILE : SimpleKeyword
        Only write property file for first geometry
    NOMOPRINT : SimpleKeyword
        OutputControl
    NOPROPFILE : SimpleKeyword
        Write no property file
    NOPRINTMOS : SimpleKeyword
        OutputControl
    """

    MINIPRINT = SimpleKeyword("miniprint")
    SMALLPRINT = SimpleKeyword("smallprint")
    NORMALPRINT = SimpleKeyword("normalprint")
    LARGEPRINT = SimpleKeyword("largeprint")
    SCFSOLVERTIME = SimpleKeyword("scfsolvertime")
    PRINTGAP = SimpleKeyword("printgap")
    PRINTMOS = SimpleKeyword("printmos")
    PRINTBASIS = SimpleKeyword("printbasis")
    GRIDPRINT = SimpleKeyword("gridprint")
    WRITEONLYINITIALPROPFILE = SimpleKeyword("writeonlyinitialpropfile")
    NOMOPRINT = SimpleKeyword("nomoprint")
    NOPROPFILE = SimpleKeyword("nopropfile")
    NOPRINTMOS = SimpleKeyword("noprintmos")
