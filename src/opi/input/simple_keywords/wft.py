from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Wft",)


class Wft(SimpleKeywordBox):
    """Enum to store all simple keywords of type Wft.

    Attributes
    ----------
    HF : SimpleKeyword
        Hartee-Fock
    HF_3C : SimpleKeyword
        3c methods, do not require dispersion correction or basis set
    MP2 : SimpleKeyword
        WFT Methods
    RIMP2 : SimpleKeyword
        WFT Methods
    OO_RI_MP2 : SimpleKeyword
        WFT Methods
    SCS_MP2 : SimpleKeyword
        WFT Methods
    SOS_MP2 : SimpleKeyword
        WFT Methods
    DLPNO_MP2 : SimpleKeyword
        WFT Methods
    DLPNO_SCS_MP2 : SimpleKeyword
        WFT Methods
    DLPNO_SOS_MP2 : SimpleKeyword
        WFT Methods
    DLPNO_MP2_F12 : SimpleKeyword
        WFT Methods
    DLPNO_MP2_F12D : SimpleKeyword
        WFT Methods
    MP3 : SimpleKeyword
        WFT Methods
    SCS_MP3 : SimpleKeyword
        WFT Methods
    CCSD : SimpleKeyword
        WFT Methods
    CCSD_F12 : SimpleKeyword
        WFT Methods
    DLPNO_CCSD : SimpleKeyword
        WFT Methods
    DLPNO_CCSD_F12 : SimpleKeyword
        WFT Methods
    DLPNO_CCSD_F12D : SimpleKeyword
        WFT Methods
    CCSD_T : SimpleKeyword
        WFT Methods
    CCSD_T_F12 : SimpleKeyword
        WFT Methods
    DLPNO_CCSD_T : SimpleKeyword
        WFT Methods
    DLPNO_CCSD_T1 : SimpleKeyword
        WFT Methods
    DLPNO_CCSD_T_F12 : SimpleKeyword
        WFT Methods
    DLPNO_CCSD_T_F12D : SimpleKeyword
        WFT Methods
    DLPNO_CCSD_T1_F12 : SimpleKeyword
        WFT Methods
    DLPNO_CCSD_T1_F12D : SimpleKeyword
        WFT Methods
    CISD : SimpleKeyword
        WFT Methods
    CISD_T : SimpleKeyword
        WFT Methods
    CC2 : SimpleKeyword
        WFT Methods
    ADC2 : SimpleKeyword
        WFT Methods
    EOM_CCSD : SimpleKeyword
        WFT Methods
    DLPNO_CISD : SimpleKeyword
        WFT Methods
    STEOM_CCSD : SimpleKeyword
        WFT Methods
    DLPNO_STEOM_CCSD : SimpleKeyword
        WFT Methods
    CASPT2 : SimpleKeyword
        WFT Methods
    CASPT2K : SimpleKeyword
        WFT Methods
    NEVPT2 : SimpleKeyword
        WFT Methods
    SC_NEVPT2 : SimpleKeyword
        WFT Methods
    DLPNO_NEVPT2 : SimpleKeyword
        WFT Methods
    """

    HF = SimpleKeyword("hf")
    HF_3C = SimpleKeyword("hf-3c")
    MP2 = SimpleKeyword("mp2")
    RIMP2 = SimpleKeyword("rimp2")
    OO_RI_MP2 = SimpleKeyword("oo-ri-mp2")
    SCS_MP2 = SimpleKeyword("scs-mp2")
    SOS_MP2 = SimpleKeyword("sos-mp2")
    DLPNO_MP2 = SimpleKeyword("dlpno-mp2")
    DLPNO_SCS_MP2 = SimpleKeyword("dlpno-scs-mp2")
    DLPNO_SOS_MP2 = SimpleKeyword("dlpno-sos-mp2")
    DLPNO_MP2_F12 = SimpleKeyword("dlpno-mp2-f12")
    DLPNO_MP2_F12D = SimpleKeyword("dlpno-mp2-f12d")
    MP3 = SimpleKeyword("mp3")
    SCS_MP3 = SimpleKeyword("scs-mp3")
    CCSD = SimpleKeyword("ccsd")
    CCSD_F12 = SimpleKeyword("ccsd-f12")
    DLPNO_CCSD = SimpleKeyword("dlpno-ccsd")
    DLPNO_CCSD_F12 = SimpleKeyword("dlpno-ccsd-f12")
    DLPNO_CCSD_F12D = SimpleKeyword("dlpno-ccsd-f12d")
    CCSD_T = SimpleKeyword("ccsd(t)")
    CCSD_T_F12 = SimpleKeyword("ccsd(t)-f12")
    DLPNO_CCSD_T = SimpleKeyword("dlpno-ccsd(t)")
    DLPNO_CCSD_T1 = SimpleKeyword("dlpno-ccsd(t1)")
    DLPNO_CCSD_T_F12 = SimpleKeyword("dlpno-ccsd(t)-f12")
    DLPNO_CCSD_T_F12D = SimpleKeyword("dlpno-ccsd(t)-f12d")
    DLPNO_CCSD_T1_F12 = SimpleKeyword("dlpno-ccsd(t1)-f12")
    DLPNO_CCSD_T1_F12D = SimpleKeyword("dlpno-ccsd(t1)-f12d")
    CISD = SimpleKeyword("cisd")
    CISD_T = SimpleKeyword("cisd(t)")
    CC2 = SimpleKeyword("cc2")
    ADC2 = SimpleKeyword("adc2")
    EOM_CCSD = SimpleKeyword("eom-ccsd")
    DLPNO_CISD = SimpleKeyword("dlpno-cisd")
    STEOM_CCSD = SimpleKeyword("steom-ccsd")
    DLPNO_STEOM_CCSD = SimpleKeyword("dlpno-steom-ccsd")
    CASPT2 = SimpleKeyword("caspt2")
    CASPT2K = SimpleKeyword("caspt2k")
    NEVPT2 = SimpleKeyword("nevpt2")
    SC_NEVPT2 = SimpleKeyword("sc-nevpt2")
    DLPNO_NEVPT2 = SimpleKeyword("dlpno-nevpt2")
