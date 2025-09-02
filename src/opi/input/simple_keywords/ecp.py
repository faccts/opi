from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Ecp",)


class Ecp(SimpleKeywordBox):
    """Enum to store all simple keywords of type Ecp."""

    CRENBL_ECP = SimpleKeyword("crenbl-ecp")
    """SimpleKeyword: effective core potentials."""
    DEFECP = SimpleKeyword("defecp")
    """SimpleKeyword: effective core potentials."""
    DEF2ECP = SimpleKeyword("def2ecp")
    """SimpleKeyword: effective core potentials."""
    DEF2_SD = SimpleKeyword("def2-sd")
    """SimpleKeyword: effective core potentials."""
    DHF_ECP = SimpleKeyword("dhf-ecp")
    """SimpleKeyword: effective core potentials."""
    DHFECP = SimpleKeyword("dhfecp")
    """SimpleKeyword: effective core potentials."""
    HAYWADT = SimpleKeyword("haywadt")
    """SimpleKeyword: effective core potentials."""
    LANL1 = SimpleKeyword("lanl1")
    """SimpleKeyword: effective core potentials."""
    LANL2 = SimpleKeyword("lanl2")
    """SimpleKeyword: effective core potentials."""
    SDD = SimpleKeyword("sdd")
    """SimpleKeyword: effective core potentials."""
    SK_MCDHF_RSC = SimpleKeyword("sk-mcdhf-rsc")
    """SimpleKeyword: effective core potentials."""
    VDZP_ECP = SimpleKeyword("vdzp-ecp")
    """SimpleKeyword: effective core potentials."""
    DEF2ECP_DEFECP_R2SCAN3C = SimpleKeyword("def2ecp/defecp/r2scan3c")
    """SimpleKeyword: effective core potentials (for r²SCAN-3c)s."""
