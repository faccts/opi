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
        AtomicCharge
    ALLPOP : SimpleKeyword
        AtomicCharge
    CHELPG : SimpleKeyword
        AtomicCharge
    CHELPG_LARGE : SimpleKeyword
        AtomicCharge
    DENSITYANALYSIS : SimpleKeyword
        AtomicCharge
    FMOPOP : SimpleKeyword
        AtomicCharge
    FMOPOPULATIONS : SimpleKeyword
        AtomicCharge
    HIRSHFELD : SimpleKeyword
        AtomicCharge
    LOEWDIN : SimpleKeyword
        AtomicCharge
    MAYER : SimpleKeyword
        AtomicCharge
    MBIS : SimpleKeyword
        AtomicCharge
    MULLIKEN : SimpleKeyword
        AtomicCharge
    NOAIM : SimpleKeyword
        AtomicCharge
    NOFMOPOP : SimpleKeyword
        AtomicCharge
    NOFMOPOPULATIONS : SimpleKeyword
        AtomicCharge
    NOHIRSHFELD : SimpleKeyword
        AtomicCharge
    NOLOEWDIN : SimpleKeyword
        AtomicCharge
    NOMAYER : SimpleKeyword
        AtomicCharge
    NOMBIS : SimpleKeyword
        AtomicCharge
    NOMULLIKEN : SimpleKeyword
        AtomicCharge
    NONPA : SimpleKeyword
        AtomicCharge
    NOPOP : SimpleKeyword
        AtomicCharge
    NOREDUCEDPOP : SimpleKeyword
        AtomicCharge
    NPA : SimpleKeyword
        AtomicCharge
    REDUCEDPOP : SimpleKeyword
        AtomicCharge
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
    NOFMOPOPULATIONS = SimpleKeyword("nofmopopulations")
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
