from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Wft",)


class DLPNOcc(SimpleKeywordBox):
    DLPNO_CCSD = ORCAKeyword("dlpno-ccsd")
    """ORCAKeyword: WFT Methods."""
    DLPNO_CCSD_T = ORCAKeyword("dlpno-ccsd(t)")
    """ORCAKeyword: WFT Methods."""


class Wft(DLPNOcc):
    """Enum to store all simple keywords of type Wft."""

    HF = ORCAKeyword("hf")
    """ORCAKeyword: Hartee-Fock."""
    HF_3C = ORCAKeyword("hf-3c")
    """ORCAKeyword: 3c methods, do not require dispersion correction or basis set."""
    MP2 = ORCAKeyword("mp2")
    """ORCAKeyword: WFT Methods."""
    RIMP2 = ORCAKeyword("rimp2")
    """ORCAKeyword: WFT Methods."""
    OO_RI_MP2 = ORCAKeyword("oo-ri-mp2")
    """ORCAKeyword: WFT Methods."""
    SCS_MP2 = ORCAKeyword("scs-mp2")
    """ORCAKeyword: WFT Methods."""
    SOS_MP2 = ORCAKeyword("sos-mp2")
    """ORCAKeyword: WFT Methods."""
    DLPNO_MP2 = ORCAKeyword("dlpno-mp2")
    """ORCAKeyword: WFT Methods."""
    DLPNO_SCS_MP2 = ORCAKeyword("dlpno-scs-mp2")
    """ORCAKeyword: WFT Methods."""
    DLPNO_SOS_MP2 = ORCAKeyword("dlpno-sos-mp2")
    """ORCAKeyword: WFT Methods."""
    DLPNO_MP2_F12 = ORCAKeyword("dlpno-mp2-f12")
    """ORCAKeyword: WFT Methods."""
    DLPNO_MP2_F12D = ORCAKeyword("dlpno-mp2-f12d")
    """ORCAKeyword: WFT Methods."""
    MP3 = ORCAKeyword("mp3")
    """ORCAKeyword: WFT Methods."""
    SCS_MP3 = ORCAKeyword("scs-mp3")
    """ORCAKeyword: WFT Methods."""
    CCSD = ORCAKeyword("ccsd")
    """ORCAKeyword: WFT Methods."""
    CCSD_F12 = ORCAKeyword("ccsd-f12")
    """ORCAKeyword: WFT Methods."""

    DLPNO_CCSD_F12 = ORCAKeyword("dlpno-ccsd-f12")
    """ORCAKeyword: WFT Methods."""
    DLPNO_CCSD_F12D = ORCAKeyword("dlpno-ccsd-f12d")
    """ORCAKeyword: WFT Methods."""
    CCSD_T = ORCAKeyword("ccsd(t)")
    """ORCAKeyword: WFT Methods."""
    CCSD_T_F12 = ORCAKeyword("ccsd(t)-f12")
    """ORCAKeyword: WFT Methods."""
    DLPNO_CCSD_T1 = ORCAKeyword("dlpno-ccsd(t1)")
    """ORCAKeyword: WFT Methods."""
    DLPNO_CCSD_T_F12 = ORCAKeyword("dlpno-ccsd(t)-f12")
    """ORCAKeyword: WFT Methods."""
    DLPNO_CCSD_T_F12D = ORCAKeyword("dlpno-ccsd(t)-f12d")
    """ORCAKeyword: WFT Methods."""
    DLPNO_CCSD_T1_F12 = ORCAKeyword("dlpno-ccsd(t1)-f12")
    """ORCAKeyword: WFT Methods."""
    DLPNO_CCSD_T1_F12D = ORCAKeyword("dlpno-ccsd(t1)-f12d")
    """ORCAKeyword: WFT Methods."""
    CISD = ORCAKeyword("cisd")
    """ORCAKeyword: WFT Methods."""
    CISD_T = ORCAKeyword("cisd(t)")
    """ORCAKeyword: WFT Methods."""
    CC2 = ORCAKeyword("cc2")
    """ORCAKeyword: WFT Methods."""
    ADC2 = ORCAKeyword("adc2")
    """ORCAKeyword: WFT Methods."""
    EOM_CCSD = ORCAKeyword("eom-ccsd")
    """ORCAKeyword: WFT Methods."""
    DLPNO_CISD = ORCAKeyword("dlpno-cisd")
    """ORCAKeyword: WFT Methods."""
    STEOM_CCSD = ORCAKeyword("steom-ccsd")
    """ORCAKeyword: WFT Methods."""
    DLPNO_STEOM_CCSD = ORCAKeyword("dlpno-steom-ccsd")
    """ORCAKeyword: WFT Methods."""
    CASPT2 = ORCAKeyword("caspt2")
    """ORCAKeyword: WFT Methods."""
    CASPT2K = ORCAKeyword("caspt2k")
    """ORCAKeyword: WFT Methods."""
    NEVPT2 = ORCAKeyword("nevpt2")
    """ORCAKeyword: WFT Methods."""
    SC_NEVPT2 = ORCAKeyword("sc-nevpt2")
    """ORCAKeyword: WFT Methods."""
    DLPNO_NEVPT2 = ORCAKeyword("dlpno-nevpt2")
    """ORCAKeyword: WFT Methods."""
