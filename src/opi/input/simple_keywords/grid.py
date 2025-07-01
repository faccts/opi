from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Grid",)


class Grid(SimpleKeywordBox):
    """Enum to store all simple keywords of type Grid.

    Attributes
    ----------
    DEFGRID1 : SimpleKeyword
        small grid
    DEFGRID2 : SimpleKeyword
        medium grid
    DEFGRID3 : SimpleKeyword
        large grid
    REFGRID : SimpleKeyword
        reference grid
    ROTINVGRID : SimpleKeyword
        Rotational invariant grid
    """

    DEFGRID1 = SimpleKeyword("defgrid1")
    DEFGRID2 = SimpleKeyword("defgrid2")
    DEFGRID3 = SimpleKeyword("defgrid3")
    REFGRID = SimpleKeyword("refgrid")
    ROTINVGRID = SimpleKeyword("rotinvgrid")
