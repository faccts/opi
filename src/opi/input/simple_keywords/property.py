from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Property",)


class Property(SimpleKeywordBox):
    """Enum to store all simple keywords of type Property.

    Attributes
    ----------
    NMR : SimpleKeyword
        Calculate NMR parameters
    G_TENSOR : SimpleKeyword
        Calculate EPR parameters
    UCO : SimpleKeyword
        Property
    NOUCO : SimpleKeyword
        Property
    UNO : SimpleKeyword
        Property
    NOUNO : SimpleKeyword
        Property
    NBO : SimpleKeyword
        Property
    NONBO : SimpleKeyword
        Property
    """

    NMR = SimpleKeyword("nmr")
    G_TENSOR = SimpleKeyword("g-tensor")
    UCO = SimpleKeyword("uco")
    NOUCO = SimpleKeyword("nouco")
    UNO = SimpleKeyword("uno")
    NOUNO = SimpleKeyword("nouno")
    NBO = SimpleKeyword("nbo")
    NONBO = SimpleKeyword("nonbo")
