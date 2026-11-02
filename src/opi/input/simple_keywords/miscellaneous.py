from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Miscellaneous",)


class Miscellaneous(SimpleKeywordBox):
    """Enum to store all simple keywords of type Miscellaneous."""

    ANGS = ORCAKeyword("angs")
    """ORCAKeyword: Miscellaneous."""
    BOHRS = ORCAKeyword("bohrs")
    """ORCAKeyword: Miscellaneous."""
    CHEAPINTS = ORCAKeyword("cheapints")
    """ORCAKeyword: Miscellaneous."""
    KEEPDENSITY = ORCAKeyword("keepdensity")
    """ORCAKeyword: Miscellaneous."""
    KEEPFOCK = ORCAKeyword("keepfock")
    """ORCAKeyword: Miscellaneous."""
    KEEPINTS = ORCAKeyword("keepints")
    """ORCAKeyword: Miscellaneous."""
    KEEPRESPDENSITY = ORCAKeyword("keeprespdensity")
    """ORCAKeyword: Miscellaneous."""
    KEEPTRANSDENSITY = ORCAKeyword("keeptransdensity")
    """ORCAKeyword: Miscellaneous."""
    LIBINT = ORCAKeyword("libint")
    """ORCAKeyword: Libint for Integral generation."""
    MASS2016 = ORCAKeyword("mass2016")
    """ORCAKeyword: Miscellaneous."""
    NOCHEAPINTS = ORCAKeyword("nocheapints")
    """ORCAKeyword: Miscellaneous."""
    NOKEEPDENSITY = ORCAKeyword("nokeepdensity")
    """ORCAKeyword: Miscellaneous."""
    NOKEEPFOCK = ORCAKeyword("nokeepfock")
    """ORCAKeyword: Miscellaneous."""
    NOKEEPINTS = ORCAKeyword("nokeepints")
    """ORCAKeyword: Miscellaneous."""
    NOLIBINT = ORCAKeyword("nolibint")
    """ORCAKeyword: Libint for Integral generation."""
    NOREADINTS = ORCAKeyword("noreadints")
    """ORCAKeyword: Miscellaneous."""
    NOSHARK = ORCAKeyword("noshark")
    """ORCAKeyword: Shark for integral generation."""
    NOSYM = ORCAKeyword("nosym")
    """ORCAKeyword: Symmetry keywords."""
    NOSYMMETRY = ORCAKeyword("nosymmetry")
    """ORCAKeyword: Symmetry keywords."""
    NOUSESHARK = ORCAKeyword("nouseshark")
    """ORCAKeyword: Shark for integral generation."""
    NOUSESYM = ORCAKeyword("nousesym")
    """ORCAKeyword: Symmetry keywords."""
    NOUSESYMMETRY = ORCAKeyword("nousesymmetry")
    """ORCAKeyword: Symmetry keywords."""
    NOXCFUN = ORCAKeyword("noxcfun")
    """ORCAKeyword: do not use Xcfun library."""
    PREFERC2V = ORCAKeyword("preferc2v")
    """ORCAKeyword: Symmetry keywords."""
    PREFERD2 = ORCAKeyword("preferd2")
    """ORCAKeyword: Symmetry keywords."""
    READINTS = ORCAKeyword("readints")
    """ORCAKeyword: Miscellaneous."""
    RESCUE = ORCAKeyword("rescue")
    """ORCAKeyword: Try to rescue a calculation from an old orca version."""
    SCALEPC = ORCAKeyword("scalepc")
    """ORCAKeyword: Scale Pointcharges."""
    SHARK = ORCAKeyword("shark")
    """ORCAKeyword: Shark for integral generation."""
    USEC2V = ORCAKeyword("usec2v")
    """ORCAKeyword: Symmetry keywords."""
    USED2 = ORCAKeyword("used2")
    """ORCAKeyword: Symmetry keywords."""
    USESHARK = ORCAKeyword("useshark")
    """ORCAKeyword: Shark for integral generation."""
    USESYM = ORCAKeyword("usesym")
    """ORCAKeyword: Symmetry keywords."""
    USESYMMETRY = ORCAKeyword("usesymmetry")
    """ORCAKeyword: Symmetry keywords."""
    XCFUN = ORCAKeyword("xcfun")
    """ORCAKeyword: Use Xcfun library."""
    PAF = ORCAKeyword("paf")
    """ORCAKeyword: Bring molecule into its principle axis orientation."""
    ALLOWRHF = ORCAKeyword("allowrhf")
    """ORCAKeyword: AllowRHF for open-shell."""
    NOALLOWRHF = ORCAKeyword("noallowrhf")
    """ORCAKeyword: AllowRHF for open-shell."""
    DOEQ = ORCAKeyword("doeq")
    """ORCAKeyword: Do Eq for nuclear charges."""
    NOEQ = ORCAKeyword("noeq")
    """ORCAKeyword: Do not Eq for nuclear charges."""
    BPOP = ORCAKeyword("bpop")
    """ORCAKeyword: Use Boltzmann weighting in multiple xyz job."""
    NUMGRAD = ORCAKeyword("numgrad")
    """ORCAKeyword: Numerical gradient."""
    SURFCROSSNUMFREQ = ORCAKeyword("surfcrossnumfreq")
    """ORCAKeyword: Check for surface crossing frequency."""
    MECP_NUMFREQ = ORCAKeyword("mecp-numfreq")
    """ORCAKeyword: Numerical MECP freq."""
    NEARIR = ORCAKeyword("nearir")
    """ORCAKeyword: VPT2 analysis for nearIR."""
    VPT2 = ORCAKeyword("vpt2")
    """ORCAKeyword: VPT2 analysis."""
