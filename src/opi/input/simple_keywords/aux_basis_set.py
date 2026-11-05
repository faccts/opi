from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("AuxBasisSet",)


class AuxBasisSet(SimpleKeywordBox):
    """Enum to store all simple keywords of type AuxBasisSet."""

    AUTOAUX = ORCAKeyword("autoaux")
    """ORCAKeyword: Can be used as replacement for any AuxBasisSet."""
    AUTOAUXTRIM = ORCAKeyword("autoauxtrim")
    """ORCAKeyword: trims the autoaux basis."""
    AUG_CC_PV5Z_C = ORCAKeyword("aug-cc-pv5z/c")
    """ORCAKeyword: AuxBasisSet."""
    AUG_CC_PV5Z_JK = ORCAKeyword("aug-cc-pv5z/jk")
    """ORCAKeyword: AuxBasisSet."""
    AUG_CC_PV6Z_C = ORCAKeyword("aug-cc-pv6z/c")
    """ORCAKeyword: AuxBasisSet."""
    AUG_CC_PVDZ_PP_C = ORCAKeyword("aug-cc-pvdz-pp/c")
    """ORCAKeyword: AuxBasisSet."""
    AUG_CC_PVDZ_C = ORCAKeyword("aug-cc-pvdz/c")
    """ORCAKeyword: AuxBasisSet."""
    AUG_CC_PVQZ_PP_C = ORCAKeyword("aug-cc-pvqz-pp/c")
    """ORCAKeyword: AuxBasisSet."""
    AUG_CC_PVQZ_C = ORCAKeyword("aug-cc-pvqz/c")
    """ORCAKeyword: AuxBasisSet."""
    AUG_CC_PVQZ_JK = ORCAKeyword("aug-cc-pvqz/jk")
    """ORCAKeyword: AuxBasisSet."""
    AUG_CC_PVTZ_PP_C = ORCAKeyword("aug-cc-pvtz-pp/c")
    """ORCAKeyword: AuxBasisSet."""
    AUG_CC_PVTZ_C = ORCAKeyword("aug-cc-pvtz/c")
    """ORCAKeyword: AuxBasisSet."""
    AUG_CC_PVTZ_JK = ORCAKeyword("aug-cc-pvtz/jk")
    """ORCAKeyword: AuxBasisSet."""
    AUG_CC_PWCV5Z_C = ORCAKeyword("aug-cc-pwcv5z/c")
    """ORCAKeyword: AuxBasisSet."""
    AUG_CC_PWCVDZ_PP_C = ORCAKeyword("aug-cc-pwcvdz-pp/c")
    """ORCAKeyword: AuxBasisSet."""
    AUG_CC_PWCVDZ_C = ORCAKeyword("aug-cc-pwcvdz/c")
    """ORCAKeyword: AuxBasisSet."""
    AUG_CC_PWCVQZ_PP_C = ORCAKeyword("aug-cc-pwcvqz-pp/c")
    """ORCAKeyword: AuxBasisSet."""
    AUG_CC_PWCVQZ_C = ORCAKeyword("aug-cc-pwcvqz/c")
    """ORCAKeyword: AuxBasisSet."""
    AUG_CC_PWCVTZ_PP_C = ORCAKeyword("aug-cc-pwcvtz-pp/c")
    """ORCAKeyword: AuxBasisSet."""
    AUG_CC_PWCVTZ_C = ORCAKeyword("aug-cc-pwcvtz/c")
    """ORCAKeyword: AuxBasisSet."""
    CC_PCVDZ_F12_MP2FIT = ORCAKeyword("cc-pcvdz-f12-mp2fit")
    """ORCAKeyword: AuxBasisSet."""
    CC_PCVQZ_F12_MP2FIT = ORCAKeyword("cc-pcvqz-f12-mp2fit")
    """ORCAKeyword: AuxBasisSet."""
    CC_PCVTZ_F12_MP2FIT = ORCAKeyword("cc-pcvtz-f12-mp2fit")
    """ORCAKeyword: AuxBasisSet."""
    CC_PV5Z_C = ORCAKeyword("cc-pv5z/c")
    """ORCAKeyword: AuxBasisSet."""
    CC_PV5Z_JK = ORCAKeyword("cc-pv5z/jk")
    """ORCAKeyword: AuxBasisSet."""
    CC_PV6Z_C = ORCAKeyword("cc-pv6z/c")
    """ORCAKeyword: AuxBasisSet."""
    CC_PVDZ_F12_MP2FIT = ORCAKeyword("cc-pvdz-f12-mp2fit")
    """ORCAKeyword: AuxBasisSet."""
    CC_PVDZ_PP_F12_MP2FIT = ORCAKeyword("cc-pvdz-pp-f12-mp2fit")
    """ORCAKeyword: AuxBasisSet."""
    CC_PVDZ_PP_C = ORCAKeyword("cc-pvdz-pp/c")
    """ORCAKeyword: AuxBasisSet."""
    CC_PVDZ_C = ORCAKeyword("cc-pvdz/c")
    """ORCAKeyword: AuxBasisSet."""
    CC_PVQZ_F12_MP2FIT = ORCAKeyword("cc-pvqz-f12-mp2fit")
    """ORCAKeyword: AuxBasisSet."""
    CC_PVQZ_PP_F12_MP2FIT = ORCAKeyword("cc-pvqz-pp-f12-mp2fit")
    """ORCAKeyword: AuxBasisSet."""
    CC_PVQZ_PP_C = ORCAKeyword("cc-pvqz-pp/c")
    """ORCAKeyword: AuxBasisSet."""
    CC_PVQZ_C = ORCAKeyword("cc-pvqz/c")
    """ORCAKeyword: AuxBasisSet."""
    CC_PVQZ_JK = ORCAKeyword("cc-pvqz/jk")
    """ORCAKeyword: AuxBasisSet."""
    CC_PVTZ_F12_MP2FIT = ORCAKeyword("cc-pvtz-f12-mp2fit")
    """ORCAKeyword: AuxBasisSet."""
    CC_PVTZ_PP_F12_MP2FIT = ORCAKeyword("cc-pvtz-pp-f12-mp2fit")
    """ORCAKeyword: AuxBasisSet."""
    CC_PVTZ_PP_C = ORCAKeyword("cc-pvtz-pp/c")
    """ORCAKeyword: AuxBasisSet."""
    CC_PVTZ_C = ORCAKeyword("cc-pvtz/c")
    """ORCAKeyword: AuxBasisSet."""
    CC_PVTZ_JK = ORCAKeyword("cc-pvtz/jk")
    """ORCAKeyword: AuxBasisSet."""
    CC_PWCV5Z_C = ORCAKeyword("cc-pwcv5z/c")
    """ORCAKeyword: AuxBasisSet."""
    CC_PWCVDZ_PP_C = ORCAKeyword("cc-pwcvdz-pp/c")
    """ORCAKeyword: AuxBasisSet."""
    CC_PWCVDZ_C = ORCAKeyword("cc-pwcvdz/c")
    """ORCAKeyword: AuxBasisSet."""
    CC_PWCVQZ_PP_C = ORCAKeyword("cc-pwcvqz-pp/c")
    """ORCAKeyword: AuxBasisSet."""
    CC_PWCVQZ_C = ORCAKeyword("cc-pwcvqz/c")
    """ORCAKeyword: AuxBasisSet."""
    CC_PWCVTZ_PP_C = ORCAKeyword("cc-pwcvtz-pp/c")
    """ORCAKeyword: AuxBasisSet."""
    CC_PWCVTZ_C = ORCAKeyword("cc-pwcvtz/c")
    """ORCAKeyword: AuxBasisSet."""
    DEF_J = ORCAKeyword("def/j")
    """ORCAKeyword: AuxBasisSet."""
    DEF2_MSVP_J = ORCAKeyword("def2-msvp/j")
    """ORCAKeyword: AuxBasisSet."""
    DEF2_MTZVP_J = ORCAKeyword("def2-mtzvp/j")
    """ORCAKeyword: AuxBasisSet."""
    DEF2_MTZVPP_J = ORCAKeyword("def2-mtzvpp/j")
    """ORCAKeyword: AuxBasisSet."""
    DEF2_QZVPP_C = ORCAKeyword("def2-qzvpp/c")
    """ORCAKeyword: AuxBasisSet."""
    DEF2_QZVPPD_C = ORCAKeyword("def2-qzvppd/c")
    """ORCAKeyword: AuxBasisSet."""
    DEF2_SVP_C = ORCAKeyword("def2-svp/c")
    """ORCAKeyword: AuxBasisSet."""
    DEF2_SVPD_C = ORCAKeyword("def2-svpd/c")
    """ORCAKeyword: AuxBasisSet."""
    DEF2_TZVP_C = ORCAKeyword("def2-tzvp/c")
    """ORCAKeyword: AuxBasisSet."""
    DEF2_TZVPD_C = ORCAKeyword("def2-tzvpd/c")
    """ORCAKeyword: AuxBasisSet."""
    DEF2_TZVPP_C = ORCAKeyword("def2-tzvpp/c")
    """ORCAKeyword: AuxBasisSet."""
    DEF2_TZVPPD_C = ORCAKeyword("def2-tzvppd/c")
    """ORCAKeyword: AuxBasisSet."""
    DEF2_J = ORCAKeyword("def2/j")
    """ORCAKeyword: AuxBasisSet."""
    DEF2_JK = ORCAKeyword("def2/jk")
    """ORCAKeyword: AuxBasisSet."""
    DEF2_JKSMALL = ORCAKeyword("def2/jksmall")
    """ORCAKeyword: AuxBasisSet."""
    DGAUSS_A1_J = ORCAKeyword("dgauss-a1/j")
    """ORCAKeyword: AuxBasisSet."""
    DGAUSS_A2_J = ORCAKeyword("dgauss-a2/j")
    """ORCAKeyword: AuxBasisSet."""
    MIN_J = ORCAKeyword("min/j")
    """ORCAKeyword: AuxBasisSet."""
    SARC_J = ORCAKeyword("sarc/j")
    """ORCAKeyword: AuxBasisSet."""
    SARC2_DKH_QZV_JK = ORCAKeyword("sarc2-dkh-qzv/jk")
    """ORCAKeyword: AuxBasisSet."""
    SARC2_DKH_QZVP_JK = ORCAKeyword("sarc2-dkh-qzvp/jk")
    """ORCAKeyword: AuxBasisSet."""
    SARC2_ZORA_QZV_JK = ORCAKeyword("sarc2-zora-qzv/jk")
    """ORCAKeyword: AuxBasisSet."""
    SARC2_ZORA_QZVP_JK = ORCAKeyword("sarc2-zora-qzvp/jk")
    """ORCAKeyword: AuxBasisSet."""
    X2C_J = ORCAKeyword("x2c/j")
    """ORCAKeyword: AuxBasisSet."""
