from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Miscellaneous",)


class Miscellaneous(SimpleKeywordBox):
    """Enum to store all simple keywords of type Miscellaneous."""

    ANGS = SimpleKeyword("angs")
    """SimpleKeyword: Miscellaneous."""
    BOHRS = SimpleKeyword("bohrs")
    """SimpleKeyword: Miscellaneous."""
    CHEAPINTS = SimpleKeyword("cheapints")
    """SimpleKeyword: Miscellaneous."""
    KEEPDENSITY = SimpleKeyword("keepdensity")
    """SimpleKeyword: Miscellaneous."""
    KEEPFOCK = SimpleKeyword("keepfock")
    """SimpleKeyword: Miscellaneous."""
    KEEPINTS = SimpleKeyword("keepints")
    """SimpleKeyword: Miscellaneous."""
    KEEPRESPDENSITY = SimpleKeyword("keeprespdensity")
    """SimpleKeyword: Miscellaneous."""
    KEEPTRANSDENSITY = SimpleKeyword("keeptransdensity")
    """SimpleKeyword: Miscellaneous."""
    LIBINT = SimpleKeyword("libint")
    """SimpleKeyword: Libint for Integral generation."""
    MASS2016 = SimpleKeyword("mass2016")
    """SimpleKeyword: Miscellaneous."""
    NOCHEAPINTS = SimpleKeyword("nocheapints")
    """SimpleKeyword: Miscellaneous."""
    NOKEEPDENSITY = SimpleKeyword("nokeepdensity")
    """SimpleKeyword: Miscellaneous."""
    NOKEEPFOCK = SimpleKeyword("nokeepfock")
    """SimpleKeyword: Miscellaneous."""
    NOKEEPINTS = SimpleKeyword("nokeepints")
    """SimpleKeyword: Miscellaneous."""
    NOLIBINT = SimpleKeyword("nolibint")
    """SimpleKeyword: Libint for Integral generation."""
    NOREADINTS = SimpleKeyword("noreadints")
    """SimpleKeyword: Miscellaneous."""
    NOSHARK = SimpleKeyword("noshark")
    """SimpleKeyword: Shark for integral generation."""
    NOSYM = SimpleKeyword("nosym")
    """SimpleKeyword: Symmetry keywords."""
    NOSYMMETRY = SimpleKeyword("nosymmetry")
    """SimpleKeyword: Symmetry keywords."""
    NOUSESHARK = SimpleKeyword("nouseshark")
    """SimpleKeyword: Shark for integral generation."""
    NOUSESYM = SimpleKeyword("nousesym")
    """SimpleKeyword: Symmetry keywords."""
    NOUSESYMMETRY = SimpleKeyword("nousesymmetry")
    """SimpleKeyword: Symmetry keywords."""
    NOXCFUN = SimpleKeyword("noxcfun")
    """SimpleKeyword: do not use Xcfun library."""
    PREFERC2V = SimpleKeyword("preferc2v")
    """SimpleKeyword: Symmetry keywords."""
    PREFERD2 = SimpleKeyword("preferd2")
    """SimpleKeyword: Symmetry keywords."""
    READINTS = SimpleKeyword("readints")
    """SimpleKeyword: Miscellaneous."""
    RESCUE = SimpleKeyword("rescue")
    """SimpleKeyword: Try to rescue a calculation from an old orca version."""
    SCALEPC = SimpleKeyword("scalepc")
    """SimpleKeyword: Scale Pointcharges."""
    SHARK = SimpleKeyword("shark")
    """SimpleKeyword: Shark for integral generation."""
    USEC2V = SimpleKeyword("usec2v")
    """SimpleKeyword: Symmetry keywords."""
    USED2 = SimpleKeyword("used2")
    """SimpleKeyword: Symmetry keywords."""
    USESHARK = SimpleKeyword("useshark")
    """SimpleKeyword: Shark for integral generation."""
    USESYM = SimpleKeyword("usesym")
    """SimpleKeyword: Symmetry keywords."""
    USESYMMETRY = SimpleKeyword("usesymmetry")
    """SimpleKeyword: Symmetry keywords."""
    XCFUN = SimpleKeyword("xcfun")
    """SimpleKeyword: Use Xcfun library."""
    PAF = SimpleKeyword("paf")
    """SimpleKeyword: Bring molecule into its principle axis orientation."""
    ALLOWRHF = SimpleKeyword("allowrhf")
    """SimpleKeyword: AllowRHF for open-shell."""
    NOALLOWRHF = SimpleKeyword("noallowrhf")
    """SimpleKeyword: AllowRHF for open-shell."""
    DOEQ = SimpleKeyword("doeq")
    """SimpleKeyword: Do Eq for nuclear charges."""
    NOEQ = SimpleKeyword("noeq")
    """SimpleKeyword: Do not Eq for nuclear charges."""
    BPOP = SimpleKeyword("bpop")
    """SimpleKeyword: Use Boltzmann weighting in multiple xyz job."""
    NUMGRAD = SimpleKeyword("numgrad")
    """SimpleKeyword: Numerical gradient."""
    SURFCROSSNUMFREQ = SimpleKeyword("surfcrossnumfreq")
    """SimpleKeyword: Check for surface crossing frequency."""
    MECP_NUMFREQ = SimpleKeyword("mecp-numfreq")
    """SimpleKeyword: Numerical MECP freq."""
    NEARIR = SimpleKeyword("nearir")
    """SimpleKeyword: VPT2 analysis for nearIR."""
    VPT2 = SimpleKeyword("vpt2")
    """SimpleKeyword: VPT2 analysis."""
