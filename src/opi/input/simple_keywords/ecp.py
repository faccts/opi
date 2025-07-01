from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Ecp",)


class Ecp(SimpleKeywordBox):
    """Enum to store all simple keywords of type Ecp.

    Attributes
    ----------
    CRENBL_ECP : SimpleKeyword
        effective core potentials
    DEFECP : SimpleKeyword
        effective core potentials
    DEF2ECP : SimpleKeyword
        effective core potentials
    DEF2_SD : SimpleKeyword
        effective core potentials
    DHF_ECP : SimpleKeyword
        effective core potentials
    DHFECP : SimpleKeyword
        effective core potentials
    HAYWADT : SimpleKeyword
        effective core potentials
    LANL1 : SimpleKeyword
        effective core potentials
    LANL2 : SimpleKeyword
        effective core potentials
    SDD : SimpleKeyword
        effective core potentials
    SK_MCDHF_RSC : SimpleKeyword
        effective core potentials
    VDZP_ECP : SimpleKeyword
        effective core potentials
    DEF2ECP_DEFECP_R2SCAN3C : SimpleKeyword
        effective core potentials (for r²SCAN-3c)s
    """

    CRENBL_ECP = SimpleKeyword("crenbl-ecp")
    DEFECP = SimpleKeyword("defecp")
    DEF2ECP = SimpleKeyword("def2ecp")
    DEF2_SD = SimpleKeyword("def2-sd")
    DHF_ECP = SimpleKeyword("dhf-ecp")
    DHFECP = SimpleKeyword("dhfecp")
    HAYWADT = SimpleKeyword("haywadt")
    LANL1 = SimpleKeyword("lanl1")
    LANL2 = SimpleKeyword("lanl2")
    SDD = SimpleKeyword("sdd")
    SK_MCDHF_RSC = SimpleKeyword("sk-mcdhf-rsc")
    VDZP_ECP = SimpleKeyword("vdzp-ecp")
    DEF2ECP_DEFECP_R2SCAN3C = SimpleKeyword("def2ecp/defecp/r2scan3c")
