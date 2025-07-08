from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("ForceField",)


class ForceField(SimpleKeywordBox):
    """Enum to store all simple keywords of type ForceField."""

    GFN_FF = SimpleKeyword("gfn-ff")
    """SimpleKeyword: GFN-FF (external) alias is xtb-ff."""
    MM = SimpleKeyword("mm")
    """SimpleKeyword: Use external molecular mechanics."""
