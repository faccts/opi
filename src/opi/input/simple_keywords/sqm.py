from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Sqm",)


class Sqm(SimpleKeywordBox):
    """Enum to store all simple keywords of type Sqm.

    Attributes
    ----------
    AM1 : SimpleKeyword
        SQM: Semiempirical quantum mechanical methods
    GFN0_XTB : SimpleKeyword
        GFN0-xTB also known as XTB0
    GFN1_XTB : SimpleKeyword
        GFN1-xTB also known as GFN-xTB or XTB1
    GFN2_XTB : SimpleKeyword
        GFN1-xTB also known as XTB or XTB2
    MNDO : SimpleKeyword
        SQM: Semiempirical quantum mechanical methods
    NATIVE_GFN1_XTB : SimpleKeyword
        SQM: Semiempirical quantum mechanical methods
    NATIVE_GFN2_XTB : SimpleKeyword
        SQM: Semiempirical quantum mechanical methods
    NDDO_1 : SimpleKeyword
        SQM: Semiempirical quantum mechanical methods
    NDDO_2 : SimpleKeyword
        SQM: Semiempirical quantum mechanical methods
    NDDO_MK : SimpleKeyword
        SQM: Semiempirical quantum mechanical methods
    NONOTCH : SimpleKeyword
        SQM: Semiempirical quantum mechanical methods
    NOTCH : SimpleKeyword
        SQM: Semiempirical quantum mechanical methods
    PM3 : SimpleKeyword
        SQM: Semiempirical quantum mechanical methods
    ZINDO_1 : SimpleKeyword
        SQM: Semiempirical quantum mechanical methods
    ZINDO_2 : SimpleKeyword
        SQM: Semiempirical quantum mechanical methods
    ZINDO_S : SimpleKeyword
        SQM: Semiempirical quantum mechanical methods
    ZNDDO_1 : SimpleKeyword
        SQM: Semiempirical quantum mechanical methods
    ZNDDO_2 : SimpleKeyword
        SQM: Semiempirical quantum mechanical methods
    """

    AM1 = SimpleKeyword("am1")
    GFN0_XTB = SimpleKeyword("gfn0-xtb")
    GFN1_XTB = SimpleKeyword("gfn1-xtb")
    GFN2_XTB = SimpleKeyword("gfn2-xtb")
    MNDO = SimpleKeyword("mndo")
    NATIVE_GFN1_XTB = SimpleKeyword("native-gfn1-xtb")
    NATIVE_GFN2_XTB = SimpleKeyword("native-gfn2-xtb")
    NDDO_1 = SimpleKeyword("nddo/1")
    NDDO_2 = SimpleKeyword("nddo/2")
    NDDO_MK = SimpleKeyword("nddo/mk")
    NONOTCH = SimpleKeyword("nonotch")
    NOTCH = SimpleKeyword("notch")
    PM3 = SimpleKeyword("pm3")
    ZINDO_1 = SimpleKeyword("zindo/1")
    ZINDO_2 = SimpleKeyword("zindo/2")
    ZINDO_S = SimpleKeyword("zindo/s")
    ZNDDO_1 = SimpleKeyword("znddo/1")
    ZNDDO_2 = SimpleKeyword("znddo/2")
