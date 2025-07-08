from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("AuxBasisSet",)


class AuxBasisSet(SimpleKeywordBox):
    """Enum to store all simple keywords of type AuxBasisSet."""

    AUTOAUX = SimpleKeyword("autoaux")
    """SimpleKeyword: Can be used as replacement for any AuxBasisSet."""
    AUTOAUXTRIM = SimpleKeyword("autoauxtrim")
    """SimpleKeyword: trims the autoaux basis."""
    AUG_CC_PV5Z_C = SimpleKeyword("aug-cc-pv5z/c")
    """SimpleKeyword: AuxBasisSet."""
    AUG_CC_PV5Z_JK = SimpleKeyword("aug-cc-pv5z/jk")
    """SimpleKeyword: AuxBasisSet."""
    AUG_CC_PV6Z_C = SimpleKeyword("aug-cc-pv6z/c")
    """SimpleKeyword: AuxBasisSet."""
    AUG_CC_PVDZ_PP_C = SimpleKeyword("aug-cc-pvdz-pp/c")
    """SimpleKeyword: AuxBasisSet."""
    AUG_CC_PVDZ_C = SimpleKeyword("aug-cc-pvdz/c")
    """SimpleKeyword: AuxBasisSet."""
    AUG_CC_PVQZ_PP_C = SimpleKeyword("aug-cc-pvqz-pp/c")
    """SimpleKeyword: AuxBasisSet."""
    AUG_CC_PVQZ_C = SimpleKeyword("aug-cc-pvqz/c")
    """SimpleKeyword: AuxBasisSet."""
    AUG_CC_PVQZ_JK = SimpleKeyword("aug-cc-pvqz/jk")
    """SimpleKeyword: AuxBasisSet."""
    AUG_CC_PVTZ_PP_C = SimpleKeyword("aug-cc-pvtz-pp/c")
    """SimpleKeyword: AuxBasisSet."""
    AUG_CC_PVTZ_C = SimpleKeyword("aug-cc-pvtz/c")
    """SimpleKeyword: AuxBasisSet."""
    AUG_CC_PVTZ_C = SimpleKeyword("aug-cc-pvtz/c")
    """SimpleKeyword: AuxBasisSet."""
    AUG_CC_PVTZ_JK = SimpleKeyword("aug-cc-pvtz/jk")
    """SimpleKeyword: AuxBasisSet."""
    AUG_CC_PWCV5Z_C = SimpleKeyword("aug-cc-pwcv5z/c")
    """SimpleKeyword: AuxBasisSet."""
    AUG_CC_PWCVDZ_PP_C = SimpleKeyword("aug-cc-pwcvdz-pp/c")
    """SimpleKeyword: AuxBasisSet."""
    AUG_CC_PWCVDZ_C = SimpleKeyword("aug-cc-pwcvdz/c")
    """SimpleKeyword: AuxBasisSet."""
    AUG_CC_PWCVQZ_PP_C = SimpleKeyword("aug-cc-pwcvqz-pp/c")
    """SimpleKeyword: AuxBasisSet."""
    AUG_CC_PWCVQZ_C = SimpleKeyword("aug-cc-pwcvqz/c")
    """SimpleKeyword: AuxBasisSet."""
    AUG_CC_PWCVTZ_PP_C = SimpleKeyword("aug-cc-pwcvtz-pp/c")
    """SimpleKeyword: AuxBasisSet."""
    AUG_CC_PWCVTZ_C = SimpleKeyword("aug-cc-pwcvtz/c")
    """SimpleKeyword: AuxBasisSet."""
    CC_PCVDZ_F12_MP2FIT = SimpleKeyword("cc-pcvdz-f12-mp2fit")
    """SimpleKeyword: AuxBasisSet."""
    CC_PCVQZ_F12_MP2FIT = SimpleKeyword("cc-pcvqz-f12-mp2fit")
    """SimpleKeyword: AuxBasisSet."""
    CC_PCVTZ_F12_MP2FIT = SimpleKeyword("cc-pcvtz-f12-mp2fit")
    """SimpleKeyword: AuxBasisSet."""
    CC_PV5Z_C = SimpleKeyword("cc-pv5z/c")
    """SimpleKeyword: AuxBasisSet."""
    CC_PV5Z_JK = SimpleKeyword("cc-pv5z/jk")
    """SimpleKeyword: AuxBasisSet."""
    CC_PV6Z_C = SimpleKeyword("cc-pv6z/c")
    """SimpleKeyword: AuxBasisSet."""
    CC_PVDZ_F12_MP2FIT = SimpleKeyword("cc-pvdz-f12-mp2fit")
    """SimpleKeyword: AuxBasisSet."""
    CC_PVDZ_PP_F12_MP2FIT = SimpleKeyword("cc-pvdz-pp-f12-mp2fit")
    """SimpleKeyword: AuxBasisSet."""
    CC_PVDZ_PP_C = SimpleKeyword("cc-pvdz-pp/c")
    """SimpleKeyword: AuxBasisSet."""
    CC_PVDZ_C = SimpleKeyword("cc-pvdz/c")
    """SimpleKeyword: AuxBasisSet."""
    CC_PVQZ_F12_MP2FIT = SimpleKeyword("cc-pvqz-f12-mp2fit")
    """SimpleKeyword: AuxBasisSet."""
    CC_PVQZ_PP_F12_MP2FIT = SimpleKeyword("cc-pvqz-pp-f12-mp2fit")
    """SimpleKeyword: AuxBasisSet."""
    CC_PVQZ_PP_C = SimpleKeyword("cc-pvqz-pp/c")
    """SimpleKeyword: AuxBasisSet."""
    CC_PVQZ_C = SimpleKeyword("cc-pvqz/c")
    """SimpleKeyword: AuxBasisSet."""
    CC_PVQZ_JK = SimpleKeyword("cc-pvqz/jk")
    """SimpleKeyword: AuxBasisSet."""
    CC_PVTZ_F12_MP2FIT = SimpleKeyword("cc-pvtz-f12-mp2fit")
    """SimpleKeyword: AuxBasisSet."""
    CC_PVTZ_PP_F12_MP2FIT = SimpleKeyword("cc-pvtz-pp-f12-mp2fit")
    """SimpleKeyword: AuxBasisSet."""
    CC_PVTZ_PP_C = SimpleKeyword("cc-pvtz-pp/c")
    """SimpleKeyword: AuxBasisSet."""
    CC_PVTZ_C = SimpleKeyword("cc-pvtz/c")
    """SimpleKeyword: AuxBasisSet."""
    CC_PVTZ_JK = SimpleKeyword("cc-pvtz/jk")
    """SimpleKeyword: AuxBasisSet."""
    CC_PWCV5Z_C = SimpleKeyword("cc-pwcv5z/c")
    """SimpleKeyword: AuxBasisSet."""
    CC_PWCVDZ_PP_C = SimpleKeyword("cc-pwcvdz-pp/c")
    """SimpleKeyword: AuxBasisSet."""
    CC_PWCVDZ_C = SimpleKeyword("cc-pwcvdz/c")
    """SimpleKeyword: AuxBasisSet."""
    CC_PWCVQZ_PP_C = SimpleKeyword("cc-pwcvqz-pp/c")
    """SimpleKeyword: AuxBasisSet."""
    CC_PWCVQZ_C = SimpleKeyword("cc-pwcvqz/c")
    """SimpleKeyword: AuxBasisSet."""
    CC_PWCVTZ_PP_C = SimpleKeyword("cc-pwcvtz-pp/c")
    """SimpleKeyword: AuxBasisSet."""
    CC_PWCVTZ_C = SimpleKeyword("cc-pwcvtz/c")
    """SimpleKeyword: AuxBasisSet."""
    DEF_J = SimpleKeyword("def/j")
    """SimpleKeyword: AuxBasisSet."""
    DEF2_MSVP_J = SimpleKeyword("def2-msvp/j")
    """SimpleKeyword: AuxBasisSet."""
    DEF2_MTZVP_J = SimpleKeyword("def2-mtzvp/j")
    """SimpleKeyword: AuxBasisSet."""
    DEF2_MTZVPP_J = SimpleKeyword("def2-mtzvpp/j")
    """SimpleKeyword: AuxBasisSet."""
    DEF2_QZVPP_C = SimpleKeyword("def2-qzvpp/c")
    """SimpleKeyword: AuxBasisSet."""
    DEF2_QZVPPD_C = SimpleKeyword("def2-qzvppd/c")
    """SimpleKeyword: AuxBasisSet."""
    DEF2_SVP_C = SimpleKeyword("def2-svp/c")
    """SimpleKeyword: AuxBasisSet."""
    DEF2_SVPD_C = SimpleKeyword("def2-svpd/c")
    """SimpleKeyword: AuxBasisSet."""
    DEF2_TZVP_C = SimpleKeyword("def2-tzvp/c")
    """SimpleKeyword: AuxBasisSet."""
    DEF2_TZVPD_C = SimpleKeyword("def2-tzvpd/c")
    """SimpleKeyword: AuxBasisSet."""
    DEF2_TZVPP_C = SimpleKeyword("def2-tzvpp/c")
    """SimpleKeyword: AuxBasisSet."""
    DEF2_TZVPPD_C = SimpleKeyword("def2-tzvppd/c")
    """SimpleKeyword: AuxBasisSet."""
    DEF2_J = SimpleKeyword("def2/j")
    """SimpleKeyword: AuxBasisSet."""
    DEF2_JK = SimpleKeyword("def2/jk")
    """SimpleKeyword: AuxBasisSet."""
    DEF2_JKSMALL = SimpleKeyword("def2/jksmall")
    """SimpleKeyword: AuxBasisSet."""
    DGAUSS_A1_J = SimpleKeyword("dgauss-a1/j")
    """SimpleKeyword: AuxBasisSet."""
    DGAUSS_A2_J = SimpleKeyword("dgauss-a2/j")
    """SimpleKeyword: AuxBasisSet."""
    MIN_J = SimpleKeyword("min/j")
    """SimpleKeyword: AuxBasisSet."""
    SARC_J = SimpleKeyword("sarc/j")
    """SimpleKeyword: AuxBasisSet."""
    SARC2_DKH_QZV_JK = SimpleKeyword("sarc2-dkh-qzv/jk")
    """SimpleKeyword: AuxBasisSet."""
    SARC2_DKH_QZVP_JK = SimpleKeyword("sarc2-dkh-qzvp/jk")
    """SimpleKeyword: AuxBasisSet."""
    SARC2_ZORA_QZV_JK = SimpleKeyword("sarc2-zora-qzv/jk")
    """SimpleKeyword: AuxBasisSet."""
    SARC2_ZORA_QZVP_JK = SimpleKeyword("sarc2-zora-qzvp/jk")
    """SimpleKeyword: AuxBasisSet."""
    X2C_J = SimpleKeyword("x2c/j")
    """SimpleKeyword: AuxBasisSet."""
