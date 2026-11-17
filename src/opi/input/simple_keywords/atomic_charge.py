from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("AtomicCharge",)


class AtomicCharge(SimpleKeywordBox):
    """Enum to store all simple keywords of type AtomicCharge."""

    AIM = ORCAKeyword("aim")
    """ORCAKeyword: Produce a WFN file for usage in AIM analysis."""
    ALLPOP = ORCAKeyword("allpop")
    """ORCAKeyword: Turns on all population analyses."""
    CHELPG = ORCAKeyword("chelpg")
    """ORCAKeyword: Calculate CHELPG charges."""
    CHELPG_LARGE = ORCAKeyword("chelpg(large)")
    """ORCAKeyword: Calculate CHELPG charges with larger grids."""
    DENSITYANALYSIS = ORCAKeyword("densityanalysis")
    """ORCAKeyword: Perform density analysis for fragments."""
    FMOPOP = ORCAKeyword("fmopop")
    """ORCAKeyword: Request population analyses for HOMO and LUMO."""
    HIRSHFELD = ORCAKeyword("hirshfeld")
    """ORCAKeyword: Calculate Hirshfeld charges."""
    LOEWDIN = ORCAKeyword("loewdin")
    """ORCAKeyword: Calculate Loewdin charges."""
    MAYER = ORCAKeyword("mayer")
    """ORCAKeyword: Calculate Mayer charges."""
    MBIS = ORCAKeyword("mbis")
    """ORCAKeyword: Calculate Minimal Basis Iterative Stockholder (MBIS) charges."""
    MULLIKEN = ORCAKeyword("mulliken")
    """ORCAKeyword: Calculate Mulliken charges."""
    NOAIM = ORCAKeyword("noaim")
    """ORCAKeyword: Do not create a WFN file for usage in AIM analysis."""
    NOFMOPOP = ORCAKeyword("nofmopop")
    """ORCAKeyword: Do not request population analyses for HOMO and LUMO."""
    NOHIRSHFELD = ORCAKeyword("nohirshfeld")
    """ORCAKeyword: Do not calculate Hirshfeld charges."""
    NOLOEWDIN = ORCAKeyword("noloewdin")
    """ORCAKeyword: Do not calculate Loewdin charges."""
    NOMAYER = ORCAKeyword("nomayer")
    """ORCAKeyword: Do not calculate Mayer charges."""
    NOMBIS = ORCAKeyword("nombis")
    """ORCAKeyword: Do not calculate Minimal Basis Iterative Stockholder (MBIS) charges."""
    NOMULLIKEN = ORCAKeyword("nomulliken")
    """ORCAKeyword: Do not calculate Mulliken charges."""
    NONPA = ORCAKeyword("nonpa")
    """ORCAKeyword: Do not calculate NPA charges."""
    NOPOP = ORCAKeyword("nopop")
    """ORCAKeyword: Turns off all population analyses."""
    NOREDUCEDPOP = ORCAKeyword("noreducedpop")
    """ORCAKeyword: Do not print Loewdin reduced orb.pop per MO."""
    NPA = ORCAKeyword("npa")
    """ORCAKeyword: Calculate NPA charges (requires the nbo package)."""
    REDUCEDPOP = ORCAKeyword("reducedpop")
    """ORCAKeyword: Print Loewdin reduced orb.pop per MO."""
    RESP = ORCAKeyword("resp")
    """ORCAKeyword: Calculate RESP charges (special CHELPG variant)"""
