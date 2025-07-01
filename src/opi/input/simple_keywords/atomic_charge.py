from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("AtomicCharge",)


class AtomicCharge(SimpleKeywordBox):
    """Enum to store all simple keywords of type AtomicCharge.

    Attributes
    ----------
    AIM : SimpleKeyword
        Produce a WFN file for usage in AIM analysis.
    ALLPOP : SimpleKeyword
        Turns on all population analyses.
    CHELPG : SimpleKeyword
        Calculate CHELPG charges.
    CHELPG_LARGE : SimpleKeyword
        Calculate CHELPG charges with larger grids.
    DENSITYANALYSIS : SimpleKeyword
        Perform density analysis for fragments.
    FMOPOP : SimpleKeyword
        Request population analyses for HOMO and LUMO.
    HIRSHFELD : SimpleKeyword
        Calculate Hirshfeld charges.
    LOEWDIN : SimpleKeyword
        Calculate Loewdin charges.
    MAYER : SimpleKeyword
        Calculate Mayer charges.
    MBIS : SimpleKeyword
        Calculate Minimal Basis Iterative Stockholder (MBIS) charges.
    MULLIKEN : SimpleKeyword
        Calculate Mulliken charges.
    NOAIM : SimpleKeyword
        Do not create a WFN file for usage in AIM analysis.
    NOFMOPOP : SimpleKeyword
        Do not request population analyses for HOMO and LUMO.
    NOHIRSHFELD : SimpleKeyword
        Do not calculate Hirshfeld charges.
    NOLOEWDIN : SimpleKeyword
        Do not calculate Loewdin charges.
    NOMAYER : SimpleKeyword
        Do not calculate Mayer charges.
    NOMBIS : SimpleKeyword
        Do not calculate Minimal Basis Iterative Stockholder (MBIS) charges.
    NOMULLIKEN : SimpleKeyword
        Do not calculate Mulliken charges.
    NONPA : SimpleKeyword
        Do not calculate NPA charges.
    NOPOP : SimpleKeyword
        Turns off all population analyses.
    NOREDUCEDPOP : SimpleKeyword
        Do not print Loewdin reduced orb.pop per MO.
    NPA : SimpleKeyword
        Calculate NPA charges (requires the nbo package).
    REDUCEDPOP : SimpleKeyword
        Print Loewdin reduced orb.pop per MO.
    """

    AIM = SimpleKeyword("aim")
    ALLPOP = SimpleKeyword("allpop")
    CHELPG = SimpleKeyword("chelpg")
    CHELPG_LARGE = SimpleKeyword("chelpg(large)")
    DENSITYANALYSIS = SimpleKeyword("densityanalysis")
    FMOPOP = SimpleKeyword("fmopop")
    FMOPOPULATIONS = SimpleKeyword("fmopopulations")
    HIRSHFELD = SimpleKeyword("hirshfeld")
    LOEWDIN = SimpleKeyword("loewdin")
    MAYER = SimpleKeyword("mayer")
    MBIS = SimpleKeyword("mbis")
    MULLIKEN = SimpleKeyword("mulliken")
    NOAIM = SimpleKeyword("noaim")
    NOFMOPOP = SimpleKeyword("nofmopop")
    NOHIRSHFELD = SimpleKeyword("nohirshfeld")
    NOLOEWDIN = SimpleKeyword("noloewdin")
    NOMAYER = SimpleKeyword("nomayer")
    NOMBIS = SimpleKeyword("nombis")
    NOMULLIKEN = SimpleKeyword("nomulliken")
    NONPA = SimpleKeyword("nonpa")
    NOPOP = SimpleKeyword("nopop")
    NOREDUCEDPOP = SimpleKeyword("noreducedpop")
    NPA = SimpleKeyword("npa")
    REDUCEDPOP = SimpleKeyword("reducedpop")
