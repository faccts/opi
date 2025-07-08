from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Property",)


class Property(SimpleKeywordBox):
    """Enum to store all simple keywords of type Property."""

    NMR = SimpleKeyword("nmr")
    """SimpleKeyword: Calculate NMR parameters."""
    G_TENSOR = SimpleKeyword("g-tensor")
    """SimpleKeyword: Calculate EPR parameters."""
    UCO = SimpleKeyword("uco")
    """SimpleKeyword: Property."""
    NOUCO = SimpleKeyword("nouco")
    """SimpleKeyword: Property."""
    UNO = SimpleKeyword("uno")
    """SimpleKeyword: Property."""
    NOUNO = SimpleKeyword("nouno")
    """SimpleKeyword: Property."""
    NBO = SimpleKeyword("nbo")
    """SimpleKeyword: Property."""
    NONBO = SimpleKeyword("nonbo")
    """SimpleKeyword: Property."""
