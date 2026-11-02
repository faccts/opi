from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Ecp",)


class Ecp(SimpleKeywordBox):
    """Enum to store all simple keywords of type Ecp."""

    CRENBL_ECP = ORCAKeyword("crenbl-ecp")
    """ORCAKeyword: effective core potentials."""
    DEFECP = ORCAKeyword("defecp")
    """ORCAKeyword: effective core potentials."""
    DEF2ECP = ORCAKeyword("def2ecp")
    """ORCAKeyword: effective core potentials."""
    DEF2_SD = ORCAKeyword("def2-sd")
    """ORCAKeyword: effective core potentials."""
    DHF_ECP = ORCAKeyword("dhf-ecp")
    """ORCAKeyword: effective core potentials."""
    DHFECP = ORCAKeyword("dhfecp")
    """ORCAKeyword: effective core potentials."""
    HAYWADT = ORCAKeyword("haywadt")
    """ORCAKeyword: effective core potentials."""
    LANL1 = ORCAKeyword("lanl1")
    """ORCAKeyword: effective core potentials."""
    LANL2 = ORCAKeyword("lanl2")
    """ORCAKeyword: effective core potentials."""
    SDD = ORCAKeyword("sdd")
    """ORCAKeyword: effective core potentials."""
    SK_MCDHF_RSC = ORCAKeyword("sk-mcdhf-rsc")
    """ORCAKeyword: effective core potentials."""
    VDZP_ECP = ORCAKeyword("vdzp-ecp")
    """ORCAKeyword: effective core potentials."""
    DEF2ECP_DEFECP_R2SCAN3C = ORCAKeyword("def2ecp/defecp/r2scan3c")
    """ORCAKeyword: effective core potentials (for r²SCAN-3c)s."""
