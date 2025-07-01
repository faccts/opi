from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("ForceField",)


class ForceField(SimpleKeywordBox):
    """Enum to store all simple keywords of type ForceField.

    Attributes
    ----------
    GFN_FF : SimpleKeyword
        GFN-FF (external) alias is xtb-ff
    MM : SimpleKeyword
        Use external molecular mechanics
    """

    GFN_FF = SimpleKeyword("gfn-ff")
    MM = SimpleKeyword("mm")
