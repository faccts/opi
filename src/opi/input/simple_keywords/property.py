from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Property",)


class Property(SimpleKeywordBox):
    """Enum to store all simple keywords of type Property."""

    NMR = ORCAKeyword("nmr")
    """ORCAKeyword: Calculate NMR parameters."""
    G_TENSOR = ORCAKeyword("g-tensor")
    """ORCAKeyword: Calculate EPR parameters."""
    UCO = ORCAKeyword("uco")
    """ORCAKeyword: Property."""
    NOUCO = ORCAKeyword("nouco")
    """ORCAKeyword: Property."""
    UNO = ORCAKeyword("uno")
    """ORCAKeyword: Property."""
    NOUNO = ORCAKeyword("nouno")
    """ORCAKeyword: Property."""
    NBO = ORCAKeyword("nbo")
    """ORCAKeyword: Property."""
    NONBO = ORCAKeyword("nonbo")
    """ORCAKeyword: Property."""
