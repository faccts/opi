from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Sqm",)


class Sqm(SimpleKeywordBox):
    """Enum to store all simple keywords of type Sqm."""

    AM1 = ORCAKeyword("am1")
    """ORCAKeyword: SQM: Semiempirical quantum mechanical methods."""
    GFN0_XTB = ORCAKeyword("gfn0-xtb")
    """ORCAKeyword: GFN0-xTB also known as XTB0."""
    GFN1_XTB = ORCAKeyword("gfn1-xtb")
    """ORCAKeyword: GFN1-xTB also known as GFN-xTB or XTB1."""
    GFN2_XTB = ORCAKeyword("gfn2-xtb")
    """ORCAKeyword: GFN2-xTB also known as XTB or XTB2."""
    MNDO = ORCAKeyword("mndo")
    """ORCAKeyword: SQM: Semiempirical quantum mechanical methods."""
    NATIVE_GFN1_XTB = ORCAKeyword("native-gfn1-xtb")
    """ORCAKeyword: Native GFN1-xTB also known as GFN-xTB or XTB1."""
    NATIVE_GFN2_XTB = ORCAKeyword("native-gfn2-xtb")
    """ORCAKeyword: Native GFN2-xTB also known as XTB or XTB2."""
    NDDO_1 = ORCAKeyword("nddo/1")
    """ORCAKeyword: SQM: Semiempirical quantum mechanical methods."""
    NDDO_2 = ORCAKeyword("nddo/2")
    """ORCAKeyword: SQM: Semiempirical quantum mechanical methods."""
    NDDO_MK = ORCAKeyword("nddo/mk")
    """ORCAKeyword: SQM: Semiempirical quantum mechanical methods."""
    NONOTCH = ORCAKeyword("nonotch")
    """ORCAKeyword: SQM: Semiempirical quantum mechanical methods."""
    NOTCH = ORCAKeyword("notch")
    """ORCAKeyword: SQM: Semiempirical quantum mechanical methods."""
    PM3 = ORCAKeyword("pm3")
    """ORCAKeyword: SQM: Semiempirical quantum mechanical methods."""
    ZINDO_1 = ORCAKeyword("zindo/1")
    """ORCAKeyword: SQM: Semiempirical quantum mechanical methods."""
    ZINDO_2 = ORCAKeyword("zindo/2")
    """ORCAKeyword: SQM: Semiempirical quantum mechanical methods."""
    ZINDO_S = ORCAKeyword("zindo/s")
    """ORCAKeyword: SQM: Semiempirical quantum mechanical methods."""
    ZNDDO_1 = ORCAKeyword("znddo/1")
    """ORCAKeyword: SQM: Semiempirical quantum mechanical methods."""
    ZNDDO_2 = ORCAKeyword("znddo/2")
    """ORCAKeyword: SQM: Semiempirical quantum mechanical methods."""
