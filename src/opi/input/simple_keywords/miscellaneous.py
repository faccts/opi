from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Miscellaneous",)


class Miscellaneous(SimpleKeywordBox):
    """Enum to store all simple keywords of type Miscellaneous.

    Attributes
    ----------
    ANGS : SimpleKeyword
        Miscellaneous
    BOHRS : SimpleKeyword
        Miscellaneous
    CHEAPINTS : SimpleKeyword
        Miscellaneous
    KEEPDENS : SimpleKeyword
        Miscellaneous
    KEEPDENSITY : SimpleKeyword
        Miscellaneous
    KEEPFOCK : SimpleKeyword
        Miscellaneous
    KEEPINTS : SimpleKeyword
        Miscellaneous
    KEEPRESPDENSITY : SimpleKeyword
        Miscellaneous
    KEEPTRANSDENSITY : SimpleKeyword
        Miscellaneous
    LIBINT : SimpleKeyword
        Libint for Integral generation
    MASS2016 : SimpleKeyword
        Miscellaneous
    NOCHEAPINTS : SimpleKeyword
        Miscellaneous
    NOKEEPDENS : SimpleKeyword
        Miscellaneous
    NOKEEPDENSITY : SimpleKeyword
        Miscellaneous
    NOKEEPFOCK : SimpleKeyword
        Miscellaneous
    NOKEEPINTS : SimpleKeyword
        Miscellaneous
    NOLIBINT : SimpleKeyword
        Libint for Integral generation
    NOREADINTS : SimpleKeyword
        Miscellaneous
    NOSHARK : SimpleKeyword
        Shark for integral generation
    NOSYM : SimpleKeyword
        Symmetry keywords
    NOSYMMETRY : SimpleKeyword
        Symmetry keywords
    NOUSESHARK : SimpleKeyword
        Shark for integral generation
    NOUSESYM : SimpleKeyword
        Symmetry keywords
    NOUSESYMMETRY : SimpleKeyword
        Symmetry keywords
    NOXCFUN : SimpleKeyword
        do not use Xcfun library
    PAL : SimpleKeyword
        Parallelization
    PAL16 : SimpleKeyword
        Parallelization
    PAL16_4X4 : SimpleKeyword
        Parallelization
    PAL2 : SimpleKeyword
        Parallelization
    PAL3 : SimpleKeyword
        Parallelization
    PAL32 : SimpleKeyword
        Parallelization
    PAL32_4X8 : SimpleKeyword
        Parallelization
    PAL32_8X4 : SimpleKeyword
        Parallelization
    PAL4 : SimpleKeyword
        Parallelization
    PAL4_2X2 : SimpleKeyword
        Parallelization
    PAL5 : SimpleKeyword
        Parallelization
    PAL6 : SimpleKeyword
        Parallelization
    PAL64 : SimpleKeyword
        Parallelization
    PAL64_8X8 : SimpleKeyword
        Parallelization
    PAL7 : SimpleKeyword
        Parallelization
    PAL8 : SimpleKeyword
        Parallelization
    PAL8_2X4 : SimpleKeyword
        Parallelization
    PAL8_4X2 : SimpleKeyword
        Parallelization
    PREFERC2V : SimpleKeyword
        Symmetry keywords
    PREFERD2 : SimpleKeyword
        Symmetry keywords
    READINTS : SimpleKeyword
        Miscellaneous
    RESCUE : SimpleKeyword
        Try to rescue a calculation from an old orca version
    SCALEPC : SimpleKeyword
        Scale Pointcharges
    SHARK : SimpleKeyword
        Shark for integral generation
    USEC2V : SimpleKeyword
        Symmetry keywords
    USED2 : SimpleKeyword
        Symmetry keywords
    USESHARK : SimpleKeyword
        Shark for integral generation
    USESYM : SimpleKeyword
        Symmetry keywords
    USESYMMETRY : SimpleKeyword
        Symmetry keywords
    XCFUN : SimpleKeyword
        Use Xcfun library
    PAF : SimpleKeyword
        Bring molecule into its principle axis orientation
    ALLOWRHF : SimpleKeyword
        AllowRHF for open-shell
    NOALLOWRHF : SimpleKeyword
        AllowRHF for open-shell
    DOEQ : SimpleKeyword
        Do Eq for nuclear charges
    NOEQ : SimpleKeyword
        Do not Eq for nuclear charges
    BPOP : SimpleKeyword
        Use Boltzmann weighting in multiple xyz job
    NUMGRAD : SimpleKeyword
        Numerical gradient
    SURFCROSSNUMFREQ : SimpleKeyword
        Check for surface crossing frequency
    MECP_NUMFREQ : SimpleKeyword
        Numerical MECP freq
    NEARIR : SimpleKeyword
        VPT2 analysis for nearIR
    VPT2 : SimpleKeyword
        VPT2 analysis
    """

    ANGS = SimpleKeyword("angs")
    BOHRS = SimpleKeyword("bohrs")
    CHEAPINTS = SimpleKeyword("cheapints")
    KEEPDENS = SimpleKeyword("keepdens")
    KEEPDENSITY = SimpleKeyword("keepdensity")
    KEEPFOCK = SimpleKeyword("keepfock")
    KEEPINTS = SimpleKeyword("keepints")
    KEEPRESPDENSITY = SimpleKeyword("keeprespdensity")
    KEEPTRANSDENSITY = SimpleKeyword("keeptransdensity")
    LIBINT = SimpleKeyword("libint")
    MASS2016 = SimpleKeyword("mass2016")
    NOCHEAPINTS = SimpleKeyword("nocheapints")
    NOKEEPDENS = SimpleKeyword("nokeepdens")
    NOKEEPDENSITY = SimpleKeyword("nokeepdensity")
    NOKEEPFOCK = SimpleKeyword("nokeepfock")
    NOKEEPINTS = SimpleKeyword("nokeepints")
    NOLIBINT = SimpleKeyword("nolibint")
    NOREADINTS = SimpleKeyword("noreadints")
    NOSHARK = SimpleKeyword("noshark")
    NOSYM = SimpleKeyword("nosym")
    NOSYMMETRY = SimpleKeyword("nosymmetry")
    NOUSESHARK = SimpleKeyword("nouseshark")
    NOUSESYM = SimpleKeyword("nousesym")
    NOUSESYMMETRY = SimpleKeyword("nousesymmetry")
    NOXCFUN = SimpleKeyword("noxcfun")
    PAL = SimpleKeyword("pal")
    PAL16 = SimpleKeyword("pal16")
    PAL16_4X4 = SimpleKeyword("pal16(4x4)")
    PAL2 = SimpleKeyword("pal2")
    PAL3 = SimpleKeyword("pal3")
    PAL32 = SimpleKeyword("pal32")
    PAL32_4X8 = SimpleKeyword("pal32(4x8)")
    PAL32_8X4 = SimpleKeyword("pal32(8x4)")
    PAL4 = SimpleKeyword("pal4")
    PAL4_2X2 = SimpleKeyword("pal4(2x2)")
    PAL5 = SimpleKeyword("pal5")
    PAL6 = SimpleKeyword("pal6")
    PAL64 = SimpleKeyword("pal64")
    PAL64_8X8 = SimpleKeyword("pal64(8x8)")
    PAL7 = SimpleKeyword("pal7")
    PAL8 = SimpleKeyword("pal8")
    PAL8_2X4 = SimpleKeyword("pal8(2x4)")
    PAL8_4X2 = SimpleKeyword("pal8(4x2)")
    PREFERC2V = SimpleKeyword("preferc2v")
    PREFERD2 = SimpleKeyword("preferd2")
    READINTS = SimpleKeyword("readints")
    RESCUE = SimpleKeyword("rescue")
    SCALEPC = SimpleKeyword("scalepc")
    SHARK = SimpleKeyword("shark")
    USEC2V = SimpleKeyword("usec2v")
    USED2 = SimpleKeyword("used2")
    USESHARK = SimpleKeyword("useshark")
    USESYM = SimpleKeyword("usesym")
    USESYMMETRY = SimpleKeyword("usesymmetry")
    XCFUN = SimpleKeyword("xcfun")
    PAF = SimpleKeyword("paf")
    ALLOWRHF = SimpleKeyword("allowrhf")
    NOALLOWRHF = SimpleKeyword("noallowrhf")
    DOEQ = SimpleKeyword("doeq")
    NOEQ = SimpleKeyword("noeq")
    BPOP = SimpleKeyword("bpop")
    NUMGRAD = SimpleKeyword("numgrad")
    SURFCROSSNUMFREQ = SimpleKeyword("surfcrossnumfreq")
    MECP_NUMFREQ = SimpleKeyword("mecp-numfreq")
    NEARIR = SimpleKeyword("nearir")
    VPT2 = SimpleKeyword("vpt2")
