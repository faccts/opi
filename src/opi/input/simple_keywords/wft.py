from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Wft",)


class Wft(SimpleKeywordBox):
    """Enum to store all simple keywords of type Wft."""

    HF = SimpleKeyword("hf")
    """SimpleKeyword: Hartee-Fock."""
    HF_3C = SimpleKeyword("hf-3c")
    """SimpleKeyword: 3c methods, do not require dispersion correction or basis set."""
    MP2 = SimpleKeyword("mp2")
    """SimpleKeyword: WFT Methods."""
    RIMP2 = SimpleKeyword("rimp2")
    """SimpleKeyword: WFT Methods."""
    OO_RI_MP2 = SimpleKeyword("oo-ri-mp2")
    """SimpleKeyword: WFT Methods."""
    SCS_MP2 = SimpleKeyword("scs-mp2")
    """SimpleKeyword: WFT Methods."""
    SOS_MP2 = SimpleKeyword("sos-mp2")
    """SimpleKeyword: WFT Methods."""
    DLPNO_MP2 = SimpleKeyword("dlpno-mp2")
    """SimpleKeyword: WFT Methods."""
    DLPNO_SCS_MP2 = SimpleKeyword("dlpno-scs-mp2")
    """SimpleKeyword: WFT Methods."""
    DLPNO_SOS_MP2 = SimpleKeyword("dlpno-sos-mp2")
    """SimpleKeyword: WFT Methods."""
    DLPNO_MP2_F12 = SimpleKeyword("dlpno-mp2-f12")
    """SimpleKeyword: WFT Methods."""
    DLPNO_MP2_F12D = SimpleKeyword("dlpno-mp2-f12d")
    """SimpleKeyword: WFT Methods."""
    MP3 = SimpleKeyword("mp3")
    """SimpleKeyword: WFT Methods."""
    SCS_MP3 = SimpleKeyword("scs-mp3")
    """SimpleKeyword: WFT Methods."""
    CCSD = SimpleKeyword("ccsd")
    """SimpleKeyword: WFT Methods."""
    CCSD_F12 = SimpleKeyword("ccsd-f12")
    """SimpleKeyword: WFT Methods."""
    DLPNO_CCSD = SimpleKeyword("dlpno-ccsd")
    """SimpleKeyword: WFT Methods."""
    DLPNO_CCSD_F12 = SimpleKeyword("dlpno-ccsd-f12")
    """SimpleKeyword: WFT Methods."""
    DLPNO_CCSD_F12D = SimpleKeyword("dlpno-ccsd-f12d")
    """SimpleKeyword: WFT Methods."""
    CCSD_T = SimpleKeyword("ccsd(t)")
    """SimpleKeyword: WFT Methods."""
    CCSD_T_F12 = SimpleKeyword("ccsd(t)-f12")
    """SimpleKeyword: WFT Methods."""
    DLPNO_CCSD_T = SimpleKeyword("dlpno-ccsd(t)")
    """SimpleKeyword: WFT Methods."""
    DLPNO_CCSD_T1 = SimpleKeyword("dlpno-ccsd(t1)")
    """SimpleKeyword: WFT Methods."""
    DLPNO_CCSD_T_F12 = SimpleKeyword("dlpno-ccsd(t)-f12")
    """SimpleKeyword: WFT Methods."""
    DLPNO_CCSD_T_F12D = SimpleKeyword("dlpno-ccsd(t)-f12d")
    """SimpleKeyword: WFT Methods."""
    DLPNO_CCSD_T1_F12 = SimpleKeyword("dlpno-ccsd(t1)-f12")
    """SimpleKeyword: WFT Methods."""
    DLPNO_CCSD_T1_F12D = SimpleKeyword("dlpno-ccsd(t1)-f12d")
    """SimpleKeyword: WFT Methods."""
    CISD = SimpleKeyword("cisd")
    """SimpleKeyword: WFT Methods."""
    CISD_T = SimpleKeyword("cisd(t)")
    """SimpleKeyword: WFT Methods."""
    CC2 = SimpleKeyword("cc2")
    """SimpleKeyword: WFT Methods."""
    ADC2 = SimpleKeyword("adc2")
    """SimpleKeyword: WFT Methods."""
    EOM_CCSD = SimpleKeyword("eom-ccsd")
    """SimpleKeyword: WFT Methods."""
    DLPNO_CISD = SimpleKeyword("dlpno-cisd")
    """SimpleKeyword: WFT Methods."""
    STEOM_CCSD = SimpleKeyword("steom-ccsd")
    """SimpleKeyword: WFT Methods."""
    DLPNO_STEOM_CCSD = SimpleKeyword("dlpno-steom-ccsd")
    """SimpleKeyword: WFT Methods."""
    CASPT2 = SimpleKeyword("caspt2")
    """SimpleKeyword: WFT Methods."""
    CASPT2K = SimpleKeyword("caspt2k")
    """SimpleKeyword: WFT Methods."""
    NEVPT2 = SimpleKeyword("nevpt2")
    """SimpleKeyword: WFT Methods."""
    SC_NEVPT2 = SimpleKeyword("sc-nevpt2")
    """SimpleKeyword: WFT Methods."""
    DLPNO_NEVPT2 = SimpleKeyword("dlpno-nevpt2")
    """SimpleKeyword: WFT Methods."""
