from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("AuxBasisSet",)


class AuxBasisSet(SimpleKeywordBox):
    """Enum to store all simple keywords of type AuxBasisSet.

    Attributes
    ----------
    AUTOAUX : SimpleKeyword
        Can be used as replacement for any AuxBasisSet
    AUTOAUXTRIM : SimpleKeyword
        trims the autoaux basis
    AUG_CC_PV5Z_C : SimpleKeyword
        AuxBasisSet
    AUG_CC_PV5Z_JK : SimpleKeyword
        AuxBasisSet
    AUG_CC_PV6Z_C : SimpleKeyword
        AuxBasisSet
    AUG_CC_PVDZ_PP_C : SimpleKeyword
        AuxBasisSet
    AUG_CC_PVDZ_C : SimpleKeyword
        AuxBasisSet
    AUG_CC_PVQZ_PP_C : SimpleKeyword
        AuxBasisSet
    AUG_CC_PVQZ_C : SimpleKeyword
        AuxBasisSet
    AUG_CC_PVQZ_JK : SimpleKeyword
        AuxBasisSet
    AUG_CC_PVTZ_PP_C : SimpleKeyword
        AuxBasisSet
    AUG_CC_PVTZ_C : SimpleKeyword
        AuxBasisSet
    AUG_CC_PVTZ_C : SimpleKeyword
        AuxBasisSet
    AUG_CC_PVTZ_JK : SimpleKeyword
        AuxBasisSet
    AUG_CC_PWCV5Z_C : SimpleKeyword
        AuxBasisSet
    AUG_CC_PWCVDZ_PP_C : SimpleKeyword
        AuxBasisSet
    AUG_CC_PWCVDZ_C : SimpleKeyword
        AuxBasisSet
    AUG_CC_PWCVQZ_PP_C : SimpleKeyword
        AuxBasisSet
    AUG_CC_PWCVQZ_C : SimpleKeyword
        AuxBasisSet
    AUG_CC_PWCVTZ_PP_C : SimpleKeyword
        AuxBasisSet
    AUG_CC_PWCVTZ_C : SimpleKeyword
        AuxBasisSet
    CC_PCVDZ_F12_MP2FIT : SimpleKeyword
        AuxBasisSet
    CC_PCVQZ_F12_MP2FIT : SimpleKeyword
        AuxBasisSet
    CC_PCVTZ_F12_MP2FIT : SimpleKeyword
        AuxBasisSet
    CC_PV5Z_C : SimpleKeyword
        AuxBasisSet
    CC_PV5Z_JK : SimpleKeyword
        AuxBasisSet
    CC_PV6Z_C : SimpleKeyword
        AuxBasisSet
    CC_PVDZ_F12_MP2FIT : SimpleKeyword
        AuxBasisSet
    CC_PVDZ_PP_F12_MP2FIT : SimpleKeyword
        AuxBasisSet
    CC_PVDZ_PP_C : SimpleKeyword
        AuxBasisSet
    CC_PVDZ_C : SimpleKeyword
        AuxBasisSet
    CC_PVQZ_F12_MP2FIT : SimpleKeyword
        AuxBasisSet
    CC_PVQZ_PP_F12_MP2FIT : SimpleKeyword
        AuxBasisSet
    CC_PVQZ_PP_C : SimpleKeyword
        AuxBasisSet
    CC_PVQZ_C : SimpleKeyword
        AuxBasisSet
    CC_PVQZ_JK : SimpleKeyword
        AuxBasisSet
    CC_PVTZ_F12_MP2FIT : SimpleKeyword
        AuxBasisSet
    CC_PVTZ_PP_F12_MP2FIT : SimpleKeyword
        AuxBasisSet
    CC_PVTZ_PP_C : SimpleKeyword
        AuxBasisSet
    CC_PVTZ_C : SimpleKeyword
        AuxBasisSet
    CC_PVTZ_JK : SimpleKeyword
        AuxBasisSet
    CC_PWCV5Z_C : SimpleKeyword
        AuxBasisSet
    CC_PWCVDZ_PP_C : SimpleKeyword
        AuxBasisSet
    CC_PWCVDZ_C : SimpleKeyword
        AuxBasisSet
    CC_PWCVQZ_PP_C : SimpleKeyword
        AuxBasisSet
    CC_PWCVQZ_C : SimpleKeyword
        AuxBasisSet
    CC_PWCVTZ_PP_C : SimpleKeyword
        AuxBasisSet
    CC_PWCVTZ_C : SimpleKeyword
        AuxBasisSet
    DEF_J : SimpleKeyword
        AuxBasisSet
    DEF2_MSVP_J : SimpleKeyword
        AuxBasisSet
    DEF2_MTZVP_J : SimpleKeyword
        AuxBasisSet
    DEF2_MTZVPP_J : SimpleKeyword
        AuxBasisSet
    DEF2_QZVPP_C : SimpleKeyword
        AuxBasisSet
    DEF2_QZVPPD_C : SimpleKeyword
        AuxBasisSet
    DEF2_SVP_C : SimpleKeyword
        AuxBasisSet
    DEF2_SVPD_C : SimpleKeyword
        AuxBasisSet
    DEF2_TZVP_C : SimpleKeyword
        AuxBasisSet
    DEF2_TZVPD_C : SimpleKeyword
        AuxBasisSet
    DEF2_TZVPP_C : SimpleKeyword
        AuxBasisSet
    DEF2_TZVPPD_C : SimpleKeyword
        AuxBasisSet
    DEF2_J : SimpleKeyword
        AuxBasisSet
    DEF2_JK : SimpleKeyword
        AuxBasisSet
    DEF2_JKSMALL : SimpleKeyword
        AuxBasisSet
    DGAUSS_A1_J : SimpleKeyword
        AuxBasisSet
    DGAUSS_A2_J : SimpleKeyword
        AuxBasisSet
    MIN_J : SimpleKeyword
        AuxBasisSet
    SARC_J : SimpleKeyword
        AuxBasisSet
    SARC2_DKH_QZV_JK : SimpleKeyword
        AuxBasisSet
    SARC2_DKH_QZVP_JK : SimpleKeyword
        AuxBasisSet
    SARC2_ZORA_QZV_JK : SimpleKeyword
        AuxBasisSet
    SARC2_ZORA_QZVP_JK : SimpleKeyword
        AuxBasisSet
    X2C_J : SimpleKeyword
        AuxBasisSet
    """

    AUTOAUX = SimpleKeyword("autoaux")
    AUTOAUXTRIM = SimpleKeyword("autoauxtrim")
    AUG_CC_PV5Z_C = SimpleKeyword("aug-cc-pv5z/c")
    AUG_CC_PV5Z_JK = SimpleKeyword("aug-cc-pv5z/jk")
    AUG_CC_PV6Z_C = SimpleKeyword("aug-cc-pv6z/c")
    AUG_CC_PVDZ_PP_C = SimpleKeyword("aug-cc-pvdz-pp/c")
    AUG_CC_PVDZ_C = SimpleKeyword("aug-cc-pvdz/c")
    AUG_CC_PVQZ_PP_C = SimpleKeyword("aug-cc-pvqz-pp/c")
    AUG_CC_PVQZ_C = SimpleKeyword("aug-cc-pvqz/c")
    AUG_CC_PVQZ_JK = SimpleKeyword("aug-cc-pvqz/jk")
    AUG_CC_PVTZ_PP_C = SimpleKeyword("aug-cc-pvtz-pp/c")
    AUG_CC_PVTZ_C = SimpleKeyword("aug-cc-pvtz/c")
    AUG_CC_PVTZ_C = SimpleKeyword("aug-cc-pvtz/c")
    AUG_CC_PVTZ_JK = SimpleKeyword("aug-cc-pvtz/jk")
    AUG_CC_PWCV5Z_C = SimpleKeyword("aug-cc-pwcv5z/c")
    AUG_CC_PWCVDZ_PP_C = SimpleKeyword("aug-cc-pwcvdz-pp/c")
    AUG_CC_PWCVDZ_C = SimpleKeyword("aug-cc-pwcvdz/c")
    AUG_CC_PWCVQZ_PP_C = SimpleKeyword("aug-cc-pwcvqz-pp/c")
    AUG_CC_PWCVQZ_C = SimpleKeyword("aug-cc-pwcvqz/c")
    AUG_CC_PWCVTZ_PP_C = SimpleKeyword("aug-cc-pwcvtz-pp/c")
    AUG_CC_PWCVTZ_C = SimpleKeyword("aug-cc-pwcvtz/c")
    CC_PCVDZ_F12_MP2FIT = SimpleKeyword("cc-pcvdz-f12-mp2fit")
    CC_PCVQZ_F12_MP2FIT = SimpleKeyword("cc-pcvqz-f12-mp2fit")
    CC_PCVTZ_F12_MP2FIT = SimpleKeyword("cc-pcvtz-f12-mp2fit")
    CC_PV5Z_C = SimpleKeyword("cc-pv5z/c")
    CC_PV5Z_JK = SimpleKeyword("cc-pv5z/jk")
    CC_PV6Z_C = SimpleKeyword("cc-pv6z/c")
    CC_PVDZ_F12_MP2FIT = SimpleKeyword("cc-pvdz-f12-mp2fit")
    CC_PVDZ_PP_F12_MP2FIT = SimpleKeyword("cc-pvdz-pp-f12-mp2fit")
    CC_PVDZ_PP_C = SimpleKeyword("cc-pvdz-pp/c")
    CC_PVDZ_C = SimpleKeyword("cc-pvdz/c")
    CC_PVQZ_F12_MP2FIT = SimpleKeyword("cc-pvqz-f12-mp2fit")
    CC_PVQZ_PP_F12_MP2FIT = SimpleKeyword("cc-pvqz-pp-f12-mp2fit")
    CC_PVQZ_PP_C = SimpleKeyword("cc-pvqz-pp/c")
    CC_PVQZ_C = SimpleKeyword("cc-pvqz/c")
    CC_PVQZ_JK = SimpleKeyword("cc-pvqz/jk")
    CC_PVTZ_F12_MP2FIT = SimpleKeyword("cc-pvtz-f12-mp2fit")
    CC_PVTZ_PP_F12_MP2FIT = SimpleKeyword("cc-pvtz-pp-f12-mp2fit")
    CC_PVTZ_PP_C = SimpleKeyword("cc-pvtz-pp/c")
    CC_PVTZ_C = SimpleKeyword("cc-pvtz/c")
    CC_PVTZ_JK = SimpleKeyword("cc-pvtz/jk")
    CC_PWCV5Z_C = SimpleKeyword("cc-pwcv5z/c")
    CC_PWCVDZ_PP_C = SimpleKeyword("cc-pwcvdz-pp/c")
    CC_PWCVDZ_C = SimpleKeyword("cc-pwcvdz/c")
    CC_PWCVQZ_PP_C = SimpleKeyword("cc-pwcvqz-pp/c")
    CC_PWCVQZ_C = SimpleKeyword("cc-pwcvqz/c")
    CC_PWCVTZ_PP_C = SimpleKeyword("cc-pwcvtz-pp/c")
    CC_PWCVTZ_C = SimpleKeyword("cc-pwcvtz/c")
    DEF_J = SimpleKeyword("def/j")
    DEF2_MSVP_J = SimpleKeyword("def2-msvp/j")
    DEF2_MTZVP_J = SimpleKeyword("def2-mtzvp/j")
    DEF2_MTZVPP_J = SimpleKeyword("def2-mtzvpp/j")
    DEF2_QZVPP_C = SimpleKeyword("def2-qzvpp/c")
    DEF2_QZVPPD_C = SimpleKeyword("def2-qzvppd/c")
    DEF2_SVP_C = SimpleKeyword("def2-svp/c")
    DEF2_SVPD_C = SimpleKeyword("def2-svpd/c")
    DEF2_TZVP_C = SimpleKeyword("def2-tzvp/c")
    DEF2_TZVPD_C = SimpleKeyword("def2-tzvpd/c")
    DEF2_TZVPP_C = SimpleKeyword("def2-tzvpp/c")
    DEF2_TZVPPD_C = SimpleKeyword("def2-tzvppd/c")
    DEF2_J = SimpleKeyword("def2/j")
    DEF2_JK = SimpleKeyword("def2/jk")
    DEF2_JKSMALL = SimpleKeyword("def2/jksmall")
    DGAUSS_A1_J = SimpleKeyword("dgauss-a1/j")
    DGAUSS_A2_J = SimpleKeyword("dgauss-a2/j")
    MIN_J = SimpleKeyword("min/j")
    SARC_J = SimpleKeyword("sarc/j")
    SARC2_DKH_QZV_JK = SimpleKeyword("sarc2-dkh-qzv/jk")
    SARC2_DKH_QZVP_JK = SimpleKeyword("sarc2-dkh-qzvp/jk")
    SARC2_ZORA_QZV_JK = SimpleKeyword("sarc2-zora-qzv/jk")
    SARC2_ZORA_QZVP_JK = SimpleKeyword("sarc2-zora-qzvp/jk")
    X2C_J = SimpleKeyword("x2c/j")
