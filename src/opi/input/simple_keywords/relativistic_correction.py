from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("RelativisticCorrection",)


class RelativisticCorrection(SimpleKeywordBox):
    """Enum to store all simple keywords of type RelativisticCorrection."""

    AMFI = SimpleKeyword("amfi")
    """SimpleKeyword: RelativisticCorrection."""
    DBOC = SimpleKeyword("dboc")
    """SimpleKeyword: RelativisticCorrection."""
    DKH = SimpleKeyword("dkh")
    """SimpleKeyword: RelativisticCorrection."""
    DKH1 = SimpleKeyword("dkh1")
    """SimpleKeyword: RelativisticCorrection."""
    DKH2 = SimpleKeyword("dkh2")
    """SimpleKeyword: RelativisticCorrection."""
    DLU_X2C = SimpleKeyword("dlu-x2c")
    """SimpleKeyword: RelativisticCorrection."""
    IORA = SimpleKeyword("iora")
    """SimpleKeyword: RelativisticCorrection."""
    IORA_RI = SimpleKeyword("iora/ri")
    """SimpleKeyword: RelativisticCorrection."""
    IORAMM_RI = SimpleKeyword("ioramm/ri")
    """SimpleKeyword: RelativisticCorrection."""
    NESC = SimpleKeyword("nesc")
    """SimpleKeyword: RelativisticCorrection."""
    NODBOC = SimpleKeyword("nodboc")
    """SimpleKeyword: RelativisticCorrection."""
    NOSOCENERGY = SimpleKeyword("nosocenergy")
    """SimpleKeyword: RelativisticCorrection."""
    REL1C = SimpleKeyword("rel1c")
    """SimpleKeyword: RelativisticCorrection."""
    RELDLU = SimpleKeyword("reldlu")
    """SimpleKeyword: RelativisticCorrection."""
    RELFULL = SimpleKeyword("relfull")
    """SimpleKeyword: RelativisticCorrection."""
    RI_SOMF = SimpleKeyword("ri-somf")
    """SimpleKeyword: RelativisticCorrection."""
    RI_SOMF_1X = SimpleKeyword("ri-somf(1x)")
    """SimpleKeyword: RelativisticCorrection."""
    RI_SOMF_4X = SimpleKeyword("ri-somf(4x)")
    """SimpleKeyword: RelativisticCorrection."""
    RI_SOMF_4XS = SimpleKeyword("ri-somf(4xs)")
    """SimpleKeyword: RelativisticCorrection."""
    SOCENERGY = SimpleKeyword("socenergy")
    """SimpleKeyword: RelativisticCorrection."""
    SOMF = SimpleKeyword("somf")
    """SimpleKeyword: RelativisticCorrection."""
    SOMF_1X = SimpleKeyword("somf(1x)")
    """SimpleKeyword: RelativisticCorrection."""
    SOMF_4X = SimpleKeyword("somf(4x)")
    """SimpleKeyword: RelativisticCorrection."""
    SOMF_4XS = SimpleKeyword("somf(4xs)")
    """SimpleKeyword: RelativisticCorrection."""
    VEFF_SOC = SimpleKeyword("veff-soc")
    """SimpleKeyword: RelativisticCorrection."""
    VEFF_2X_SOC = SimpleKeyword("veff(-2x)-soc")
    """SimpleKeyword: RelativisticCorrection."""
    X2C = SimpleKeyword("x2c")
    """SimpleKeyword: RelativisticCorrection."""
    ZEFF_SOC = SimpleKeyword("zeff-soc")
    """SimpleKeyword: RelativisticCorrection."""
    ZORA = SimpleKeyword("zora")
    """SimpleKeyword: RelativisticCorrection."""
    ZORA_RI = SimpleKeyword("zora/ri")
    """SimpleKeyword: RelativisticCorrection."""
