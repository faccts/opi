from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("AtomicCharge",)


class AtomicCharge(SimpleKeywordBox):
    """Enum to store all simple keywords of type AtomicCharge."""

    AIM = SimpleKeyword("aim")
    """SimpleKeyword: Produce a WFN file for usage in AIM analysis."""
    ALLPOP = SimpleKeyword("allpop")
    """SimpleKeyword: Turns on all population analyses."""
    CHELPG = SimpleKeyword("chelpg")
    """SimpleKeyword: Calculate CHELPG charges."""
    CHELPG_LARGE = SimpleKeyword("chelpg(large)")
    """SimpleKeyword: Calculate CHELPG charges with larger grids."""
    DENSITYANALYSIS = SimpleKeyword("densityanalysis")
    """SimpleKeyword: Perform density analysis for fragments."""
    FMOPOP = SimpleKeyword("fmopop")
    """SimpleKeyword: Request population analyses for HOMO and LUMO."""
    FMOPOPULATIONS = SimpleKeyword("fmopopulations")
    HIRSHFELD = SimpleKeyword("hirshfeld")
    """SimpleKeyword: Calculate Hirshfeld charges."""
    LOEWDIN = SimpleKeyword("loewdin")
    """SimpleKeyword: Calculate Loewdin charges."""
    MAYER = SimpleKeyword("mayer")
    """SimpleKeyword: Calculate Mayer charges."""
    MBIS = SimpleKeyword("mbis")
    """SimpleKeyword: Calculate Minimal Basis Iterative Stockholder (MBIS) charges."""
    MULLIKEN = SimpleKeyword("mulliken")
    """SimpleKeyword: Calculate Mulliken charges."""
    NOAIM = SimpleKeyword("noaim")
    """SimpleKeyword: Do not create a WFN file for usage in AIM analysis."""
    NOFMOPOP = SimpleKeyword("nofmopop")
    """SimpleKeyword: Do not request population analyses for HOMO and LUMO."""
    NOHIRSHFELD = SimpleKeyword("nohirshfeld")
    """SimpleKeyword: Do not calculate Hirshfeld charges."""
    NOLOEWDIN = SimpleKeyword("noloewdin")
    """SimpleKeyword: Do not calculate Loewdin charges."""
    NOMAYER = SimpleKeyword("nomayer")
    """SimpleKeyword: Do not calculate Mayer charges."""
    NOMBIS = SimpleKeyword("nombis")
    """SimpleKeyword: Do not calculate Minimal Basis Iterative Stockholder (MBIS) charges."""
    NOMULLIKEN = SimpleKeyword("nomulliken")
    """SimpleKeyword: Do not calculate Mulliken charges."""
    NONPA = SimpleKeyword("nonpa")
    """SimpleKeyword: Do not calculate NPA charges."""
    NOPOP = SimpleKeyword("nopop")
    """SimpleKeyword: Turns off all population analyses."""
    NOREDUCEDPOP = SimpleKeyword("noreducedpop")
    """SimpleKeyword: Do not print Loewdin reduced orb.pop per MO."""
    NPA = SimpleKeyword("npa")
    """SimpleKeyword: Calculate NPA charges (requires the nbo package)."""
    REDUCEDPOP = SimpleKeyword("reducedpop")
    """SimpleKeyword: Print Loewdin reduced orb.pop per MO."""
