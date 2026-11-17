from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("ForceField",)


class ForceField(SimpleKeywordBox):
    """Enum to store all simple keywords of type ForceField."""

    GFN_FF = ORCAKeyword("gfn-ff")
    """ORCAKeyword: GFN-FF (external) alias is xtb-ff."""
    MM = ORCAKeyword("mm")
    """ORCAKeyword: Use external molecular mechanics."""
