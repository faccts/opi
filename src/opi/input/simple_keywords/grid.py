from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Grid",)


class Grid(SimpleKeywordBox):
    """Enum to store all simple keywords of type Grid."""

    DEFGRID1 = ORCAKeyword("defgrid1", alias="1")
    """ORCAKeyword: small grid."""
    DEFGRID2 = ORCAKeyword("defgrid2", alias="2")
    """ORCAKeyword: medium grid."""
    DEFGRID3 = ORCAKeyword("defgrid3", alias="3")
    """ORCAKeyword: large grid."""
    REFGRID = ORCAKeyword("refgrid")
    """ORCAKeyword: reference grid."""
    ROTINVGRID = ORCAKeyword("rotinvgrid")
    """ORCAKeyword: Rotational invariant grid."""
