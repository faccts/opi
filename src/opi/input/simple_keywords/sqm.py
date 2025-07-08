from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Sqm",)


class Sqm(SimpleKeywordBox):
    """Enum to store all simple keywords of type Sqm."""

    AM1 = SimpleKeyword("am1")
    """SimpleKeyword: SQM: Semiempirical quantum mechanical methods."""
    GFN0_XTB = SimpleKeyword("gfn0-xtb")
    """SimpleKeyword: GFN0-xTB also known as XTB0."""
    GFN1_XTB = SimpleKeyword("gfn1-xtb")
    """SimpleKeyword: GFN1-xTB also known as GFN-xTB or XTB1."""
    GFN2_XTB = SimpleKeyword("gfn2-xtb")
    """SimpleKeyword: GFN2-xTB also known as XTB or XTB2."""
    MNDO = SimpleKeyword("mndo")
    """SimpleKeyword: SQM: Semiempirical quantum mechanical methods."""
    NATIVE_GFN1_XTB = SimpleKeyword("native-gfn1-xtb")
    """SimpleKeyword: Native GFN1-xTB also known as GFN-xTB or XTB1."""
    NATIVE_GFN2_XTB = SimpleKeyword("native-gfn2-xtb")
    """SimpleKeyword: Native GFN2-xTB also known as XTB or XTB2."""
    NDDO_1 = SimpleKeyword("nddo/1")
    """SimpleKeyword: SQM: Semiempirical quantum mechanical methods."""
    NDDO_2 = SimpleKeyword("nddo/2")
    """SimpleKeyword: SQM: Semiempirical quantum mechanical methods."""
    NDDO_MK = SimpleKeyword("nddo/mk")
    """SimpleKeyword: SQM: Semiempirical quantum mechanical methods."""
    NONOTCH = SimpleKeyword("nonotch")
    """SimpleKeyword: SQM: Semiempirical quantum mechanical methods."""
    NOTCH = SimpleKeyword("notch")
    """SimpleKeyword: SQM: Semiempirical quantum mechanical methods."""
    PM3 = SimpleKeyword("pm3")
    """SimpleKeyword: SQM: Semiempirical quantum mechanical methods."""
    ZINDO_1 = SimpleKeyword("zindo/1")
    """SimpleKeyword: SQM: Semiempirical quantum mechanical methods."""
    ZINDO_2 = SimpleKeyword("zindo/2")
    """SimpleKeyword: SQM: Semiempirical quantum mechanical methods."""
    ZINDO_S = SimpleKeyword("zindo/s")
    """SimpleKeyword: SQM: Semiempirical quantum mechanical methods."""
    ZNDDO_1 = SimpleKeyword("znddo/1")
    """SimpleKeyword: SQM: Semiempirical quantum mechanical methods."""
    ZNDDO_2 = SimpleKeyword("znddo/2")
    """SimpleKeyword: SQM: Semiempirical quantum mechanical methods."""
