from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("RelativisticCorrection",)


class RelativisticCorrection(SimpleKeywordBox):
    """Enum to store all simple keywords of type RelativisticCorrection."""

    AMFI = ORCAKeyword("amfi")
    """ORCAKeyword: RelativisticCorrection."""
    DBOC = ORCAKeyword("dboc")
    """ORCAKeyword: RelativisticCorrection."""
    DKH = ORCAKeyword("dkh")
    """ORCAKeyword: RelativisticCorrection."""
    DKH1 = ORCAKeyword("dkh1")
    """ORCAKeyword: RelativisticCorrection."""
    DKH2 = ORCAKeyword("dkh2")
    """ORCAKeyword: RelativisticCorrection."""
    DLU_X2C = ORCAKeyword("dlu-x2c")
    """ORCAKeyword: RelativisticCorrection."""
    IORA = ORCAKeyword("iora")
    """ORCAKeyword: RelativisticCorrection."""
    IORA_RI = ORCAKeyword("iora/ri")
    """ORCAKeyword: RelativisticCorrection."""
    IORAMM_RI = ORCAKeyword("ioramm/ri")
    """ORCAKeyword: RelativisticCorrection."""
    NESC = ORCAKeyword("nesc")
    """ORCAKeyword: RelativisticCorrection."""
    NODBOC = ORCAKeyword("nodboc")
    """ORCAKeyword: RelativisticCorrection."""
    NOSOCENERGY = ORCAKeyword("nosocenergy")
    """ORCAKeyword: RelativisticCorrection."""
    REL1C = ORCAKeyword("rel1c")
    """ORCAKeyword: RelativisticCorrection."""
    RELDLU = ORCAKeyword("reldlu")
    """ORCAKeyword: RelativisticCorrection."""
    RELFULL = ORCAKeyword("relfull")
    """ORCAKeyword: RelativisticCorrection."""
    RI_SOMF = ORCAKeyword("ri-somf")
    """ORCAKeyword: RelativisticCorrection."""
    RI_SOMF_1X = ORCAKeyword("ri-somf(1x)")
    """ORCAKeyword: RelativisticCorrection."""
    RI_SOMF_4X = ORCAKeyword("ri-somf(4x)")
    """ORCAKeyword: RelativisticCorrection."""
    RI_SOMF_4XS = ORCAKeyword("ri-somf(4xs)")
    """ORCAKeyword: RelativisticCorrection."""
    SOCENERGY = ORCAKeyword("socenergy")
    """ORCAKeyword: RelativisticCorrection."""
    SOMF = ORCAKeyword("somf")
    """ORCAKeyword: RelativisticCorrection."""
    SOMF_1X = ORCAKeyword("somf(1x)")
    """ORCAKeyword: RelativisticCorrection."""
    SOMF_4X = ORCAKeyword("somf(4x)")
    """ORCAKeyword: RelativisticCorrection."""
    SOMF_4XS = ORCAKeyword("somf(4xs)")
    """ORCAKeyword: RelativisticCorrection."""
    VEFF_SOC = ORCAKeyword("veff-soc")
    """ORCAKeyword: RelativisticCorrection."""
    VEFF_2X_SOC = ORCAKeyword("veff(-2x)-soc")
    """ORCAKeyword: RelativisticCorrection."""
    X2C = ORCAKeyword("x2c")
    """ORCAKeyword: RelativisticCorrection."""
    ZEFF_SOC = ORCAKeyword("zeff-soc")
    """ORCAKeyword: RelativisticCorrection."""
    ZORA = ORCAKeyword("zora")
    """ORCAKeyword: RelativisticCorrection."""
    ZORA_RI = ORCAKeyword("zora/ri")
    """ORCAKeyword: RelativisticCorrection."""
