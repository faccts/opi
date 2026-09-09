from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Grid",)


class Grid(SimpleKeywordBox):
    """Enum to store all simple keywords of type Grid."""

    DEFGRID1 = SimpleKeyword("defgrid1", alias="1")
    """SimpleKeyword: small grid."""
    DEFGRID2 = SimpleKeyword("defgrid2", alias="2")
    """SimpleKeyword: medium grid."""
    DEFGRID3 = SimpleKeyword("defgrid3", alias="3")
    """SimpleKeyword: large grid."""
    REFGRID = SimpleKeyword("refgrid")
    """SimpleKeyword: reference grid."""
    ROTINVGRID = SimpleKeyword("rotinvgrid")
    """SimpleKeyword: Rotational invariant grid."""
